from flask import Flask, request, g
from html import escape
import sqlite3

app = Flask(__name__)
DATABASE = 'data.db'


def render_page(title, eyebrow, headline, description, body_html, footer_html=''):
    return f'''<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)}</title>
    <style>
        :root {{
            --bg1: #f8fafc;
            --bg2: #e0f2fe;
            --card: #ffffff;
            --surface: #f8fafc;
            --border: #dbe4ef;
            --text: #0f172a;
            --muted: #475569;
            --accent: #0284c7;
            --accent2: #16a34a;
        }}
        * {{ box-sizing: border-box; }}
        body {{
            margin: 0;
            min-height: 100vh;
            font-family: Inter, Segoe UI, Arial, sans-serif;
            color: var(--text);
            background:
                radial-gradient(circle at top, rgba(14, 165, 233, 0.18), transparent 34%),
                linear-gradient(135deg, var(--bg1), var(--bg2));
            display: grid;
            place-items: center;
            padding: 32px;
        }}
        .panel {{
            width: min(880px, 100%);
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 24px;
            box-shadow: 0 22px 60px rgba(15, 23, 42, 0.12);
            overflow: hidden;
        }}
        .hero {{
            padding: 28px 32px 20px;
            border-bottom: 1px solid var(--border);
            background: linear-gradient(135deg, rgba(14, 165, 233, 0.10), rgba(34, 197, 94, 0.08));
        }}
        .eyebrow {{
            display: inline-block;
            padding: 6px 12px;
            border-radius: 999px;
            background: #e0f2fe;
            color: #0369a1;
            font-size: 12px;
            letter-spacing: .08em;
            text-transform: uppercase;
        }}
        h1 {{ margin: 14px 0 8px; font-size: 34px; line-height: 1.1; }}
        .desc {{ margin: 0; color: var(--muted); max-width: 64ch; line-height: 1.6; }}
        .content {{ padding: 30px 32px 32px; }}
        .card {{
            border: 1px solid var(--border);
            border-radius: 18px;
            background: var(--surface);
            padding: 22px;
            margin-bottom: 18px;
        }}
        .card h2 {{ margin: 0 0 12px; font-size: 18px; }}
        .row {{ display: flex; gap: 12px; flex-wrap: wrap; align-items: center; }}
        .btn {{
            display: inline-block;
            text-decoration: none;
            border: 0;
            border-radius: 12px;
            padding: 11px 16px;
            font-weight: 700;
            color: #ffffff;
            background: linear-gradient(135deg, #0284c7, #16a34a);
            box-shadow: 0 10px 22px rgba(2, 132, 199, 0.18);
        }}
        .btn.secondary {{
            color: #0f172a;
            background: #ffffff;
            border: 1px solid var(--border);
            box-shadow: none;
        }}
        .input {{
            width: 100%;
            padding: 12px 14px;
            margin: 8px 0 14px;
            border-radius: 12px;
            border: 1px solid var(--border);
            background: #ffffff;
            color: var(--text);
            outline: none;
        }}
        .note {{ color: var(--muted); font-size: 14px; line-height: 1.6; }}
        .badge {{
            display: inline-block;
            margin-bottom: 12px;
            padding: 6px 10px;
            border-radius: 999px;
            color: #166534;
            background: #dcfce7;
            font-size: 12px;
            letter-spacing: .06em;
            text-transform: uppercase;
        }}
        pre {{
            margin: 0;
            padding: 16px;
            border-radius: 14px;
            background: #ffffff;
            border: 1px solid var(--border);
            overflow: auto;
            color: #0f172a;
            line-height: 1.6;
        }}
        .footer {{ padding: 0 32px 28px; color: var(--muted); font-size: 13px; }}
        .grid {{ display: grid; gap: 12px; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }}
        .result {{ padding: 14px 16px; border-radius: 14px; background: #f0fdf4; border: 1px solid #bbf7d0; }}
    </style>
</head>
<body>
    <main class="panel">
        <section class="hero">
            <span class="eyebrow">{escape(eyebrow)}</span>
            <h1>{escape(headline)}</h1>
            <p class="desc">{escape(description)}</p>
        </section>
        <section class="content">
            {body_html}
        </section>
        {f'<div class="footer">{footer_html}</div>' if footer_html else ''}
    </main>
</body>
</html>'''

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = sqlite3.connect(DATABASE)
        g._database = db
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    body = '''<div class="grid">
        <div class="card">
            <div class="badge">Scenario 01</div>
            <h2>Vulnerable search endpoint</h2>
            <p class="note">This page demonstrates a SQL injection flaw caused by direct concatenation of user input into the query.</p>
        </div>
        <div class="card">
            <div class="badge">Quick actions</div>
            <div class="row">
                <a class="btn" href="/init">Initialize database</a>
                <a class="btn secondary" href="/search?q=alice">Search alice</a>
            </div>
        </div>
    </div>'''
    return render_page('Vulnerable Lab - SQL Injection', 'SQL Injection', 'Search endpoint with unsafe query building', 'A minimal Flask app with an intentionally vulnerable search endpoint.', body, 'Open /init first, then use /search to inspect the results.')

@app.route('/init')
def init():
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT)')
    c.execute('DELETE FROM users')
    c.executemany('INSERT INTO users (username) VALUES (?)', [('alice',), ('bob',), ('admin',)])
    db.commit()
    db.close()
    body = '''<div class="card">
        <div class="badge">Database ready</div>
        <h2>SQLite database initialized</h2>
        <p class="note">The <code>users</code> table has been created and populated with sample records for the lab.</p>
        <div class="row">
            <a class="btn" href="/search?q=alice">Go to search</a>
            <a class="btn secondary" href="/">Back to overview</a>
        </div>
    </div>'''
    return render_page('SQL Injection - Database initialized', 'SQL Injection', 'Database initialization complete', 'The sample data is now available for the search endpoint.', body, 'This screen works well as a browser screenshot for the implementation chapter.')

@app.route('/search')
def search():
    q = request.args.get('q', '')
    db = get_db()
    cur = db.cursor()
    # QUERY VULNERABILE: concatenazione diretta dell'input
    cur.execute(f"SELECT id, username FROM users WHERE username LIKE '%{q}%'")
    rows = cur.fetchall()
    results = ''.join([f'<div class="result">{escape(str(r[0]))} - {escape(r[1])}</div>' for r in rows])
    if not results:
        results = '<div class="result">No results found.</div>'
    body = f'''<div class="card">
        <div class="badge">Query results</div>
        <h2>Search term: <code>{escape(q)}</code></h2>
        <div class="grid">{results}</div>
    </div>
    <div class="row">
        <a class="btn" href="/init">Reinitialize database</a>
        <a class="btn secondary" href="/">Back to overview</a>
    </div>'''
    return render_page('SQL Injection - Search results', 'SQL Injection', 'Search output', 'The query is executed with direct string concatenation, which makes the endpoint vulnerable.', body, 'Try a normal search like alice for the clean screenshot, then use an altered input to demonstrate the flaw.')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
