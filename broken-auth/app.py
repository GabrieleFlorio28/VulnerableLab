from flask import Flask, request, redirect

app = Flask(__name__)

# Insecure user store: plaintext passwords and weak verification
USERS = {
    'alice': 'password123',
    'bob': 'qwerty',
}

@app.route('/')
def index():
    return 'Broken Authentication example\nUse /login to POST username and password.'

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return '''<form method="post"><input name="username"><input name="password"><button>Login</button></form>'''
    username = request.form.get('username','')
    password = request.form.get('password','')
    expected = USERS.get(username)
    if expected is None:
        return 'Invalid user', 401
    # VULNERABLE CHECK: only compares first three characters -> easy to bypass/brute-force
    if expected[:3] == password[:3]:
        return f'Logged in as {username}'
    return 'Invalid credentials', 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
