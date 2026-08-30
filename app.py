from flask import Flask, request
import os, requests

app = Flask(__name__)

@app.route("/webhook", methods=["GET"])
def verify():
    my = os.environ.get("VERIFY_TOKEN","victoria123")
    if request.args.get("hub.verify_token")==my:
        return request.args.get("hub.challenge"),200
    return "fail",403

@app.route("/webhook", methods=["POST"])
def incoming():
    print(request.json)
    try:
        val=request.json['entry'][0]['changes'][0]['value']
        if 'messages' in val:
            frm=val['messages'][0]['from']
            pid=os.environ.get("PHONE_NUMBER_ID")
            token=os.environ.get("WHATSAPP_TOKEN")
            print(f"Trying to reply to {frm} with PID {pid} Token starts {token[:10]}")
            url=f"https://graph.facebook.com/v19.0/{pid}/messages"
            headers={"Authorization":f"Bearer {token}","Content-Type":"application/json"}
            payload={"messaging_product":"whatsapp","to":frm,"type":"text","text":{"body":"✅ Bot is working! I received your message"}}
            r=requests.post(url, headers=headers, json=payload)
            print(f"Reply result: {r.status_code} {r.text}")
    except Exception as e:
        print(f"ERR {e}")
    return "OK",200

@app.route("/")
def home(): return "Test Bot Live",200
