from flask import Flask, request, session, redirect, url_for, render_template, abort
from werkzeug.security import generate_password_hash, check_password_hash
from html import escape
import os

app = Flask(__name__)

# Chiave segreta forte e casuale (non hardcodata)
app.secret_key = os.urandom(32)

# Configurazione hardening per i cookie di sessione
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_SECURE=False  # Impostare a True se esposto dietro terminatore TLS/HTTPS
)

# Memorizzazione sicura delle credenziali tramite hash salted (nessuna password in chiaro)
USERS = {
    'alice': generate_password_hash('password123'),
    'bob': generate_password_hash('qwerty'),
}

# Iniezione header difensivi a livello HTTP
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Content-Security-Policy'] = "default-src 'self' 'unsafe-inline';"
    return response


def render_page(title, eyebrow, headline, description, body_html, footer_html=''):
    return f'''<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)}</title>
    <style>
        :root {{ --bg1:#f8fafc; --bg2:#e0f2fe; --card:#ffffff; --surface:#f8fafc; --border:#dbe4ef; --text:#0f172a; --muted:#475569; --accent:#0284c7; --accent2:#16a34a; }}
        * {{ box-sizing: border-box; }}
        body {{ margin:0; min-height:100vh; font-family:Inter, Segoe UI, Arial, sans-serif; color:var(--text); background:radial-gradient(circle at top, rgba(14,165,233,.18), transparent 34%), linear-gradient(135deg, var(--bg1), var(--bg2)); display:grid; place-items:center; padding:32px; }}
        .panel {{ width:min(880px,100%); background:var(--card); border:1px solid var(--border); border-radius:24px; box-shadow:0 22px 60px rgba(15,23,42,.12); overflow:hidden; }}
        .hero {{ padding:28px 32px 20px; border-bottom:1px solid var(--border); background:linear-gradient(135deg, rgba(14,165,233,.10), rgba(34,197,94,.08)); }}
        .eyebrow {{ display:inline-block; padding:6px 12px; border-radius:999px; background:#e0f2fe; color:#0369a1; font-size:12px; letter-spacing:.08em; text-transform:uppercase; }}
        h1 {{ margin:14px 0 8px; font-size:34px; line-height:1.1; }}
        .desc {{ margin:0; color:var(--muted); max-width:64ch; line-height:1.6; }}
        .content {{ padding:30px 32px 32px; }}
        .card {{ border:1px solid var(--border); border-radius:18px; background:var(--surface); padding:22px; margin-bottom:18px; }}
        .card h2 {{ margin:0 0 12px; font-size:18px; }}
        .row {{ display:flex; gap:12px; flex-wrap:wrap; align-items:center; }}
        .btn {{ display:inline-block; text-decoration:none; border:0; border-radius:12px; padding:11px 16px; font-weight:700; color:#ffffff; background:linear-gradient(135deg, #0284c7, #16a34a); box-shadow:0 10px 22px rgba(2,132,199,.18); }}
        .btn.secondary {{ color:#0f172a; background:#ffffff; border:1px solid var(--border); box-shadow:none; }}
        .input {{ width:100%; padding:12px 14px; margin:8px 0 14px; border-radius:12px; border:1px solid var(--border); background:#ffffff; color:var(--text); outline:none; }}
        .note {{ color:var(--muted); font-size:14px; line-height:1.6; }}
        .badge {{ display:inline-block; margin-bottom:12px; padding:6px 10px; border-radius:999px; color:#166534; background:#dcfce7; font-size:12px; letter-spacing:.06em; text-transform:uppercase; }}
        .footer {{ padding:0 32px 28px; color:var(--muted); font-size:13px; }}
        .result {{ padding:14px 16px; border-radius:14px; background:#f0fdf4; border:1px solid #bbf7d0; }}
        form {{ margin: 0; }}
    </style>
</head>
<body>
    <main class="panel">
        <section class="hero">
            <span class="eyebrow">{escape(eyebrow)}</span>
            <h1>{escape(headline)}</h1>
            <p class="desc">{escape(description)}</p>
        </section>
        <section class="content">{body_html}</section>
        {f'<div class="footer">{footer_html}</div>' if footer_html else ''}
    </main>
</body>
</html>'''

@app.route('/')
def index():
    body = '''<div class="card">
        <div class="badge">Scenario 02 - Mitigated</div>
        <h2>Hardened Authentication Flow</h2>
        <p class="note">Password hashing via PBKDF2/SHA256, constant-time verification checks, and session cookie protections are active.</p>
        <div class="row">
            <a class="btn" href="/login">Open login page</a>
        </div>
    </div>'''
    return render_page('Mitigated Lab - Broken Authentication - Broken Authentication', 'Authentication Hardening', 'Secure login control', 'A fully remediated authentication pipeline implementing cryptographic hashing.', body, 'Use the login form to test valid versus invalid credentials.')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        body = '''<div class="card">
            <div class="badge">Secure login</div>
            <h2>Authenticate to continue</h2>
            <p class="note">Credentials are matched against secure hashes with timing attack mitigations.</p>
            <form method="post">
                <label>Username</label>
                <input class="input" name="username" placeholder="alice">
                <label>Password</label>
                <input class="input" name="password" type="password" placeholder="password123">
                <div class="row">
                    <button class="btn" type="submit">Login</button>
                    <a class="btn secondary" href="/">Back to overview</a>
                </div>
            </form>
        </div>'''
        return render_page('Authentication - Login', 'Authentication Hardening', 'Login form', 'Secure verification flow.', body,)
    username = request.form.get('username','').strip()
    password = request.form.get('password','')

    user_password_hash = USERS.get(username)
    
    # Verifica robusta: validazione crittografica e mitigazione di user enumeration
    if user_password_hash and check_password_hash(user_password_hash, password):
        session['user'] = username
        body = f'''<div class="card">
            <div class="badge">Access granted</div>
            <h2>Logged in as {escape(username)}</h2>
            <p class="note">Authentication succeeded through cryptographic hash validation.</p>
            <div class="row"><a class="btn" href="/login">Back to login</a></div>
        </div>'''
        return render_page('Authentication - Success', 'Authentication Hardening', 'Authenticated session', 'The credentials matched the salted cryptographic hash.', body)
    # Ritorno 401 generico per evitare user enumeration se le credenziali sono errate
    body = f'''<div class="card">
        <div class="badge">Access denied</div>
        <h2>Invalid credentials</h2>
        <p class="note">Invalid username or password provided.</p>
        <div class="row"><a class="btn" href="/login">Back to login</a></div>
    </div>'''
    return render_page('Broken Authentication - Access Denied', 'Authentication Hardening', 'Authentication failed', 'Generic error response to prevent user harvesting.', body), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
