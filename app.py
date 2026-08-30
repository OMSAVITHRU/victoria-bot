from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "OK", 200

@app.route("/webhook", methods=["GET"])
def verify():
    print(f"ALL ARGS: {dict(request.args)}")
    challenge = request.args.get("hub.challenge")
    if challenge:
        return challenge, 200
    return "OK", 200

@app.route("/webhook", methods=["POST"])
def incoming():
    print(request.json)
    return "OK", 200
