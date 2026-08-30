from flask import Flask, request
import os
import requests

app = Flask(__name__)

@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    mode = request.args.get("hub.mode")
    my_token = os.environ.get("VERIFY_TOKEN", "victoria123")
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
        # Ignore status updates (sent/delivered/read)
        if 'statuses' in entry:
            return "OK", 200

        if 'messages' in entry:
            phone = entry['messages'][0]['from']
            msg_type = entry['messages'][0]['type']

            if msg_type == 'text':
                msg_body = entry['messages'][0]['text']['body']
            else:
                msg_body = f"[{msg_type} message]"

            # Send reply
            whatsapp_token = os.environ.get("WHATSAPP_TOKEN")
            phone_number_id = os.environ.get("PHONE_NUMBER_ID")

            if not whatsapp_token or not phone_number_id:
                print("ERROR: WHATSAPP_TOKEN or PHONE_NUMBER_ID missing!")
                return "OK", 200

            url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"
            headers = {
                "Authorization": f"Bearer {whatsapp_token}",
                "Content-Type": "application/json"
            }
            payload = {
                "messaging_product": "whatsapp",
                "to": phone,
                "type": "text",
                "text": {"body": f"Hi! You said: {msg_body}\n\nVictoria Bot is Live ✅ - {phone}"}
            }
            resp = requests.post(url, headers=headers, json=payload)
            print(f"Reply sent to {phone}: {resp.status_code} {resp.text}")

    except Exception as e:
        print(f"Error in incoming: {e}")
