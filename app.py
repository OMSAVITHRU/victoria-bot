from flask import Flask, request
import requests

app = Flask(__name__)

VERIFY_TOKEN = "victoria_secret_123"
WHATSAPP_TOKEN = "PASTE_TOKEN"
PHONE_NUMBER_ID = "PASTE_ID"
IG_TOKEN = "PASTE_IG_TOKEN"

# ===== EDIT PRICES HERE ONLY =====
x1 = 350 # CBC
x2 = 100 # Sugar F/PP
x3 = 500 # HbA1c
x4 = 600 # LFT
x5 = 600 # KFT
x6 = 500 # Thyroid
x7 = 600 # Lipid
x8 = 800 # Vitamin D
x9 = 800 # Vitamin B12
x10 = 150 # Urine Routine
x11 = 500 # Urine Culture
x12 = 999 # Diabetic Package
x13 = 1999 # Full Body Checkup
# Add more: x14, x15...
# ==================================

def get_lab_menu():
    return f"""🏥 *Victoria Hospital Lab, Puttur*

*Lab Investigations* 🔬
1️⃣ Blood Tests
2️⃣ Urine Tests
3️⃣ Packages
4️⃣ Report Status
5️⃣ Staff

Reply 1-5
Or type test name

*For price, type test name*"""

DETAILS = {
    "1": f"🩸 *Blood Tests*\n• CBC - Rs.{{x1}}\n• Sugar F/PP - Rs.{{x2}}\n• HbA1c - Rs.{{x3}}\n• LFT - Rs.{{x4}}\n• KFT - Rs.{{x5}}\n• Thyroid - Rs.{{x6}}\n• Lipid - Rs.{{x7}}\n• Vit D - Rs.{{x8}}\n• Vit B12 - Rs.{{x9}}\n\n⏰ 7am-8pm",
    "2": f"🧪 *Urine Tests*\n• Urine Routine - Rs.{{x10}}\n• Urine Culture - Rs.{{x11}}",
    "3": f"📦 *Packages*\n• Diabetic @ Rs.{{x12}}\n• Full Body @ Rs.{{x13}}",
    "4": "📄 Send Bill No for report status",
    "5": "👨‍⚕️ Call 08251-230000 for staff"
}

# Map test names to price variables
PRICE_MAP = {
    "cbc": x1, "sugar": x2, "hba1c": x3, "lft": x4, "kft": x5,
    "thyroid": x6, "lipid": x7, "vitamin d": x8, "b12": x9,
    "urine": x10, "urine culture": x11, "diabetic": x12, "full body": x13
}

def send_wa(to, text, buttons=None):
    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
    payload = {"messaging_product":"whatsapp","to":to,"text":{"body":text}}
    if buttons:
        payload = {
            "messaging_product":"whatsapp","to":to,
            "type":"interactive",
            "interactive":{"type":"button","body":{"text":text},"action":{"buttons":buttons}}
        }
    requests.post(url, headers=headers, json=payload)

def send_ig(sid, text):
    url = f"https://graph.facebook.com/v20.0/me/messages?access_token={IG_TOKEN}"
    requests.post(url, json={"recipient":{"id":sid},"message":{"text":text}})

@app.route('/')
def home(): return "Victoria Lab Bot - Variable Price"
@app.route('/privacy')
def privacy(): return "Privacy Policy"
@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token') == VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    return "fail",403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    try:
        if 'entry' in data and data['entry'][0].get('changes'):
            val = data['entry'][0]['changes'][0]['value']
            if 'messages' in val:
                m = val['messages'][0]
                frm = m['from']
                if m['type'] == 'text':
                    txt = m['text']['body'].strip()
                    low = txt.lower()
                    if low in ['hi','hello','menu']:
                        btns = [
                            {"type":"reply","reply":{"id":"lab","title":"🔬 Tests"}},
                            {"type":"reply","reply":{"id":"price","title":"💰 Price"}},
                            {"type":"reply","reply":{"id":"staff","title":"👨‍⚕️ Staff"}}
                        ]
                        send_wa(frm, "Welcome to Victoria Lab Puttur!", btns)
                    elif txt in DETAILS:
                        send_wa(frm, DETAILS[txt].format(x1=x1,x2=x2,x3=x3,x4=x4,x5=x5,x6=x6,x7=x7,x8=x8,x9=x9,x10=x10,x11=x11,x12=x12,x13=x13))
                    elif low in PRICE_MAP:
                        send_wa(frm, f"✅ {txt.upper()} available - Rs.{PRICE_MAP[low]}\nTo book send Name & Age")
                    else:
                        send_wa(frm, get_lab_menu())

                if m['type'] == 'interactive':
                    bid = m['interactive']['button_reply']['id']
                    if bid == 'lab': send_wa(frm, get_lab_menu())
                    elif bid == 'price': send_wa(frm, DETAILS["1"].format(x1=x1,x2=x2,x3=x3,x4=x4,x5=x5,x6=x6,x7=x7,x8=x8,x9=x9,x10=x10,x11=x11,x12=x12,x13=x13))
                    elif bid == 'staff': send_wa(frm, DETAILS["5"])

        if 'entry' in data and 'messaging' in data['entry'][0]:
            for e in data['entry']:
                for msg in e.get('messaging', []):
                    if 'message' in msg:
                        sid = msg['sender']['id']
                        low = msg['message'].get('text','').lower()
                        if low in PRICE_MAP:
                            send_ig(sid, f"{low.upper()} - Rs.{PRICE_MAP[low]}")
                        else:
                            send_ig(sid, get_lab_menu())
    except Exception as e:
        print(e)
    return "OK",200
