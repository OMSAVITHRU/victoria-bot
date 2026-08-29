from flask import Flask, request
import os

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "victoria123")

@app.route("/")
def home():
    return "Bot is running", 200

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        
        print(f"Verification: mode={mode}, token={token}, challenge={challenge}")
        print(f"Expected token: {VERIFY_TOKEN}")
        
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("VERIFY SUCCESS")
            return challenge, 200
        else:
            print("VERIFY FAILED")
            return "Forbidden", 403

    if request.method == "POST":
        data = request.get_json()
        print("Received message:", data)
        # Your message handling + send reply here
        return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
