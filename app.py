from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Victoria Bot is Live - Puttur"

@app.route('/webhook', methods=['GET'])
def verify():
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    if token == 'victoria_secret_123':
        return challenge
    return "Invalid token", 403

@app.route('/webhook', methods=['POST'])
def incoming():
    data = request.get_json()
    print(data)
    return "OK", 200
