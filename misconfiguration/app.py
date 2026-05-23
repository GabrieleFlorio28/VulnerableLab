from flask import Flask, request
import os

app = Flask(__name__)

DEBUG_MODE = os.getenv('DEBUG_MODE','false').lower() in ('1','true','yes')

@app.route('/')
def index():
    return 'Misconfiguration example. DEBUG_MODE=' + str(DEBUG_MODE)

# Admin/shutdown endpoint accidentally exposed when DEBUG_MODE is true
@app.route('/admin')
def admin():
    if not DEBUG_MODE:
        return 'Not available', 403
    return 'Admin panel (exposed due to misconfiguration)'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=DEBUG_MODE)
