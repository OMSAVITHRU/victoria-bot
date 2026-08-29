from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def home():
    return "Victoria Live"

@app.route('/privacy')
def privacy():
    return "<h1>Privacy Policy</h1><p>Victoria Hospital Lab Investig Puttur uses Instagram API to auto-reply to DMs. We do not store or share user data.</p>"

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token')=='victoria_secret_123':
        return request.args.get('hub.challenge')
    return "fail",403

@app.route('/webhook', methods=['POST'])
def incoming():
    print(request.get_json())
    return "OK",200
