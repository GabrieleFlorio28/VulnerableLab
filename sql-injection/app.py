from flask import Flask, request, g
import sqlite3

app = Flask(__name__)
DATABASE = 'data.db'

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
    return 'Vulnerable Lab - SQL Injection example'

@app.route('/init')
def init():
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT)')
    c.execute('DELETE FROM users')
    c.executemany('INSERT INTO users (username) VALUES (?)', [('alice',), ('bob',), ('admin',)])
    db.commit()
    db.close()
    return 'initialized'

@app.route('/search')
def search():
    q = request.args.get('q', '')
    db = get_db()
    cur = db.cursor()
    # QUERY VULNERABILE: concatenazione diretta dell'input
    cur.execute(f"SELECT id, username FROM users WHERE username LIKE '%{q}%'")
    rows = cur.fetchall()
    return '<br>'.join([f"{r[0]} - {r[1]}" for r in rows])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
