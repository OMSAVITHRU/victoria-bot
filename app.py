import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Tokens from Render Environment
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "victoria_secret_123")
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")

# Victoria Health Lab Triage Logic
def get_triage_response(user_msg):
    msg = user_msg.lower()
    
    if "hi" in msg or "hello" in msg or "hey" in msg:
        return (
            "👋 Welcome to *Victoria Health Lab Triage (VHLT)*\n\n"
            "I can help you with:\n"
            "1️⃣ Book a Lab Test\n"
            "2️⃣ Check Report Status\n"
            "3️⃣ Talk to Support\n\n"
            "Please reply with 1, 2, or 3"
        )
    elif "1" in msg or "book" in msg:
        return (
            "🧪 *Book a Lab Test*\n\n"
            "Please send:\n"
            "• Test Name\n"
            "• Preferred Date\n"
            "• Your Location\n\n"
            "Example: `CBC, Tomorrow 9am, Koramangala`"
        )
    elif "2" in msg or "report" in msg:
        return "📄 Please share your UHID / Phone number to check report status."
    elif "3" in msg or "support" in msg:
        return "👨‍⚕️ Connecting to support... Our team will call you in 10 mins. Please share your issue."
    else:
        return (
            "Thanks! We received: *" + user_msg + "*\n\n"
            "Our VHLT team will assist you shortly.\n"
            "Type *Hi* to see menu again."
        )

def send_whatsapp_message(to, text):
    if not WHATSAPP_TOKEN or not PHONE_NUMBER_ID:
        print("Missing WHATSAPP_TOKEN or PHONE_NUMBER_ID")
        return
    
    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    try:
        r = requests.post(url, headers=headers, json=data)
        print(f"Send status: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"Send error: {e}")

@app.route("/")
def home():
    return "VHLT - Victoria Health Lab Triage Bot is Live! Use /webhook", 200

# --- META VERIFICATION (This fixes your FAIL) ---
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    print(f"Verification attempt: mode={mode}, token={token}")
    
    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK VERIFIED!")
        return challenge, 200
    else:
        print("Verification failed - token mismatch")
        return "Verification failed", 403

# --- MESSAGE RECEIVING ---
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print(f"Incoming: {data}")
    
    try:
        if data.get("object") == "whatsapp_business_account":
            for entry in data.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    messages = value.get("messages", [])
                    for message in messages:
                        from_number = message.get("from")
                        msg_body = message.get("text", {}).get("body", "")
                        
                        print(f"From {from_number}: {msg_body}")
                        
                        if from_number and msg_body:
                            reply = get_triage_response(msg_body)
                            send_whatsapp_message(from_number, reply)
                            
    except Exception as e:
        print(f"Webhook error: {e}")
    
    return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
