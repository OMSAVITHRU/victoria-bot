from flask import Flask, request
import os
app = Flask(__name__)

@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    mode = request.args.get("hub.mode")
    
    my_token = os.environ.get("VERIFY_TOKEN")
    print(f"GOT: {token} | EXPECTED: {my_token}")
    
    if mode == "subscribe" and token == my_token:
        return challenge, 200
    return "Forbidden", 403

@app.route("/webhook", methods=["POST"])
def incoming():
    print(request.json)
    return "OK", 200

@app.route("/")
def home():
    return "OK", 200
