from flask import Flask, request
import os, requests

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
    data = request.json
    print(data)
    try:
        entry = data['entry'][0]['changes'][0]['value']
        if 'messages' in entry:
            phone = entry['messages'][0]['from']
            msg = entry['messages'][0]['text']['body']

            # Send reply
            token = os.environ.get("WHATSAPP_TOKEN")
            phone_id = os.environ.get("PHONE_NUMBER_ID")
            url = f"https://graph.facebook.com/v19.0/{phone_id}/messages"
            headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
            payload = {
                "messaging_product": "whatsapp",
                "to": phone,
                "text": {"body": f"You said: {msg} - Victoria Bot is Live ✅"}
            }
            requests.post(url, headers=headers, json=payload)
    except Exception as e:
        print(f"Error: {e}")
    return "OK", 200

@app.route("/")
def home():
    return "Victoria Bot Live", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
