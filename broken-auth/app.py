from flask import Flask, request
from html import escape

app = Flask(__name__)

# Insecure user store: plaintext passwords and weak verification
USERS = {
    'alice': 'password123',
    'bob': 'qwerty',
}


def render_page(title, eyebrow, headline, description, body_html, footer_html=''):
    return f'''<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)}</title>
    <style>
        :root {{ --bg1:#0f172a; --bg2:#111827; --card:rgba(15,23,42,.82); --border:rgba(148,163,184,.22); --text:#e2e8f0; --muted:#94a3b8; --accent:#38bdf8; --accent2:#22c55e; }}
        * {{ box-sizing: border-box; }}
        body {{ margin:0; min-height:100vh; font-family:Inter, Segoe UI, Arial, sans-serif; color:var(--text); background:radial-gradient(circle at top, rgba(56,189,248,.18), transparent 34%), linear-gradient(135deg, var(--bg1), var(--bg2)); display:grid; place-items:center; padding:32px; }}
        .panel {{ width:min(880px,100%); background:var(--card); border:1px solid var(--border); border-radius:24px; box-shadow:0 24px 80px rgba(0,0,0,.35); overflow:hidden; }}
        .hero {{ padding:28px 32px 20px; border-bottom:1px solid var(--border); background:linear-gradient(135deg, rgba(14,165,233,.12), rgba(34,197,94,.08)); }}
        .eyebrow {{ display:inline-block; padding:6px 12px; border-radius:999px; background:rgba(56,189,248,.14); color:#bfdbfe; font-size:12px; letter-spacing:.08em; text-transform:uppercase; }}
        h1 {{ margin:14px 0 8px; font-size:34px; line-height:1.1; }}
        .desc {{ margin:0; color:var(--muted); max-width:64ch; line-height:1.6; }}
        .content {{ padding:30px 32px 32px; }}
        .card {{ border:1px solid var(--border); border-radius:18px; background:rgba(15,23,42,.55); padding:22px; margin-bottom:18px; }}
        .card h2 {{ margin:0 0 12px; font-size:18px; }}
        .row {{ display:flex; gap:12px; flex-wrap:wrap; align-items:center; }}
        .btn {{ display:inline-block; text-decoration:none; border:0; border-radius:12px; padding:11px 16px; font-weight:700; color:#04111f; background:linear-gradient(135deg, #67e8f9, #34d399); box-shadow:0 10px 22px rgba(34,197,94,.18); }}
        .btn.secondary {{ color:var(--text); background:rgba(148,163,184,.12); border:1px solid var(--border); box-shadow:none; }}
        .input {{ width:100%; padding:12px 14px; margin:8px 0 14px; border-radius:12px; border:1px solid var(--border); background:rgba(2,6,23,.65); color:var(--text); outline:none; }}
        .note {{ color:var(--muted); font-size:14px; line-height:1.6; }}
        .badge {{ display:inline-block; margin-bottom:12px; padding:6px 10px; border-radius:999px; color:#d1fae5; background:rgba(34,197,94,.14); font-size:12px; letter-spacing:.06em; text-transform:uppercase; }}
        .footer {{ padding:0 32px 28px; color:var(--muted); font-size:13px; }}
        .result {{ padding:14px 16px; border-radius:14px; background:rgba(34,197,94,.08); border:1px solid rgba(34,197,94,.24); }}
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
        <div class="badge">Scenario 02</div>
        <h2>Broken authentication flow</h2>
        <p class="note">Credentials are stored in plaintext and the verification logic is intentionally weak to make the flaw visible during the demo.</p>
        <div class="row">
            <a class="btn" href="/login">Open login page</a>
        </div>
    </div>'''
    return render_page('Vulnerable Lab - Broken Authentication', 'Broken Authentication', 'Weak login control', 'A deliberately fragile authentication flow for demonstration and testing.', body, 'Open the login form and submit a valid user. The form is styled so the browser screenshot looks cleaner.')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        body = '''<div class="card">
            <div class="badge">Login form</div>
            <h2>Authenticate to continue</h2>
            <p class="note">For the lab, the verification is intentionally flawed so the effect of a weak control can be observed easily.</p>
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
        return render_page('Broken Authentication - Login', 'Broken Authentication', 'Login form', 'The page is presented in a cleaner layout for the thesis screenshots.', body, 'The vulnerability remains unchanged: the password comparison is still intentionally weak.')
    username = request.form.get('username','')
    password = request.form.get('password','')
    expected = USERS.get(username)
    if expected is None:
        body = f'''<div class="card">
            <div class="badge">Access denied</div>
            <h2>Invalid user</h2>
            <p class="note">The username <code>{escape(username)}</code> was not found in the internal store.</p>
            <div class="row"><a class="btn" href="/login">Back to login</a></div>
        </div>'''
        return render_page('Broken Authentication - Invalid user', 'Broken Authentication', 'Authentication failed', 'The supplied user does not exist in the internal list.', body), 401
    # VULNERABLE CHECK: only compares first three characters -> easy to bypass/brute-force
    if expected[:3] == password[:3]:
        body = f'''<div class="card">
            <div class="badge">Access granted</div>
            <h2>Logged in as {escape(username)}</h2>
            <p class="note">This success is intentional in the lab and highlights the weakness in the comparison logic.</p>
            <div class="row"><a class="btn" href="/login">Try another login</a></div>
        </div>'''
        return render_page('Broken Authentication - Success', 'Broken Authentication', 'Authenticated session', 'The login flow accepted the credentials because the check is intentionally weak.', body)
    body = f'''<div class="card">
        <div class="badge">Access denied</div>
        <h2>Invalid credentials</h2>
        <p class="note">The username <code>{escape(username)}</code> was found, but the supplied password did not satisfy the vulnerable check.</p>
        <div class="row"><a class="btn" href="/login">Back to login</a></div>
    </div>'''
    return render_page('Broken Authentication - Invalid credentials', 'Broken Authentication', 'Authentication failed', 'The input did not satisfy the deliberately weak check.', body), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
