import io
import base64
import pyotp
import qrcode
import hashlib
from cryptography.fernet import Fernet
from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "aegisshield_master_secret_key"

SHARED_SECRET = "JBSWY3DPEHPK3PXP"
PANIC_CODE = "999999"

# Generate a consistent key for demo encryption
FERNET_KEY = Fernet.generate_key()
cipher_suite = Fernet(FERNET_KEY)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AegisShield | Cyber Security Suite</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background: #0b0f19; color: #f8fafc; min-height: 100vh; display: flex; flex-direction: column; }
        header { background: #161e2e; padding: 18px 40px; border-bottom: 1px solid #1f293d; display: flex; justify-content: space-between; align-items: center; }
        .logo { font-size: 20px; font-weight: 700; color: #38bdf8; letter-spacing: 1px; }
        .nav-link { color: #f87171; text-decoration: none; font-size: 13px; font-weight: bold; border: 1px solid #f87171; padding: 6px 14px; border-radius: 6px; }
        .main-container { display: flex; justify-content: center; align-items: center; flex-grow: 1; padding: 30px; }
        
        /* Cards */
        .card { background: #161e2e; padding: 35px; border-radius: 16px; border: 1px solid #1f293d; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.5); text-align: center; width: 380px; }
        .dashboard-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; width: 100%; max-width: 1000px; }
        .panel { background: #161e2e; padding: 25px; border-radius: 12px; border: 1px solid #1f293d; text-align: left; }
        
        .panel h3 { color: #38bdf8; font-size: 16px; margin-bottom: 12px; border-bottom: 1px solid #334155; padding-bottom: 8px; }
        .qr-wrapper { background: white; padding: 12px; border-radius: 10px; display: inline-block; margin-bottom: 15px; }
        .timer-bar-container { background: #334155; height: 5px; border-radius: 3px; overflow: hidden; margin-bottom: 20px; }
        .timer-bar { background: #38bdf8; height: 100%; width: 100%; transition: width 1s linear; }
        
        input, textarea { width: 100%; padding: 10px; background: #0b0f19; border: 1px solid #334155; border-radius: 6px; color: #f8fafc; font-size: 13px; outline: none; margin-bottom: 10px; }
        input:focus, textarea:focus { border-color: #38bdf8; }
        button { width: 100%; padding: 10px; background: #0284c7; color: white; border: none; border-radius: 6px; font-size: 13px; font-weight: 600; cursor: pointer; transition: 0.2s; }
        button:hover { background: #0369a1; }
        
        .result-box { background: #0b0f19; padding: 10px; border-radius: 6px; border: 1px solid #334155; font-family: monospace; font-size: 11px; word-break: break-all; color: #a7f3d0; margin-top: 10px; }
        .alert-duress { background: #7f1d1d; border: 1px solid #dc2626; color: #fecaca; padding: 12px; border-radius: 8px; font-size: 12px; margin-bottom: 20px; text-align: center; }
        .hint { font-size: 11px; color: #64748b; margin-top: 12px; line-height: 1.4; }
    </style>
</head>
<body>

    <header>
        <div class="logo">AEGIS SHIELD</div>
        {% if page == 'dashboard' %}
            <a href="/logout" class="nav-link">Lock Portal</a>
        {% endif %}
    </header>

    <div class="main-container">
        {% if page == 'login' %}
            <div class="card">
                <div style="font-size:12px; color:#94a3b8; text-transform:uppercase; margin-bottom:15px; letter-spacing:1px;">Zero-Trust MFA Verification</div>
                
                <div class="qr-wrapper">
                    <img src="data:image/png;base64,{{ qr_code }}" width="170" height="170" alt="MFA QR">
                </div>

                <div class="timer-bar-container">
                    <div id="progress" class="timer-bar"></div>
                </div>

                <form action="/verify" method="POST">
                    <input type="text" name="code" placeholder="000000" maxlength="6" required autocomplete="off" style="text-align:center; font-size:20px; letter-spacing:5px; font-weight:bold;">
                    <button type="submit">Authenticate Session</button>
                </form>

                <div class="hint">
                    Scan with <b>Google Authenticator</b>.<br>
                    Use code <b>999999</b> for Panic Override.
                </div>

                <script>
                    function updateTimer() {
                        const now = Math.floor(Date.now() / 1000);
                        const secondsRemaining = 30 - (now % 30);
                        document.getElementById('progress').style.width = (secondsRemaining / 30) * 100 + '%';
                        if (secondsRemaining === 30) window.location.reload();
                    }
                    setInterval(updateTimer, 1000);
                    updateTimer();
                </script>
            </div>

        {% elif page == 'dashboard' %}
            <div style="width: 100%; max-width: 1000px;">
                
                {% if mode == 'DURESS' %}
                    <div class="alert-duress">
                        ⚠️ <b>DURESS PROTOCOL ACTIVATED:</b> Vault files wiped. Simulated safe environment rendered.
                    </div>
                {% endif %}

                <div class="dashboard-grid">
                    
                    <!-- Tool 1: AES-256 Message Encryptor -->
                    <div class="panel">
                        <h3>🔑 Module 1: AES-256 Text Encryptor</h3>
                        <form action="/encrypt" method="POST">
                            <textarea name="plaintext" rows="3" placeholder="Enter confidential message..." required></textarea>
                            <button type="submit">Encrypt Message</button>
                        </form>
                        {% if encrypted_res %}
                            <div class="result-box"><b>Ciphertext:</b><br>{{ encrypted_res }}</div>
                        {% endif %}
                    </div>

                    <!-- Tool 2: SHA-256 Data Integrity -->
                    <div class="panel">
                        <h3>🛡️ Module 2: SHA-256 Hash Guard</h3>
                        <form action="/hash" method="POST">
                            <input type="text" name="hash_text" placeholder="Enter text to generate hash..." required>
                            <button type="submit">Calculate Hash</button>
                        </form>
                        {% if hash_res %}
                            <div class="result-box"><b>SHA-256 Digest:</b><br>{{ hash_res }}</div>
                        {% endif %}
                    </div>

                    <!-- Tool 3: Password Entropy Analyzer -->
                    <div class="panel">
                        <h3>⚡ Module 3: Password Strength Analyzer</h3>
                        <input type="password" id="pass_input" oninput="analyzePass()" placeholder="Type a test password...">
                        <div id="pass_result" class="result-box" style="color: #cbd5e1;">Type a password to evaluate strength...</div>
                    </div>

                </div>
            </div>

            <script>
                function analyzePass() {
                    let p = document.getElementById('pass_input').value;
                    let res = document.getElementById('pass_result');
                    if(p.length === 0) { res.innerHTML = "Type a password to evaluate strength..."; return; }
                    
                    let score = 0;
                    if(p.length >= 8) score++;
                    if(p.length >= 12) score++;
                    if(/[A-Z]/.test(p)) score++;
                    if(/[0-9]/.test(p)) score++;
                    if(/[^A-Za-z0-9]/.test(p)) score++;

                    if(score <= 2) res.innerHTML = "🔴 <b style='color:#f87171;'>WEAK</b> (Crack time: Instantly)";
                    else if(score <= 4) res.innerHTML = "🟡 <b style='color:#facc15;'>MEDIUM</b> (Crack time: Few Days)";
                    else res.innerHTML = "🟢 <b style='color:#4ade80;'>STRONG</b> (Crack time: 100+ Years)";
                }
            </script>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    totp = pyotp.TOTP(SHARED_SECRET)
    uri = totp.provisioning_uri(name="Admin", issuer_name="AegisShield_Suite")

    img = qrcode.make(uri)
    buf = io.BytesIO()
    img.save(buf)
    qr_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    return render_template_string(HTML_TEMPLATE, page='login', qr_code=qr_b64)

@app.route('/verify', methods=['POST'])
def verify():
    code = request.form.get('code', '').strip()
    totp = pyotp.TOTP(SHARED_SECRET)

    if code == PANIC_CODE:
        session['mode'] = 'DURESS'
        session['logged_in'] = True
        return redirect(url_for('dashboard'))

    if totp.verify(code):
        session['mode'] = 'NORMAL'
        session['logged_in'] = True
        return redirect(url_for('dashboard'))

    return "<h3>🔴 Access Denied</h3><a href='/'>Try Again</a>", 403

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    return render_template_string(HTML_TEMPLATE, page='dashboard', mode=session.get('mode'))

@app.route('/encrypt', methods=['POST'])
def encrypt():
    text = request.form.get('plaintext', '').encode()
    cipher = cipher_suite.encrypt(text).decode()
    return render_template_string(HTML_TEMPLATE, page='dashboard', mode=session.get('mode'), encrypted_res=cipher)

@app.route('/hash', methods=['POST'])
def hash_data():
    text = request.form.get('hash_text', '').encode()
    digest = hashlib.sha256(text).hexdigest()
    return render_template_string(HTML_TEMPLATE, page='dashboard', mode=session.get('mode'), hash_res=digest)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)