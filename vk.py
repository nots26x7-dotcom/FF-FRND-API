import sys
sys.path.append("/")

from flask import Flask, jsonify, request, make_response
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii
import my_pb2
import output_pb2

import os
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings("ignore", category=InsecureRequestWarning)

# -----------------------------
# AES Configuration
# -----------------------------
AES_KEY = b'Yg&tc%DEuh6%Zc^8'
AES_IV = b'6oyZDr22E3ychjM%'

app = Flask(__name__)

def encrypt_message(plaintext):
    """Encrypt with AES-CBC, PKCS7 padding"""
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    padded = pad(plaintext, AES.block_size)
    return cipher.encrypt(padded)

def encrypt_message_hex(plaintext):
    return binascii.hexlify(encrypt_message(plaintext)).decode()

# -----------------------------
# Step 1: OAuth Guest Login -> access_token + open_id
# -----------------------------
def get_oauth_token(uid, password):
    url = "https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant"
    headers = {
        "User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 9;en;US;)",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"
    }
    r = requests.post(url, headers=headers, data=data, timeout=15)
    if r.status_code != 200:
        return {"error": f"OAuth failed: HTTP {r.status_code}"}
    try:
        j = r.json()
    except:
        return {"error": "OAuth response not JSON", "raw": r.text}
    token = j.get("access_token") or j.get("token") or j.get("session_key") or j.get("jwt")
    if not token:
        return {"error": "No token in OAuth response"}
    return {
        "access_token": token,
        "open_id": j.get("open_id"),
        "uid": j.get("uid")
    }

# -----------------------------
# Step 2: MajorLogin (access_token + open_id) -> JWT token
# -----------------------------
def major_login(access_token, open_id=""):
    game_data = my_pb2.GameData()
    game_data.timestamp = "2024-12-05 18:15:32"
    game_data.game_name = "free fire"
    game_data.game_version = 1
    game_data.version_code = "1.123.2"
    game_data.os_info = "Android OS 9 / API-28 (PI/rel.cjw.20220518.114133)"
    game_data.device_type = "Handheld"
    game_data.network_provider = "Verizon Wireless"
    game_data.connection_type = "WIFI"
    game_data.screen_width = 1280
    game_data.screen_height = 960
    game_data.dpi = "240"
    game_data.cpu_info = "ARMv7 VFPv3 NEON VMH | 2400 | 4"
    game_data.total_ram = 5951
    game_data.gpu_name = "Adreno (TM) 640"
    game_data.gpu_version = "OpenGL ES 3.0"
    game_data.user_id = "Google|74b585a9-0268-4ad3-8f36-ef41d2e53610"
    game_data.ip_address = "172.190.111.97"
    game_data.language = "en"
    game_data.open_id = open_id
    game_data.access_token = access_token
    game_data.platform_type = 4
    game_data.device_form_factor = "Handheld"
    game_data.device_model = "Asus ASUS_I005DA"
    game_data.field_60 = 32968
    game_data.field_61 = 29815
    game_data.field_62 = 2479
    game_data.field_63 = 914
    game_data.field_64 = 31213
    game_data.field_65 = 32968
    game_data.field_66 = 31213
    game_data.field_67 = 32968
    game_data.field_70 = 4
    game_data.field_73 = 2
    game_data.library_path = "/data/app/com.dts.freefireth-QPvBnTUhYWE-7DMZSOGdmA==/lib/arm"
    game_data.field_76 = 1
    game_data.apk_info = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-QPvBnTUhYWE-7DMZSOGdmA==/base.apk"
    game_data.field_78 = 6
    game_data.field_79 = 1
    game_data.os_architecture = "32"
    game_data.build_number = "2019117877"
    game_data.field_85 = 1
    game_data.graphics_backend = "OpenGLES2"
    game_data.max_texture_units = 16383
    game_data.rendering_api = 4
    game_data.encoded_field_89 = "\u0017T\u0011\u0017\u0002\b\u000eUMQ\bEZ\u0003@ZK;Z\u0002\u000eV\ri[QVi\u0003\ro\t\u0007e"
    game_data.field_92 = 9204
    game_data.marketplace = "3rd_party"
    game_data.encryption_key = "KqsHT2B4It60T/65PGR5PXwFxQkVjGNi+IMCK3CFBCBfrNpSUA1dZnjaT3HcYchlIFFL1ZJOg0cnulKCPGD3C3h1eFQ="
    game_data.total_storage = 111107
    game_data.field_97 = 1
    game_data.field_98 = 1
    game_data.field_99 = "4"
    game_data.field_100 = "4"

    serialized = game_data.SerializeToString()
    encrypted = encrypt_message(serialized)

    url = "https://loginbp.ggblueshark.com/MajorLogin"
    headers = {
        'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/octet-stream",
        'Expect': "100-continue",
        'X-GA': "v1 1",
        'X-Unity-Version': "2018.4.11f1",
        'ReleaseVersion': "OB53"
    }
    try:
        resp = requests.post(url, data=encrypted, headers=headers, verify=False, timeout=15)
        if resp.status_code != 200:
            return {"error": f"MajorLogin HTTP {resp.status_code}"}
        msg = output_pb2.Garena_420()
        msg.ParseFromString(resp.content)
        # Extract token from protobuf (field number may vary, but we know it's there)
        token = None
        if hasattr(msg, 'token') and msg.token:
            token = msg.token
        else:
            # Fallback: parse as string (last resort)
            text = str(msg)
            for line in text.split('\n'):
                if 'token:' in line:
                    token = line.split(':', 1)[1].strip().strip('"')
                    break
        if token:
            return {"token": token}
        return {"error": "No token in MajorLogin response"}
    except Exception as e:
        return {"error": f"MajorLogin exception: {str(e)}"}

# -----------------------------
# Step 3: Build dynamic GetFriend request (protobuf with user's UID)
# -----------------------------
def encode_varint(value):
    """Encode an integer as protobuf varint"""
    result = []
    while value > 0x7F:
        result.append((value & 0x7F) | 0x80)
        value >>= 7
    result.append(value)
    return bytes(result)

def create_friend_request_payload(uid):
    """
    Creates a protobuf message for GetFriend.
    Field 1 (wire type 0, varint) = uid
    """
    # field number 1, wire type 0 -> (1<<3)|0 = 0x08
    return bytes([0x08]) + encode_varint(int(uid))

# -----------------------------
# Step 4: Call GetFriend endpoint
# -----------------------------
def get_friends_from_token(jwt_token, uid):
    """Send encrypted GetFriend request and parse response"""
    # Build dynamic payload
    plain_payload = create_friend_request_payload(uid)
    encrypted_payload = encrypt_message(plain_payload)

    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "UnityPlayer/2022.3.47f1",
        "ReleaseVersion": "OB53",
        "X-Unity-Version": "2022.3.47f1",
        "X-GA": "v1 1"
    }
    try:
        response = requests.post(
            "https://client.ind.freefiremobile.com/GetFriend",
            headers=headers,
            data=encrypted_payload,
            timeout=15,
            verify=False
        )
        if response.status_code != 200:
            return {"success": False, "error": f"GetFriend HTTP {response.status_code}"}

        raw = response.content
        # Parse protobuf response manually (simple field extraction)
        friends = []
        pos = 0
        data = raw
        while pos < len(data):
            # Read field header
            if pos >= len(data):
                break
            header = data[pos]
            pos += 1
            field_num = header >> 3
            wire_type = header & 0x07
            if wire_type == 0:  # varint
                val = 0
                shift = 0
                while True:
                    if pos >= len(data):
                        break
                    b = data[pos]
                    pos += 1
                    val |= (b & 0x7F) << shift
                    if not (b & 0x80):
                        break
                    shift += 7
                if field_num == 1:  # repeated friend list
                    # This varint is the length of a nested message, skip for now
                    pass
            elif wire_type == 2:  # length-delimited (string or nested message)
                # read length
                length = 0
                shift = 0
                while True:
                    if pos >= len(data):
                        break
                    b = data[pos]
                    pos += 1
                    length |= (b & 0x7F) << shift
                    if not (b & 0x80):
                        break
                    shift += 7
                chunk = data[pos:pos+length]
                pos += length
                # Try to parse chunk as a nested friend message
                friend_info = {}
                subpos = 0
                while subpos < len(chunk):
                    if subpos >= len(chunk):
                        break
                    subhead = chunk[subpos]
                    subpos += 1
                    subfield = subhead >> 3
                    subwire = subhead & 0x07
                    if subwire == 0:  # varint
                        v = 0
                        s = 0
                        while True:
                            if subpos >= len(chunk):
                                break
                            b = chunk[subpos]
                            subpos += 1
                            v |= (b & 0x7F) << s
                            if not (b & 0x80):
                                break
                            s += 7
                        if subfield == 1:
                            friend_info['uid'] = str(v)
                    elif subwire == 2:  # string
                        l = 0
                        s = 0
                        while True:
                            if subpos >= len(chunk):
                                break
                            b = chunk[subpos]
                            subpos += 1
                            l |= (b & 0x7F) << s
                            if not (b & 0x80):
                                break
                            s += 7
                        str_val = chunk[subpos:subpos+l].decode('utf-8', errors='ignore')
                        subpos += l
                        if subfield == 3:
                            friend_info['nickname'] = str_val
                if friend_info:
                    friends.append(friend_info)
        return {"success": True, "friends_count": len(friends), "friends_list": friends}
    except Exception as e:
        return {"success": False, "error": str(e)}

# -----------------------------
# Flask Endpoints
# -----------------------------
@app.route('/token', methods=['GET'])
def get_token_response():
    """Original endpoint: UID + Password -> JWT token"""
    uid = request.args.get('uid')
    password = request.args.get('password')
    if not uid or not password:
        return jsonify({"error": "Missing uid and password"}), 400

    oauth = get_oauth_token(uid, password)
    if "error" in oauth:
        return jsonify(oauth), 400

    major = major_login(oauth["access_token"], oauth.get("open_id", ""))
    if "error" in major:
        return jsonify(major), 500

    return jsonify({
        "token": major["token"],
        "oauth_raw": oauth,
        "status": "live"
    })

@app.route('/friend', methods=['GET'])
def get_friends():
    """
    Get friend list using one of three methods:
    1. ?uid=UID&pass=PASSWORD
    2. ?access=ACCESS_TOKEN&open_id=OPEN_ID
    3. ?jwt=JWT_TOKEN&uid=UID   (uid is required for building the request)
    """
    uid = request.args.get('uid')
    password = request.args.get('pass')
    access_token = request.args.get('access')
    open_id = request.args.get('open_id')
    jwt_token = request.args.get('jwt')

    method = None
    final_jwt = None
    user_uid = None

    # Method 1: UID + Password
    if uid and password:
        method = "UID_PASS"
        oauth = get_oauth_token(uid, password)
        if "error" in oauth:
            return jsonify({"success": False, "error": oauth["error"]}), 401
        major = major_login(oauth["access_token"], oauth.get("open_id", ""))
        if "error" in major:
            return jsonify({"success": False, "error": major["error"]}), 401
        final_jwt = major["token"]
        user_uid = uid

    # Method 2: Access Token + Open ID
    elif access_token:
        if not open_id:
            return jsonify({
                "success": False,
                "error": "Missing open_id parameter. Usage: ?access=TOKEN&open_id=OPEN_ID"
            }), 400
        method = "ACCESS_TOKEN"
        major = major_login(access_token, open_id)
        if "error" in major:
            return jsonify({"success": False, "error": major["error"]}), 401
        final_jwt = major["token"]
        # We still need the UID to build the friend request. Try to extract from JWT.
        try:
            import jwt as pyjwt
            decoded = pyjwt.decode(final_jwt, options={"verify_signature": False})
            user_uid = decoded.get("account_id") or decoded.get("sub")
        except:
            return jsonify({"success": False, "error": "Could not extract UID from JWT, please provide uid parameter"}), 400
        if not user_uid:
            return jsonify({"success": False, "error": "UID not found in JWT, pass uid parameter"}), 400

    # Method 3: Direct JWT
    elif jwt_token:
        if not uid:
            return jsonify({"success": False, "error": "Missing uid parameter for JWT method"}), 400
        method = "JWT_TOKEN"
        final_jwt = jwt_token
        user_uid = uid
    else:
        return jsonify({
            "success": False,
            "error": "Missing parameters. Use ?uid=UID&pass=PASS or ?access=TOKEN&open_id=OPEN_ID or ?jwt=JWT&uid=UID"
        }), 400

    # Now get friends
    result = get_friends_from_token(final_jwt, user_uid)
    result["method"] = method
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)