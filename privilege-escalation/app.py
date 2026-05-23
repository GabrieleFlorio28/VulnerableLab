from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Privilege Escalation example.\nUse /read-secret to attempt to read /root/secret.txt'

@app.route('/read-secret')
def read_secret():
    try:
        with open('/root/secret.txt','r') as f:
            return f.read()
    except Exception as e:
        return f'Cannot read secret: {e}', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
