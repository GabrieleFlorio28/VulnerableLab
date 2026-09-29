from flask import Flask, request
from html import escape
import os

app = Flask(__name__)

# Impostazione sicura predefinita: in produzione il debug mode deve rimanere categoricamente disattivato
DEBUG_MODE = False

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
    body = f'''<div class="card">
        <div class="badge">Scenario 04 - Mitigated</div>
        <h2>Hardened Configuration Posture</h2>
        <p class="note">Administrative endpoints and debug interfaces are strictly protected and disabled by default in production.</p>
        <div class="row">
            <a class="btn" href="/admin">Test admin access</a>
        </div>
    </div>
    <div class="card">
        <h2>Runtime status</h2>
        <p class="note">Debug mode is strictly <strong>disabled</strong>. Error stack traces and Werkzeug debug consoles are inactive.</p>
    </div>'''
    return render_page('Mitigated Lab - Misconfiguration', 'Configuration Hardening', 'Hardened runtime configuration', 'Debug flags and administrative routes are secured against unauthorized access.', body, 'Attempting to open /admin will return a 403 Forbidden response.')

# Endpoint protetto: non espone superfici amministrative basate su flag di runtime deboli
@app.route('/admin')
def admin():
    body = '''<div class="card">
        <div class="badge">Forbidden</div>
        <h2>Administrative surface protected</h2>
        <p class="note">Access denied. Administrative endpoints require explicit mutual authentication or VPN/internal access gates.</p>
        <div class="row"><a class="btn" href="/">Back to overview</a></div>
    </div>'''
    return render_page('Configuration Hardening - Forbidden', 'Configuration Hardening', 'Access denied', 'Administrative routes cannot be toggled on via debug flags.', body), 403

if __name__ == '__main__':
    # Debug disattivato in modo categorico
    app.run(host='0.0.0.0', port=5000, debug=False)
