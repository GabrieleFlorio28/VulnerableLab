from flask import Flask, request
from html import escape
import os

app = Flask(__name__)

DEBUG_MODE = os.getenv('DEBUG_MODE','false').lower() in ('1','true','yes')


def render_page(title, eyebrow, headline, description, body_html, footer_html=''):
    return f'''<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)}</title>
    <style>
        :root {{ --bg1:#f8fafc; --bg2:#e0f2fe; --card:#ffffff; --surface:#f8fafc; --border:#dbe4ef; --text:#0f172a; --muted:#475569; }}
        * {{ box-sizing:border-box; }}
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
        .note {{ color:var(--muted); font-size:14px; line-height:1.6; }}
        .badge {{ display:inline-block; margin-bottom:12px; padding:6px 10px; border-radius:999px; color:#166534; background:#dcfce7; font-size:12px; letter-spacing:.06em; text-transform:uppercase; }}
        .input {{ width:100%; padding:12px 14px; margin:8px 0 14px; border-radius:12px; border:1px solid var(--border); background:#ffffff; color:var(--text); outline:none; }}
        .footer {{ padding:0 32px 28px; color:var(--muted); font-size:13px; }}
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
    status = 'enabled' if DEBUG_MODE else 'disabled'
    body = f'''<div class="card">
        <div class="badge">Scenario 04</div>
        <h2>Application configuration overview</h2>
        <p class="note">The service is running with <code>DEBUG_MODE={str(DEBUG_MODE).lower()}</code>. In the lab this makes the admin endpoint visible and is used to demonstrate the effect of an insecure deployment setting.</p>
        <div class="row">
            <a class="btn" href="/admin">Open admin endpoint</a>
        </div>
    </div>
    <div class="card">
        <h2>Current status</h2>
        <p class="note">Debug mode is <strong>{escape(status)}</strong> for this scenario.</p>
    </div>'''
    return render_page('Vulnerable Lab - Misconfiguration', 'Misconfiguration', 'Insecure runtime configuration', 'The service exposes an administrative route because the environment is intentionally misconfigured.', body, 'This screen is useful to show how a deployment setting can change the visible behavior of the application.')

# Admin/shutdown endpoint accidentally exposed when DEBUG_MODE is true
@app.route('/admin')
def admin():
    if not DEBUG_MODE:
        body = '''<div class="card">
            <div class="badge">Forbidden</div>
            <h2>Admin endpoint not available</h2>
            <p class="note">The route is protected because debug mode is disabled.</p>
            <div class="row"><a class="btn" href="/">Back to overview</a></div>
        </div>'''
        return render_page('Misconfiguration - Forbidden', 'Misconfiguration', 'Access denied', 'The endpoint is unavailable when debug mode is disabled.', body), 403
    body = '''<div class="card">
        <div class="badge">Admin panel</div>
        <h2>Exposed due to misconfiguration</h2>
        <p class="note">This administrative surface is reachable because the service is running with debug mode enabled.</p>
        <div class="row"><a class="btn" href="/">Back to overview</a></div>
    </div>'''
    return render_page('Misconfiguration - Admin panel', 'Misconfiguration', 'Administrative endpoint exposed', 'The endpoint is reachable because the deployment is intentionally misconfigured.', body)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=DEBUG_MODE)
