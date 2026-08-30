from flask import Flask, request
import os, requests, json

app = Flask(__name__)
VERIFY_TOKEN = "victoria123"
# Put these in Render Env Vars later
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_ID = os.getenv("PHONE_ID")

@app.route("/")
def home():
    return "OK", 200

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        print(f"ALL ARGS: {dict(request.args)}", flush=True)
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == VERIFY_TOKEN and challenge:
            return challenge, 200
        # temp bypass for old bad URL with only?hub.challenge=
        if challenge and not mode:
            return challenge, 200
        return "OK", 200

    # POST - real WhatsApp message
    data = request.get_json()
    print(f"INCOMING: {json.dumps(data, indent=2)}", flush=True)

    try:
        entry = data["entry"][0]["changes"][0]["value"]
        if "messages" in entry:
            msg = entry["messages"][0]
            from_number = msg["from"]
            text = msg["text"]["body"]
            print(f"Message from {from_number}: {text}", flush=True)
            # Optional auto-reply if token set
            if WHATSAPP_TOKEN and PHONE_ID:
                requests.post(
                    f"https://graph.facebook.com/v20.0/{PHONE_ID}/messages",
                    headers={"Authorization": f"Bearer {WHATSAPP_TOKEN}"},
                    json={"messaging_product":"whatsapp","to":from_number,"text":{"body":f"You said: {text}"}}
                )
    except Exception as e:
        print(f"Error: {e}", flush=True)

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
