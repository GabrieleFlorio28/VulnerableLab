from flask import Flask
from html import escape

app = Flask(__name__)


def render_page(title, eyebrow, headline, description, body_html, footer_html=''):
    return f'''<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)}</title>
    <style>
        :root {{ --bg1:#0f172a; --bg2:#111827; --card:rgba(15,23,42,.82); --border:rgba(148,163,184,.22); --text:#e2e8f0; --muted:#94a3b8; }}
        * {{ box-sizing:border-box; }}
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
        .note {{ color:var(--muted); font-size:14px; line-height:1.6; }}
        .badge {{ display:inline-block; margin-bottom:12px; padding:6px 10px; border-radius:999px; color:#d1fae5; background:rgba(34,197,94,.14); font-size:12px; letter-spacing:.06em; text-transform:uppercase; }}
        pre {{ margin:0; padding:16px; border-radius:14px; background:rgba(2,6,23,.72); border:1px solid var(--border); overflow:auto; color:#e0f2fe; line-height:1.6; }}
        .footer {{ padding:0 32px 28px; color:var(--muted); font-size:13px; }}
        code {{ padding:2px 6px; border-radius:8px; background:rgba(148,163,184,.12); }}
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
        <div class="badge">Scenario 03</div>
        <h2>Restricted file access</h2>
        <p class="note">The service exposes an endpoint that attempts to read a privileged file from the container, making the effect of excessive access easier to observe.</p>
        <div class="row">
            <a class="btn" href="/read-secret">Read secret file</a>
        </div>
    </div>'''
    return render_page('Vulnerable Lab - Privilege Escalation', 'Privilege Escalation', 'Access to a privileged resource', 'The endpoint is intentionally wired to a secret file inside the container.', body, 'The lab demonstrates the impact of exposing data that should remain confined.')

@app.route('/read-secret')
def read_secret():
    try:
        with open('/root/secret.txt','r') as f:
            secret = escape(f.read())
            body = f'''<div class="card">
                <div class="badge">Secret exposed</div>
                <h2>Read privileged content</h2>
                <p class="note">The application managed to access a file that should normally remain protected inside the container.</p>
                <pre>{secret}</pre>
                <div class="row" style="margin-top:14px;">
                    <a class="btn" href="/">Back to overview</a>
                </div>
            </div>'''
            return render_page('Privilege Escalation - Secret exposed', 'Privilege Escalation', 'Privileged content', 'The container reveals a sensitive file as part of the demo scenario.', body)
    except Exception as e:
        body = f'''<div class="card">
            <div class="badge">Error</div>
            <h2>Cannot read secret</h2>
            <p class="note">The application failed to access the file.</p>
            <pre>{escape(str(e))}</pre>
        </div>'''
        return render_page('Privilege Escalation - Error', 'Privilege Escalation', 'Read failure', 'The privileged file could not be opened.', body), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
