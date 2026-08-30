from flask import Flask, request
import os, requests
from datetime import datetime

app = Flask(__name__)
sessions = {}

def send_msg(to, text):
    token = os.environ.get("WHATSAPP_TOKEN")
    pid = os.environ.get("PHONE_NUMBER_ID")
    if not token or not pid:
        return
    url = f"https://graph.facebook.com/v19.0/{pid}/messages"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"messaging_product":"whatsapp","to":to,"type":"text","text":{"body":text}}
    requests.post(url, headers=headers, json=payload)

@app.route("/webhook", methods=["GET"])
def verify():
    my = os.environ.get("VERIFY_TOKEN","victoria123")
    if request.args.get("hub.verify_token") == my:
        return request.args.get("hub.challenge"),200
    return "Forbidden",403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print(data)
    try:
        val = data['entry'][0]['changes'][0]['value']
        if 'messages' in val:
            frm = val['messages'][0]['from']
            txt = val['messages'][0].get('text',{}).get('body','')
            name = val['contacts'][0]['profile'].get('name','')
            if txt.lower() in ["hi","hello"]:
                send_msg(frm, f"Hi {name} Bot working! Send Name")
            else:
                send_msg(frm, f"You said: {txt} - Bot OK")
    except Exception as e:
        print(e)
    return "OK",200

@app.route("/")
def home():
    return "OK",200
