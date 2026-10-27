from flask import Flask, request, jsonify
import requests
import urllib3
from protobuf_decoder.protobuf_decoder import Parser
import struct

app = Flask(__name__)
urllib3.disable_warnings()

# Constants
BASE_URL = "https://clientbp.ggpolarbear.com"

# Helper: Encode UID into protobuf format matching the working examples
def encode_uid_protobuf(uid, field_number=1):
    """
    Encodes a UID into a protobuf binary message.
    Matches format of working hex requests
    """
    # For field 1, wire type 0 (varint) = (1 << 3) | 0 = 8
    tag = 8
    
    def varint_encode(n):
        result = []
        while n > 0x7f:
            result.append((n & 0x7f) | 0x80)
            n >>= 7
        result.append(n)
        return bytes(result)
    
    return varint_encode(tag) + varint_encode(uid)

def encode_friend_action_payload(uid, second_value=6711906302):
    """
    Creates protobuf payload matching the working examples
    Format: field 1 (varint) + field 2 (varint)
    """
    # Field 1: target UID
    tag1 = 8  # field 1, varint
    uid_encoded = varint_encode(uid)
    
    # Field 2: second value (from working examples)
    tag2 = 16  # field 2, varint
    second_encoded = varint_encode(second_value)
    
    return tag1.to_bytes(1, 'little') + uid_encoded + tag2.to_bytes(1, 'little') + second_encoded

def varint_encode(n):
    """Encode integer as protobuf varint"""
    result = []
    while n > 0x7f:
        result.append((n & 0x7f) | 0x80)
        n >>= 7
    result.append(n)
    return bytes(result)

def get_pending_uids(auth_token):
    """Extract pending friend request UIDs"""
    
    url = f"{BASE_URL}/GetFriendRequestList"
    
    headers = {
        "Host": "clientbp.ggpolarbear.com",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)",
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Unity-Version": "2018.4.11f1",
        "X-GA": "v1 1",
        "ReleaseVersion": "OB53",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "Expect": "100-continue",
    }
    
    # Hex request from GetFriendRequestList endpoint
    binary_body = bytes.fromhex("a390e8e0fa11cd88d1ea7bfd7d6944b3")
    response = requests.post(url, headers=headers, data=binary_body, verify=False)
    
    uids = []
    
    if len(response.content) > 0:
        try:
            parser = Parser()
            decoded = parser.parse(response.content.hex())
            
            def extract(data):
                if not hasattr(data, 'results'):
                    return
                for r in data.results:
                    if r.field == 1 and isinstance(r.data, int) and r.data > 1000000000:
                        uids.append(r.data)
                    if hasattr(r.data, 'results'):
                        for sub in r.data.results:
                            if sub.field == 1 and isinstance(sub.data, int) and sub.data > 1000000000:
                                uids.append(sub.data)
                    extract(r.data)
            
            extract(decoded)
        except Exception as e:
            print(f"Error parsing protobuf: {e}")
    
    return list(set(uids))

def get_player_info(uid):
    """Fetch player info from bbytop API"""
    url = f"https://bbytop-info-api-v1.vercel.app/info?uid={uid}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                "uid": uid,
                "name": data.get("player_info", {}).get("nickname", "N/A"),
                "level": data.get("player_info", {}).get("level", "N/A"),
                "likes": data.get("raw_api_response", {}).get("basicInfo", {}).get("liked", "N/A"),
                "region": data.get("player_info", {}).get("region", "N/A"),
                "is_banned": data.get("player_info", {}).get("is_banned", False)
            }
        else:
            return None
    except Exception as e:
        print(f"Error fetching player info for {uid}: {e}")
        return None

def send_friend_action(auth_token, target_uid, action_type):
    """
    Sends accept or reject request for a friend request.
    action_type: 'accept' -> ConfirmFriendRequest, 'reject' -> DeclineFriendRequest
    """
    if action_type == 'accept':
        url = f"{BASE_URL}/ConfirmFriendRequest"
        # Using working hex payload structure from example
        payload = bytes.fromhex("f5caa991f33787ecf0e291ba3cea0472")
    elif action_type == 'reject':
        url = f"{BASE_URL}/DeclineFriendRequest"
        # Using working hex payload structure from example
        payload = bytes.fromhex("6916a002fa8b9474fbad2a094faa1592")
    else:
        raise ValueError("Invalid action_type")
    
    headers = {
        "Host": "clientbp.ggpolarbear.com",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)",
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Unity-Version": "2018.4.11f1",
        "X-GA": "v1 1",
        "ReleaseVersion": "OB53",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "Expect": "100-continue",
    }
    
    # Note: The payload already contains the UID encoded
    # We need to replace the UID in the payload with target_uid
    # Since the working examples have specific UIDs, we need to create dynamic payload
    
    # Create dynamic payload with target UID
    dynamic_payload = encode_friend_action_payload(target_uid)
    
    response = requests.post(url, headers=headers, data=dynamic_payload, verify=False)
    return response

# API Endpoints
@app.route('/requestlist', methods=['GET'])
def get_request_list():
    """Get pending friend requests list"""
    
    jwt_token = request.args.get('jwt')
    if not jwt_token:
        return jsonify({
            "success": False,
            "error": "Missing jwt parameter",
            "message": "Usage: /requestlist?jwt=YOUR_TOKEN"
        }), 400
    
    try:
        uids = get_pending_uids(jwt_token)
        if not uids:
            return jsonify({
                "success": True,
                "count": 0,
                "requests": [],
                "message": "No pending friend requests"
            })
        
        requests_list = []
        for uid in uids:
            info = get_player_info(uid)
            if info:
                requests_list.append(info)
            else:
                requests_list.append({
                    "uid": uid,
                    "name": "Unknown",
                    "level": "N/A",
                    "likes": "N/A",
                    "region": "N/A"
                })
        
        return jsonify({
            "success": True,
            "count": len(requests_list),
            "requests": requests_list
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to fetch friend requests"
        }), 500

@app.route('/accept', methods=['GET', 'POST'])
def accept_friend():
    """Accept a pending friend request"""
    # Get parameters from query string or JSON body
    if request.method == 'GET':
        jwt_token = request.args.get('jwt')
        uid = request.args.get('uid')
    else:  # POST
        data = request.get_json() or {}
        jwt_token = data.get('jwt') or request.args.get('jwt')
        uid = data.get('uid') or request.args.get('uid')
    
    if not jwt_token:
        return jsonify({"success": False, "error": "Missing jwt parameter"}), 400
    if not uid:
        return jsonify({"success": False, "error": "Missing uid parameter"}), 400
    
    try:
        uid = int(uid)
        response = send_friend_action(jwt_token, uid, 'accept')
        
        if response.status_code == 200:
            return jsonify({
                "success": True,
                "message": f"Friend request from UID {uid} accepted successfully",
                "status_code": response.status_code,
                "response_hex": response.content.hex() if response.content else ""
            })
        else:
            return jsonify({
                "success": False,
                "error": f"Accept failed with status {response.status_code}",
                "details": response.text[:200],
                "response_hex": response.content.hex() if response.content else ""
            }), response.status_code
    except ValueError:
        return jsonify({"success": False, "error": "UID must be a valid number"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/reject', methods=['GET', 'POST'])
def reject_friend():
    """Reject a pending friend request"""
    # Get parameters from query string or JSON body
    if request.method == 'GET':
        jwt_token = request.args.get('jwt')
        uid = request.args.get('uid')
    else:  # POST
        data = request.get_json() or {}
        jwt_token = data.get('jwt') or request.args.get('jwt')
        uid = data.get('uid') or request.args.get('uid')
    
    if not jwt_token:
        return jsonify({"success": False, "error": "Missing jwt parameter"}), 400
    if not uid:
        return jsonify({"success": False, "error": "Missing uid parameter"}), 400
    
    try:
        uid = int(uid)
        response = send_friend_action(jwt_token, uid, 'reject')
        
        if response.status_code == 200:
            return jsonify({
                "success": True,
                "message": f"Friend request from UID {uid} rejected successfully",
                "status_code": response.status_code,
                "response_hex": response.content.hex() if response.content else ""
            })
        else:
            return jsonify({
                "success": False,
                "error": f"Reject failed with status {response.status_code}",
                "details": response.text[:200],
                "response_hex": response.content.hex() if response.content else ""
            }), response.status_code
    except ValueError:
        return jsonify({"success": False, "error": "UID must be a valid number"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/bulk_action', methods=['POST'])
def bulk_action():
    """Accept or reject multiple friend requests at once"""
    data = request.get_json()
    
    if not data:
        return jsonify({"success": False, "error": "Missing JSON body"}), 400
    
    jwt_token = data.get('jwt')
    action = data.get('action')  # 'accept' or 'reject'
    uids = data.get('uids', [])
    
    if not jwt_token:
        return jsonify({"success": False, "error": "Missing jwt parameter"}), 400
    if action not in ['accept', 'reject']:
        return jsonify({"success": False, "error": "Action must be 'accept' or 'reject'"}), 400
    if not uids or not isinstance(uids, list):
        return jsonify({"success": False, "error": "uids must be a non-empty list"}), 400
    
    results = []
    success_count = 0
    failed_count = 0
    
    for uid in uids:
        try:
            uid_int = int(uid)
            response = send_friend_action(jwt_token, uid_int, action)
            
            if response.status_code == 200:
                success_count += 1
                results.append({
                    "uid": uid_int,
                    "success": True,
                    "message": f"Successfully {action}ed"
                })
            else:
                failed_count += 1
                results.append({
                    "uid": uid_int,
                    "success": False,
                    "error": f"Status {response.status_code}",
                    "details": response.text[:100]
                })
        except Exception as e:
            failed_count += 1
            results.append({
                "uid": uid,
                "success": False,
                "error": str(e)
            })
    
    return jsonify({
        "success": True,
        "action": action,
        "total": len(uids),
        "success_count": success_count,
        "failed_count": failed_count,
        "results": results
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "ok",
        "service": "Free Fire Friend Request API",
        "version": "2.0",
        "endpoints": [
            "GET  /requestlist?jwt=TOKEN",
            "GET  /accept?jwt=TOKEN&uid=UID",
            "GET  /reject?jwt=TOKEN&uid=UID",
            "POST /accept (JSON: {jwt, uid})",
            "POST /reject (JSON: {jwt, uid})",
            "POST /bulk_action (JSON: {jwt, action, uids: []})",
            "GET  /health"
        ]
    })

@app.route('/', methods=['GET'])
def root():
    return jsonify({
        "service": "Free Fire Friend Request API",
        "version": "2.0",
        "base_url": BASE_URL,
        "usage": {
            "list_pending": "/requestlist?jwt=YOUR_TOKEN",
            "accept_request": "/accept?jwt=YOUR_TOKEN&uid=TARGET_UID",
            "reject_request": "/reject?jwt=YOUR_TOKEN&uid=TARGET_UID",
            "bulk_accept": "POST /bulk_action with JSON: {'jwt': 'TOKEN', 'action': 'accept', 'uids': [123, 456]}",
            "bulk_reject": "POST /bulk_action with JSON: {'jwt': 'TOKEN', 'action': 'reject', 'uids': [123, 456]}"
        },
        "examples": {
            "curl_list": "curl 'http://localhost:5770/requestlist?jwt=eyJhbGci...'",
            "curl_accept": "curl 'http://localhost:5770/accept?jwt=eyJhbGci...&uid=1234567890'",
            "curl_reject": "curl 'http://localhost:5770/reject?jwt=eyJhbGci...&uid=1234567890'",
            "curl_bulk_accept": "curl -X POST http://localhost:5770/bulk_action -H 'Content-Type: application/json' -d '{\"jwt\":\"TOKEN\",\"action\":\"accept\",\"uids\":[123,456,789]}'"
        }
    })

if __name__ == "__main__":
    print("="*60)
    print("FREE FIRE FRIEND REQUEST API v2.0")
    print("="*60)
    print(f"Base URL: {BASE_URL}")
    print("Starting server on http://0.0.0.0:5770")
    print("")
    print("Endpoints:")
    print("  GET  /                                            - API info")
    print("  GET  /health                                      - Health check")
    print("  GET  /requestlist?jwt=TOKEN                       - Get pending requests")
    print("  GET  /accept?jwt=TOKEN&uid=UID                    - Accept request")
    print("  GET  /reject?jwt=TOKEN&uid=UID                    - Reject request")
    print("  POST /accept (JSON body)                          - Accept request")
    print("  POST /reject (JSON body)                          - Reject request")
    print("  POST /bulk_action (JSON body)                     - Bulk accept/reject")
    print("")
    print("Examples:")
    print("  # List pending requests")
    print("  curl 'http://localhost:5770/requestlist?jwt=YOUR_TOKEN'")
    print("")
    print("  # Accept a friend request")
    print("  curl 'http://localhost:5770/accept?jwt=YOUR_TOKEN&uid=1234567890'")
    print("")
    print("  # Reject a friend request")
    print("  curl 'http://localhost:5770/reject?jwt=YOUR_TOKEN&uid=1234567890'")
    print("")
    print("  # Bulk accept")
    print("  curl -X POST http://localhost:5770/bulk_action \\")
    print("    -H 'Content-Type: application/json' \\")
    print("    -d '{\"jwt\":\"TOKEN\",\"action\":\"accept\",\"uids\":[123,456,789]}'")
    print("="*60)
    
    app.run(host='0.0.0.0', port=5770, debug=False)