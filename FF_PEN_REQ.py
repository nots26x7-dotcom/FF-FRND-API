from flask import Flask, request, jsonify, render_template_string
import requests
import urllib3
from protobuf_decoder.protobuf_decoder import Parser

app = Flask(__name__)
urllib3.disable_warnings()

# ========== HTML WEBSITE (PREMIUM DESIGN) ==========
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title>Free Fire Friend Request API | Premium Service</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Poppins', 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 2rem 1rem;
        }

        .container {
            max-width: 900px;
            width: 100%;
            margin: 0 auto;
        }

        .card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 25px 45px -12px rgba(0, 0, 0, 0.5);
            overflow: hidden;
            transition: transform 0.3s ease;
        }

        .card:hover {
            transform: translateY(-5px);
        }

        .header {
            background: linear-gradient(120deg, #ff416c, #ff4b2b);
            padding: 2rem;
            text-align: center;
            color: white;
        }

        .header h1 {
            font-size: 2.2rem;
            font-weight: 700;
            letter-spacing: -0.5px;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }

        .header p {
            font-size: 1rem;
            opacity: 0.9;
        }

        .content {
            padding: 2rem;
        }

        .info-box {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 1.5rem;
            padding: 1.5rem;
            margin-bottom: 2rem;
            border-left: 4px solid #ff4b2b;
        }

        .info-box h3 {
            color: #ffb347;
            margin-bottom: 0.75rem;
            font-size: 1.3rem;
        }

        .api-endpoint {
            background: #0f172a;
            border-radius: 1rem;
            padding: 1rem;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            word-break: break-all;
            margin: 1rem 0;
            border: 1px solid #334155;
            color: #a5f3fc;
        }

        .btn {
            display: inline-block;
            background: linear-gradient(90deg, #ff416c, #ff4b2b);
            color: white;
            text-decoration: none;
            padding: 0.8rem 1.8rem;
            border-radius: 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
            margin: 0.5rem 0.5rem 0.5rem 0;
            border: none;
            cursor: pointer;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        }

        .btn:hover {
            transform: scale(1.02);
            box-shadow: 0 6px 15px rgba(0,0,0,0.3);
            filter: brightness(1.05);
        }

        .telegram-link {
            background: #0088cc;
            background: linear-gradient(90deg, #0088cc, #00aaff);
        }

        .credit-section {
            text-align: center;
            margin-top: 2rem;
            padding-top: 1.5rem;
            border-top: 1px solid rgba(255,255,255,0.1);
            font-size: 0.9rem;
            color: #cbd5e1;
        }

        .credit-section a {
            color: #ffb347;
            text-decoration: none;
            font-weight: 600;
        }

        .credit-section a:hover {
            text-decoration: underline;
        }

        .feature-list {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            margin: 1.5rem 0;
        }

        .feature {
            flex: 1;
            min-width: 150px;
            background: rgba(255,255,255,0.03);
            padding: 1rem;
            border-radius: 1rem;
            text-align: center;
        }

        .feature span {
            font-size: 2rem;
            display: block;
            margin-bottom: 0.5rem;
        }

        @media (max-width: 600px) {
            .header h1 { font-size: 1.6rem; }
            .content { padding: 1.5rem; }
            .btn { padding: 0.6rem 1.2rem; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <div class="header">
                <h1>🔥 FREE FIRE FRIEND REQUEST API</h1>
                <p>Get pending friend requests with player details</p>
            </div>
            <div class="content">
                <div class="info-box">
                    <h3>📌 API Endpoint</h3>
                    <div class="api-endpoint">
                        GET /requestlist?jwt=YOUR_TOKEN
                    </div>
                    <p style="margin-top: 0.5rem;">Returns JSON with pending friend requests including UID, name, level, likes, region & ban status.</p>
                </div>

                <div class="info-box">
                    <h3>⭐ Features</h3>
                    <div class="feature-list">
                        <div class="feature"><span>📋</span> Fetch Pending UIDs</div>
                        <div class="feature"><span>👤</span> Player Info (bbytop API)</div>
                        <div class="feature"><span>🚫</span> Ban Status Check</div>
                        <div class="feature"><span>⚡</span> Fast & Reliable</div>
                    </div>
                </div>

                <div style="text-align: center; margin: 1.5rem 0;">
                    <a href="https://t.me/vkboyx77" target="_blank" class="btn telegram-link">
                        📱 Contact Owner on Telegram
                    </a>
                    <a href="https://t.me/VK_FF_SHADOW" target="_blank" class="btn telegram-link">
                        📢 Join Telegram Channel
                    </a>
                </div>

                <div class="credit-section">
                    <p>✨ <strong>CREDIT</strong> : @BBYTOP12 ✨</p>
                    <p>💎 Developed with ❤️ by <a href="https://t.me/vkboyx77" target="_blank">VKBOYX77</a></p>
                    <p style="margin-top: 0.5rem; font-size: 0.75rem;">© 2025 Premium Service | All rights reserved</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

# ========== CORE FUNCTIONS (unchanged from original) ==========
def get_pending_uids(auth_token):
    """Extract pending friend request UIDs"""
    url = "https://client.ind.freefiremobile.com/GetFriendRequestList"
    headers = {
        "Host": "client.ind.freefiremobile.com",
        "User-Agent": "UnityPlayer/2022.3.47f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-GA": "v1 1",
        "ReleaseVersion": "OB53",
    }
    binary_body = bytes.fromhex("a390e8e0fa11cd88d1ea7bfd7d6944b3")
    response = requests.post(url, headers=headers, data=binary_body, verify=False)
    
    uids = []
    if len(response.content) > 0:
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
    except:
        return None

# ========== ROUTES ==========
@app.route('/')
def premium_website():
    """Premium landing page with credits and Telegram links"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/requestlist', methods=['GET'])
def get_request_list():
    """API: Get pending friend requests list"""
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

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "ok",
        "service": "Free Fire Friend Request API",
        "endpoints": ["/", "/requestlist?jwt=TOKEN", "/health"]
    })

# ========== RUN SERVER ==========
if __name__ == "__main__":
    print("="*50)
    print("🔥 FREE FIRE FRIEND REQUEST API (PREMIUM EDITION)")
    print("="*50)
    print("✅ Credits: @BBYTOP12 | Telegram: @vkboyx77")
    print("✅ Channel: https://t.me/VK_FF_SHADOW")
    print("")
    print("🌐 Website: http://0.0.0.0:5000/")
    print("📡 API: http://0.0.0.0:5000/requestlist?jwt=TOKEN")
    print("❤️ Health: http://0.0.0.0:5000/health")
    print("="*50)
    app.run(host='0.0.0.0', port=5000, debug=False)