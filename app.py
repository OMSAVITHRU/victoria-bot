from flask import Flask, request
import requests
app = Flask(__name__)

VERIFY_TOKEN = "victoria_secret_123"
ACCESS_TOKEN = "PUT_YOUR_LONG_TOKEN_HERE"
IG_ID = "17841400000000000" # we will replace later

@app.route('/')
def home():
    return "Victoria Live"

@app.route('/privacy')
def privacy():
    return "Privacy: We don't store data. For Victoria Hospital Lab Puttur"

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token') == VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    return "fail",403

@app.route('/webhook', methods=['POST'])
def incoming():
    data = request.get_json()
    print(data)
    try:
        for entry in data['entry']:
            for msg in entry.get('messaging', []):
                sender = msg['sender']['id']
                if 'message' in msg:
                    text = msg['message'].get('text','')
                    # REPLY
                    url = f"https://graph.facebook.com/v20.0/me/messages?access_token={ACCESS_TOKEN}"
                    payload = {
                        "recipient": {"id": sender},
                        "message": {"text": f"Hi! Thanks for messaging Victoria Hospital Lab Puttur 🙏\nYou said: {text}\nOur team will reply soon. For urgent: Call 08251-230000"}
                    }
                    requests.post(url, json=payload)
    except Exception as e:
        print(e)
    return "OK",200
