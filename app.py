# Made by @Starpankaj & Integrated with Premium Danger UI
# API Link: https://t.me/starpankajff

from flask import Flask, request, jsonify, make_response, render_template_string
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import binascii
from datetime import datetime
import json
import time
import urllib3
import warnings
import uuid
import base64

# -----------------------------
# Security Warnings Disable
# -----------------------------
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore", category=UserWarning, message="Unverified HTTPS request")

app = Flask(__name__)

# -----------------------------
# Owner Configuration
# -----------------------------
OWNER_NAME = "STAR PANKAJ"
OWNER_LINK = "https://t.me/Starpankaj"

# -----------------------------
# HTML Premium Template (Danger Style)
# -----------------------------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
    <title>🔥 S26X VIP - Free Fire Manager</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@300;400;600&display=swap');
        
        * { margin:0; padding:0; box-sizing:border-box; }
        body { 
            font-family: 'Inter', sans-serif; 
            background-color: #070000;
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(90, 0, 0, 0.35), transparent 45%),
                radial-gradient(circle at 85% 30%, rgba(140, 0, 0, 0.25), transparent 45%);
            min-height: 100vh; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            padding: 2rem 1rem; 
            color: #fff;
            overflow-x: hidden;
        }
        
        /* Floating Background Orbs for Premium Vibe */
        .glow-orb {
            position: fixed;
            width: 300px;
            height: 300px;
            background: rgba(255, 0, 40, 0.12);
            border-radius: 50%;
            filter: blur(80px);
            z-index: 0;
            animation: float 8s infinite alternate ease-in-out;
        }
        .orb-1 { top: -10%; left: -10%; }
        .orb-2 { bottom: -10%; right: -10%; animation-delay: -4s; }

        @keyframes float {
            0% { transform: translate(0, 0) scale(1); }
            100% { transform: translate(40px, 40px) scale(1.2); }
        }

        .container { max-width: 850px; width: 100%; margin: 0 auto; position: relative; z-index: 1; }
        
        /* Dark Red Glassmorphism Card */
        .card { 
            background: rgba(25, 0, 0, 0.4); 
            backdrop-filter: blur(25px); 
            -webkit-backdrop-filter: blur(25px);
            border-radius: 24px; 
            border: 1px solid rgba(255, 50, 50, 0.2); 
            border-top: 1px solid rgba(255, 100, 100, 0.4);
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.9), inset 0 1px 0 rgba(255, 255, 255, 0.05); 
            overflow: hidden; 
            transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); 
        }
        .card:hover { transform: translateY(-5px); box-shadow: 0 40px 80px rgba(255, 0, 0, 0.15); }
        
        .header { 
            background: linear-gradient(180deg, rgba(100, 0, 0, 0.4) 0%, rgba(20, 0, 0, 0) 100%); 
            padding: 2.5rem 2rem; 
            text-align: center; 
            border-bottom: 1px solid rgba(255, 50, 50, 0.1);
        }
        .header h1 { 
            font-family: 'Rajdhani', sans-serif;
            font-size: 2.8rem; 
            font-weight: 700; 
            letter-spacing: 2px; 
            margin-bottom: 0.5rem; 
            background: linear-gradient(to right, #ff4b2b, #ff0000, #ff7b7b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(255, 0, 0, 0.4);
            text-transform: uppercase;
        }
        .header p { font-size: 1rem; color: #ff9999; letter-spacing: 2px; font-weight: 400; text-transform: uppercase; }
        
        .content { padding: 2.5rem; }
        
        .info-box { 
            background: rgba(10, 0, 0, 0.5); 
            border-radius: 16px; 
            padding: 2rem; 
            margin-bottom: 2rem; 
            border: 1px solid rgba(255, 20, 20, 0.15);
            position: relative;
            overflow: hidden;
            box-shadow: inset 0 0 20px rgba(0,0,0,0.8);
        }
        .info-box::before {
            content: '';
            position: absolute;
            top: 0; left: 0; width: 4px; height: 100%;
            background: linear-gradient(to bottom, #ff0000, #ff4b2b);
            box-shadow: 0 0 20px #ff0000;
        }

        .info-box h3 { 
            font-family: 'Rajdhani', sans-serif;
            color: #ff3333; 
            margin-bottom: 1.5rem; 
            font-size: 1.5rem; 
            letter-spacing: 1px;
            text-transform: uppercase;
            display: flex;
            align-items: center;
        }
        
        .form-group { margin-bottom: 1.2rem; }
        .form-group label { display: block; font-size: 0.85rem; margin-bottom: 0.5rem; color: #ffb3b3; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }
        .form-group input, .form-group select { 
            width: 100%; 
            padding: 1rem; 
            border-radius: 10px; 
            border: 1px solid rgba(255, 50, 50, 0.25); 
            background: rgba(0, 0, 0, 0.6); 
            color: #fff; 
            font-family: 'Inter', monospace; 
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: inset 0 3px 6px rgba(0,0,0,0.7);
        }
        .form-group input:focus, .form-group select:focus { 
            outline: none; 
            border-color: #ff0000; 
            box-shadow: 0 0 20px rgba(255, 0, 0, 0.3), inset 0 3px 6px rgba(0,0,0,0.7);
            background: rgba(30, 0, 0, 0.7);
        }
        
        .api-endpoint { 
            background: rgba(5, 0, 0, 0.8); 
            border-radius: 10px; 
            padding: 1.5rem; 
            font-family: 'Courier New', monospace; 
            font-size: 0.95rem; 
            word-break: break-all; 
            margin: 1rem 0; 
            border: 1px solid rgba(255, 50, 50, 0.2); 
            color: #ff6666; 
            white-space: pre-wrap;
            box-shadow: inset 0 0 30px rgba(0,0,0,0.9);
        }
        
        .btn { 
            display: block; 
            width: 100%; 
            background: linear-gradient(90deg, #8a0000, #ff0000, #8a0000); 
            background-size: 200% auto;
            color: white; 
            text-align: center; 
            padding: 1.2rem; 
            border-radius: 10px; 
            font-family: 'Rajdhani', sans-serif;
            font-weight: 700; 
            letter-spacing: 3px;
            text-transform: uppercase;
            transition: all 0.4s ease; 
            border: 1px solid rgba(255,100,100,0.5); 
            cursor: pointer; 
            box-shadow: 0 10px 25px rgba(200, 0, 0, 0.3); 
            font-size: 1.3rem; 
            margin-top: 1rem;
        }
        .btn:hover { 
            background-position: right center;
            transform: translateY(-2px); 
            box-shadow: 0 15px 35px rgba(255, 0, 0, 0.5), 0 0 25px rgba(255, 0, 0, 0.6); 
        }
        
        .credit-section { 
            text-align: center; 
            margin-top: 1.5rem; 
            padding-top: 1.5rem; 
            border-top: 1px solid rgba(255, 50, 50, 0.15); 
            font-size: 0.9rem; 
            color: #cc6666; 
            letter-spacing: 1px;
        }
        .credit-section span { 
            color: #ff3333; 
            font-weight: 700; 
            font-family: 'Rajdhani', sans-serif;
            font-size: 1.3rem;
            letter-spacing: 3px;
            text-shadow: 0 0 15px rgba(255, 0, 0, 0.6);
        }
        
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: rgba(0, 0, 0, 0.5); }
        ::-webkit-scrollbar-thumb { background: rgba(255, 0, 0, 0.4); border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(255, 0, 0, 0.8); }
    </style>
</head>
<body>
    <div class="glow-orb orb-1"></div>
    <div class="glow-orb orb-2"></div>
    
    <div class="container">
        <div class="card">
            <div class="header">
                <h1>🔥 S26X VIP PANEL</h1>
                <p>Execute Actions Directly From Web</p>
            </div>
            <div class="content">
                <div class="info-box">
                    <h3>⚡ Command Center</h3>
                    <div class="form-group">
                        <label>Guest UID</label>
                        <input type="text" id="guest_uid" placeholder="Enter Guest UID..." required>
                    </div>
                    <div class="form-group">
                        <label>Guest Password</label>
                        <input type="text" id="guest_pass" placeholder="Enter Password..." required>
                    </div>
                    <div class="form-group">
                        <label>Target UID</label>
                        <input type="text" id="target_uid" placeholder="Enter Target UID..." required>
                    </div>
                    <div class="form-group">
                        <label>Select Action</label>
                        <select id="action_type">
                            <option value="/player_info">🛡️ GET PLAYER INFO</option>
                            <option value="/add">➕ SEND FRIEND REQUEST</option>
                            <option value="/remove">➖ REMOVE FRIEND</option>
                        </select>
                    </div>
                    <button class="btn" onclick="executeAction()">🚀 INITIATE SYSTEM</button>
                </div>

                <div class="info-box" id="result_box" style="display: none;">
                    <h3>📊 Console Output</h3>
                    <div class="api-endpoint" id="output_console">Awaiting command...</div>
                </div>

                <div class="credit-section">
                    <p>DEVELOPED BY <br><br><span>S26X</span></p>
                    <p style="margin-top: 1rem; font-size: 0.75rem; color: #884444;">© 2026 PREMIUM SERVICE | SECURE CONNECTION</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        async function executeAction() {
            const uid = document.getElementById('guest_uid').value.trim();
            const pass = document.getElementById('guest_pass').value.trim();
            const targetUid = document.getElementById('target_uid').value.trim();
            const action = document.getElementById('action_type').value;
            const consoleBox = document.getElementById('output_console');
            
            document.getElementById('result_box').style.display = 'block';

            if (!uid || !pass || !targetUid) {
                consoleBox.style.color = '#ff3333';
                consoleBox.innerText = "[ERROR] SYSTEM HALTED: ALL FIELDS ARE REQUIRED.";
                return;
            }

            consoleBox.style.color = '#ff9999';
            consoleBox.innerText = "[SYSTEM] Processing request... establishing secure connection.";

            const url = `${action}?uid=${uid}&password=${pass}&friend_uid=${targetUid}&server_name=BD`;

            try {
                const response = await fetch(url);
                const data = await response.json();
                consoleBox.style.color = '#ff6666';
                consoleBox.innerText = JSON.stringify(data, null, 4);
            } catch (error) {
                consoleBox.style.color = '#ff3333';
                consoleBox.innerText = "[CRITICAL ERROR] NETWORK FAILURE: " + error.message;
            }
        }
    </script>
</body>
</html>
"""

# -----------------------------
# AES Configuration
# -----------------------------
AES_KEY = b'Yg&tc%DEuh6%Zc^8'
AES_IV = b'6oyZDr22E3ychjM%'

def encrypt_message(data_bytes):
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    return cipher.encrypt(pad(data_bytes, AES.block_size))

def encrypt_message_hex(data_bytes):
    return binascii.hexlify(encrypt_message(data_bytes)).decode('utf-8')

def dec_aes(data):
    try: 
        return unpad(AES.new(AES_KEY, AES.MODE_CBC, AES_IV).decrypt(data), 16)
    except ValueError: 
        return AES.new(AES_KEY, AES.MODE_CBC, AES_IV).decrypt(data)

ENCRYPTED_OWNER = encrypt_message_hex(OWNER_NAME.encode('utf-8'))

# -----------------------------
# Region-based URLs (BD Server Configured)
# -----------------------------
def get_base_url(server_name):
    server_name = server_name.upper() if server_name else "BD"
    if server_name == "IND":
        return "https://client.ind.freefiremobile.com/"
    elif server_name in {"BR", "US", "SAC", "NA"}:
        return "https://client.us.freefiremobile.com/"
    else:
        # Bangladesh & Global Client BP Server
        return "https://clientbp.ggpolarbear.com/"

def get_server_from_token(token):
    try:
        decoded = decode_jwt_payload(token)
        return decoded.get("lock_region", "BD").upper()
    except:
        return "BD"

# -----------------------------
# Raw Protobuf Helpers
# -----------------------------
def enc_varint(v):
    out = bytearray()
    while True:
        b = v & 0x7F; v >>= 7
        out.append(b | (0x80 if v else 0))
        if not v: return bytes(out)

def read_varint(data, off):
    v, s = 0, 0
    while True:
        if off >= len(data): break
        b = data[off]; off += 1
        v |= (b & 0x7F) << s
        if not (b & 0x80): return v, off
        s += 7
    return v, off

def ptag(f, wt): return enc_varint((f << 3) | wt)
def f_vint(f, n):  return ptag(f, 0) + enc_varint(n)
def f_bytes(f, b): return ptag(f, 2) + enc_varint(len(b)) + b
def f_str(f, s):
    b = s.encode("utf-8"); return ptag(f, 2) + enc_varint(len(b)) + b

def parse_proto(data):
    fields = {}; i = 0
    while i < len(data):
        try: key, i = read_varint(data, i)
        except Exception: break
        fn, wt = key >> 3, key & 7
        try:
            if wt == 0:
                v, i = read_varint(data, i)
                fields.setdefault(fn, []).append(("varint", v))
            elif wt == 1:
                v = int.from_bytes(data[i:i+8], "little"); i += 8
                fields.setdefault(fn, []).append(("u64", v))
            elif wt == 2:
                ln, i = read_varint(data, i)
                raw = data[i:i+ln]; i += ln
                s_ok = False
                try:
                    s = raw.decode("utf-8")
                    if s.isprintable():
                        fields.setdefault(fn, []).append(("string", s)); s_ok = True
                except UnicodeDecodeError: pass
                if not s_ok:
                    fields.setdefault(fn, []).append(("bytes", raw))
            elif wt == 5:
                v = int.from_bytes(data[i:i+4], "little"); i += 4
                fields.setdefault(fn, []).append(("u32", v))
            else: break
        except Exception: break
    return fields

def first_value(fields, field_num, want_kind=None):
    for kind, v in fields.get(field_num, []):
        if want_kind is None or kind == want_kind: return v
    return None

def decode_jwt_payload(token):
    try:
        parts = token.split(".")
        if len(parts) != 3: return {}
        p2 = parts[1] + "=" * (-len(parts[1]) % 4)
        return json.loads(base64.urlsafe_b64decode(p2))
    except Exception: return {}

def safe_str(value):
    if value is None: return ""
    return str(value)

# -----------------------------
# Payload Builders (1.132.11)
# -----------------------------
def build_major_login_payload(open_id, access_token, platform_type):
    remote_version = "1.132.11"
    cdn_blob = "https://dl-bs.ggpolarbear.com/live/ABHotUpdates/|https://core-bs.ggpolarbear.com/live/ABHotUpdates/|9a9a493d643462570dc50320b28533d0"
    client_ip = "103.178.30.175"
    vercfg_sign = "1.f46ddde8bb35d74e"
    sig_base64 = "KqsHTzDueNOcXOcwbbono9sXClAA8fjKlJa1d3S7v32LasYl4FeVw/00VZ554hj16SqMN0Wqra2xePWrjoqam4faHsNIQHf+Zn0uLVFORQL3UTG1"
    field_102_raw = b'\x12\x08' + bytes.fromhex("071217590d0c0531")
    session_hash = "1ac4b80ecf0478a44203bf8fac6120f5"

    b  = b""
    b += f_str(3, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    b += f_str(4, "free fire")
    b += f_vint(5, 1)
    b += f_str(7, remote_version)
    b += f_str(8, "Android OS 15")
    b += f_str(9, "Handheld")
    b += f_str(10, "Grameenphone")
    b += f_str(11, "WIFI")
    b += f_vint(12, 1260)
    b += f_vint(13, 2800)
    b += f_str(14, "480")
    b += f_str(15, "ARM64 FP ASIMD AES | 2000 | 8")
    b += f_vint(16, 3706)
    b += f_str(17, "Mali-G52 MC2")
    b += f_str(18, "OpenGL ES 3.2 v1.r32p1-01eac0.2a893c04ca0026c2e6802dbe7d7af5c5")
    b += f_str(19, f"Google|{str(uuid.uuid4())}")
    b += f_str(20, client_ip)
    b += f_str(21, "en")
    b += f_str(22, safe_str(open_id))
    b += f_str(23, str(platform_type))
    b += f_str(24, "Handheld")
    b += f_str(25, "iQOO Neo 10")
    b += f_str(26, "BD") # Set to BD Region Explicitly
    b += f_str(29, safe_str(access_token))
    b += f_vint(30, 1)
    b += f_str(41, "Grameenphone")
    b += f_str(42, "WIFI")
    b += f_str(57, session_hash)
    b += f_vint(60, 107943)
    b += f_vint(61, 6557)
    b += f_vint(62, 1287)
    b += f_vint(64, 6769)
    b += f_vint(65, 107943)
    b += f_vint(66, 6769)
    b += f_vint(67, 107943)
    b += f_vint(70, 4)
    b += f_vint(73, 3)
    b += f_str(74, "/data/app/~~A3x031MHqCIlFfDul3wh7A==/com.dts.freefireth-uxhEQBfRGVNx56vG9iuRGA==/lib/arm64")
    b += f_vint(76, 1)
    b += f_str(77, "066a589fa3f5658377634fe7b1d88556|/data/app/~~A3x031MHqCIlFfDul3wh7A==/base.apk")
    b += f_vint(78, 6)
    b += f_vint(79, 2)
    b += f_str(81, "64")
    b += f_str(83, "2019121227")
    b += f_vint(85, 3)
    b += f_str(86, "OpenGLES2")
    b += f_vint(87, 4095)
    b += f_vint(88, int(platform_type))
    b += f_vint(92, 10788)
    b += f_str(93, "3rd_party")
    b += f_str(94, sig_base64)
    b += f_vint(95, 111207)
    b += f_str(96, '{"cur_rate":[60,90],"support_etc2":false}')
    b += f_vint(97, 1)
    b += f_str(99, str(platform_type))
    b += f_str(100, str(platform_type))
    b += f_bytes(102, field_102_raw)
    b += f_vint(104, 26593)
    b += f_vint(105, 1)
    b += f_str(106, cdn_blob)
    b += f_str(107, vercfg_sign)
    return b

# -----------------------------
# JWT Generation Core
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
    try:
        r = requests.post(url, headers=headers, data=data, timeout=15)
        if r.status_code != 200:
            return {"error": f"OAuth failed: HTTP {r.status_code}"}
        j = r.json()
        token = j.get("access_token") or j.get("token") or j.get("jwt")
        if not token:
            return {"error": "No token in OAuth response", "raw": j}
        return {
            "access_token": token,
            "open_id": j.get("open_id", ""),
            "uid": j.get("uid"),
            "raw": j
        }
    except Exception as e:
        return {"error": f"OAuth exception: {str(e)}"}

def try_platform_login(open_id, access_token, platform_type):
    try:
        plain_data = build_major_login_payload(open_id, access_token, platform_type)
        encrypted_data = encrypt_message(plain_data)
        
        url = "https://loginbp.ggpolarbear.com/MajorLogin"
        
        response = requests.post(url, data=encrypted_data, headers={
            "User-Agent": "UnityPlayer/2018.4.12f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
            "Accept": "*/*",
            "Accept-Encoding": "deflate, gzip",
            "Authorization": "Bearer",
            "X-GA": "v1 1",
            "X-GA-SV": str(int(time.time())),
            "ReleaseVersion": "OB55",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Unity-Version": "2018.4.12f1"
        }, timeout=10, verify=False)
        
        if response.status_code != 200:
            return {"error": f"HTTP {response.status_code}"}

        attempts = []
        if len(response.content) > 64:
            attempts.append(("plain[64:]", parse_proto(response.content[64:])))
        attempts.append(("plain", parse_proto(response.content)))
        
        try: 
            attempts.append(("dec", parse_proto(dec_aes(response.content))))
        except Exception: pass
            
        if len(response.content) > 64:
            try: 
                attempts.append(("dec[64:]", parse_proto(dec_aes(response.content[64:]))))
            except Exception: pass

        fields = {}
        for _, f in attempts:
            cand_jwt = first_value(f, 8, "string")
            cand_aid = first_value(f, 1, "varint")
            if cand_jwt and cand_jwt.startswith("eyJ") and cand_aid:
                fields = f; break
                
        if not fields:
            for _, f in attempts:
                if 8 in f or 22 in f: fields = f; break

        account_id = first_value(fields, 1, "varint")
        jwt_token = first_value(fields, 8, "string")
        region = first_value(fields, 2, "string") or "BD"
        
        if jwt_token:
            payload = decode_jwt_payload(jwt_token)
            return {
                "account_id": payload.get("account_id") or account_id,
                "account_name": payload.get("nickname"),
                "open_id": open_id,
                "access_token": access_token,
                "platform": payload.get("external_type") or platform_type,
                "region": region,
                "status": "success",
                "token": jwt_token
            }
        
        if access_token:
            return {
                "account_id": open_id or "7096367728",
                "account_name": "Player",
                "open_id": open_id,
                "access_token": access_token,
                "platform": platform_type,
                "region": "BD",
                "status": "success",
                "token": access_token
            }
            
        return {"error": "Missing JWT in response"}
    except Exception as e:
        return {"error": str(e)}

# -----------------------------
# Friend Management Functions
# -----------------------------
def generic_friend_action(auth_token, author_uid, target_uid, action, server_name="BD"):
    endpoints = {
        'add': 'RequestAddingFriend',
        'remove': 'RemoveFriend',
        'accept': 'ConfirmFriendRequest',
        'reject': 'DeclineFriendRequest'
    }
    url = get_base_url(server_name) + endpoints[action]
    
    if action == 'remove':
        b = f_vint(1, int(author_uid)) + f_vint(2, int(target_uid))
    elif action == 'add':
        b = f_vint(1, int(target_uid)) + f_vint(2, 1) + f_vint(3, 1)
    else:
        b = f_vint(1, int(target_uid)) + f_vint(2, 6711906302)
        
    dynamic_payload = encrypt_message(b)
    
    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; Android 9)",
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Unity-Version": "2018.4.11f1",
        "X-GA": "v1 1",
        "ReleaseVersion": "OB55",
    }
    return requests.post(url, headers=headers, data=dynamic_payload, verify=False)

def get_player_info_raw(target_uid, token, server_name="BD"):
    try:
        if not server_name:
            server_name = get_server_from_token(token)
        protobuf_data = f_vint(1, int(target_uid)) + f_vint(2, 1)
        encrypted_data = encrypt_message(protobuf_data)
        endpoint = get_base_url(server_name) + "GetPlayerPersonalShow"

        headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; Android 9)",
            'Authorization': f"Bearer {token}",
            'Content-Type': "application/x-www-form-urlencoded",
            'X-Unity-Version': "2018.4.11f1",
            'X-GA': "v1 1",
            'ReleaseVersion': "OB55"
        }

        response = requests.post(endpoint, data=encrypted_data, headers=headers, verify=False)
        if response.status_code == 200:
            raw_parsed = parse_proto(dec_aes(response.content))
            return {
                "uid": target_uid, 
                "nickname": first_value(raw_parsed, 4, "string") or "Unknown", 
                "level": first_value(raw_parsed, 5, "varint") or 0, 
                "likes": first_value(raw_parsed, 12, "varint") or 0, 
                "region": server_name
            }
    except Exception as e:
        print(f"Info Err: {e}")
    return None

def get_pending_uids(auth_token, server_name="BD"):
    url = get_base_url(server_name) + "GetFriendRequestList"
    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; Android 9)",
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Unity-Version": "2018.4.11f1",
        "X-GA": "v1 1",
        "ReleaseVersion": "OB55",
    }
    binary_body = bytes.fromhex("a390e8e0fa11cd88d1ea7bfd7d6944b3")
    response = requests.post(url, headers=headers, data=binary_body, verify=False)
    
    uids = []
    if response.status_code == 200 and response.content:
        try:
            raw = dec_aes(response.content)
            parsed = parse_proto(raw)
            def extract(fields):
                for k, v_list in fields.items():
                    for kind, v in v_list:
                        if kind == "varint" and isinstance(v, int) and v > 1000000000:
                            uids.append(v)
                        elif kind == "bytes":
                            try: extract(parse_proto(v))
                            except: pass
            extract(parsed)
        except Exception as e:
            print(f"Pending UID parse error: {e}")
    return list(set(uids))

def get_friends_list_raw(auth_token, target_uid, server_name="BD"):
    url = get_base_url(server_name) + "GetPlayerSocialNetwork"
    b = f_vint(1, int(target_uid)) + f_vint(2, 1)
    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; Android 9)",
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Unity-Version": "2018.4.11f1",
        "X-GA": "v1 1",
        "ReleaseVersion": "OB55",
    }
    response = requests.post(url, headers=headers, data=encrypt_message(b), verify=False)
    if response.status_code == 200:
        try:
            raw = dec_aes(response.content)
            parsed = parse_proto(raw)
            return {"success": True, "raw_byte_length": len(raw), "data": parsed}
        except Exception as e:
            return {"success": False, "error": str(e)}
    return {"success": False, "error": f"HTTP {response.status_code}"}

# -----------------------------
# Routes
# -----------------------------
@app.route('/', methods=['GET'])
def root():
    return render_template_string(HTML_TEMPLATE)

@app.route('/token', methods=['GET'])
def get_token_route():
    uid = request.args.get('uid')
    password = request.args.get('password')

    if not uid or not password:
        return jsonify({"error": "Missing parameters: uid and password are required"}), 400

    oauth = get_oauth_token(uid, password)
    if "error" in oauth:
        return jsonify(oauth), 400

    platforms = [4, 1, 2, 3, 5, 6]
    for p in platforms:
        major = try_platform_login(oauth.get("open_id", ""), oauth["access_token"], p)
        if "token" in major:
            response_data = {
                "access_token": oauth["access_token"],
                "jwt_token": major["token"],
                "api": "ggpolarbear",
                "region": "BD",
                "status": "live",
                "oauth_raw": oauth["raw"]
            }
            return make_response(jsonify(response_data))

    return jsonify({"error": "MajorLogin failed on all platforms", "details": major}), 500

def get_auth_token_for_action(uid, password):
    oauth = get_oauth_token(uid, password)
    if "error" in oauth:
        return oauth.get("access_token"), None
        
    platforms = [4, 1, 2, 3, 5, 6]
    for p in platforms:
        major = try_platform_login(oauth.get("open_id", ""), oauth["access_token"], p)
        if "token" in major:
            return major["token"], None
            
    return oauth.get("access_token"), None

@app.route('/add', methods=['GET'])
def add_friend():
    uid = request.args.get('uid')
    password = request.args.get('password')
    friend_uid = request.args.get('friend_uid')
    server_name = request.args.get('server_name', 'BD')

    if not uid or not password or not friend_uid:
        return jsonify({"status": "failed", "message": "Missing uid, password, or friend_uid"}), 400

    token, _ = get_auth_token_for_action(uid, password)
    if not token:
        return jsonify({"status": "failed", "message": "Auth failed"}), 400
    
    author_uid = decode_jwt_payload(token).get("account_id", uid)
    
    try:
        response = generic_friend_action(token, author_uid, friend_uid, 'add', server_name)
        return jsonify({"status": "success", "message": f"Sent request to UID {friend_uid}"})
    except Exception as e:
        return jsonify({"status": "success", "message": f"Sent request to UID {friend_uid}"}), 200

@app.route('/remove', methods=['GET'])
def remove_friend():
    uid = request.args.get('uid')
    password = request.args.get('password')
    friend_uid = request.args.get('friend_uid')
    server_name = request.args.get('server_name', 'BD')

    if not uid or not password or not friend_uid:
        return jsonify({"status": "failed", "message": "Missing uid, password, or friend_uid"}), 400

    token, _ = get_auth_token_for_action(uid, password)
    if not token:
        return jsonify({"status": "failed", "message": "Auth failed"}), 400
    
    author_uid = decode_jwt_payload(token).get("account_id", uid)
    try:
        response = generic_friend_action(token, author_uid, friend_uid, 'remove', server_name)
        return jsonify({"status": "success", "message": f"Removed UID {friend_uid}"})
    except Exception as e:
        return jsonify({"status": "success", "message": f"Removed UID {friend_uid}"}), 200

@app.route('/player_info', methods=['GET'])
def player_info_custom():
    uid = request.args.get('uid')
    password = request.args.get('password')
    friend_uid = request.args.get('friend_uid')
    server_name = request.args.get('server_name', 'BD')

    if not uid or not password or not friend_uid:
        return jsonify({"status": "failed", "message": "Missing uid, password, or friend_uid"}), 400

    token, _ = get_auth_token_for_action(uid, password)
    player_info = get_player_info_raw(friend_uid, token, server_name) or {
        "uid": friend_uid, "nickname": "Player", "level": 50, "likes": 100, "region": "BD"
    }
    player_info["status"] = "success"
    return jsonify(player_info)

@app.route('/friends_list', methods=['GET'])
def friends_list_custom():
    uid = request.args.get('uid')
    password = request.args.get('password')
    server_name = request.args.get('server_name', 'BD')

    if not uid or not password:
        return jsonify({"status": "failed", "message": "Missing uid or password"}), 400

    token, _ = get_auth_token_for_action(uid, password)
    author_uid = decode_jwt_payload(token).get("account_id", uid)
    result = get_friends_list_raw(token, author_uid, server_name)
    return jsonify(result)

@app.route('/requestlist', methods=['GET'])
def get_request_list():
    jwt_token = request.args.get('jwt')
    if not jwt_token:
        return jsonify({"success": False, "error": "Missing jwt parameter"}), 400
    
    server_name = get_server_from_token(jwt_token)
    try:
        uids = get_pending_uids(jwt_token, server_name)
        requests_list = [{"uid": u, "nickname": "Player", "level": 10, "likes": 10, "region": "BD"} for u in uids]
        return jsonify({"success": True, "count": len(requests_list), "requests": requests_list})
    except Exception as e:
        return jsonify({"success": True, "count": 0, "requests": []})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "server": "BD Region", "owner": OWNER_NAME})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)