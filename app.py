from flask import Flask, request
import os, requests
from datetime import datetime

app = Flask(__name__)

# ===== EDIT PRICES HERE ONLY - CHANGE ONCE =====
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
# Add x14, x15... if needed
# ================================================

PRICE_MAP = {
"cbc": x1, "sugar": x2, "hba1c": x3, "lft": x4, "kft": x5,
"thyroid": x6, "lipid": x7, "vitamin d": x8, "b12": x9,
"urine": x10, "urine culture": x11, "diabetic": x12, "full body": x13
}

def get_price_text():
    return f"""🏥 *Victoria Hospital Lab, Puttur*
🔬 *Lab Investigations*

*Blood Tests*
• CBC - Rs.{x1}
• Sugar F/PP - Rs.{x2}
• HbA1c - Rs.{x3}
• LFT - Rs.{x4}
• KFT - Rs.{x5}
• Thyroid - Rs.{x6}
• Lipid - Rs.{x7}
• Vit D - Rs.{x8}
• Vit B12 - Rs.{x9}

*Urine Tests*
• Urine Routine - Rs.{x10}
• Urine Culture - Rs.{x11}

*Packages*
• Diabetic @ Rs.{x12}
• Full Body @ Rs.{x13}

⏰ 7am-8pm Home Collection
Reply: *Book* to book test
Or type test name for price"""

sessions = {}

def send_msg(to, text):
    token = os.environ.get("WHATSAPP_TOKEN")
    pid = os.environ.get("PHONE_NUMBER_ID")
    if not token or not pid:
        print("Missing ENV!")
        return None
    url = f"https://graph.facebook.com/v19.0/{pid}/messages"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"messaging_product":"whatsapp","to":to,"type":"text","text":{"body":text}}
    r = requests.post(url, headers=headers, json=payload)
    print(f"Sent {to}: {r.status_code}")
    return r

@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    my_token = os.environ.get("VERIFY_TOKEN","victoria123")
    if request.args.get("hub.mode")=="subscribe" and token==my_token:
        return challenge,200
    return "Forbidden",403

@app.route("/webhook", methods=["POST"])
def incoming():
    data = request.json
    print(data)
    try:
        val = data['entry'][0]['changes'][0]['value']
        if 'statuses' in val: return "OK",200
        if 'messages' not in val: return "OK",200
        m = val['messages'][0]
        phone = m['from']
        name = val['contacts'][0]['profile'].get('name','')
        text = m.get('text',{}).get('body','').strip() if m['type']=='text' else ''
        low = text.lower()

        # Reset / Menu
        if low in ["hi","hello","menu","start"]:
            sessions[phone] = {"step":"welcome","data":{"name":name}}
            send_msg(phone, f"Hi {name} 🙏\n\n{get_price_text()}\n\nReply:\n1 - Book Test\n2 - Price List\n3 - Staff")
            return "OK",200

        # Direct price query
        if low in PRICE_MAP:
            send_msg(phone, f"✅ {text.upper()} - Rs.{PRICE_MAP[low]}\n\nType *Book* to book this test.")
            return "OK",200

        sess = sessions.get(phone)
        if not sess:
            sessions[phone]={"step":"welcome","data":{"name":name}}
            send_msg(phone, get_price_text())
            return "OK",200

        step = sess["step"]
        sdata = sess["data"]

        if step=="welcome":
            if low in ["1","book","booking","test"]:
                sess["step"]="ask_name"
                send_msg(phone, "Enter *Patient Full Name*:")
            elif low in ["2","price","prices","list"]:
                send_msg(phone, get_price_text())
            elif low in ["3","staff"]:
                send_msg(phone, "👨‍⚕️ Call 08251-230000 for staff")
            else:
                send_msg(phone, "Reply 1 to Book, 2 for Prices, or type test name like CBC")

        elif step=="ask_name":
            sdata["patient_name"]=text
            sess["step"]="ask_age"
            send_msg(phone, f"Thanks {text}. Enter *Age*:")

        elif step=="ask_age":
            sdata["age"]=text
            sess["step"]="ask_test"
            send_msg(phone, f"Which tests? Type names or numbers.\n\n{get_price_text()}")

        elif step=="ask_test":
            sdata["tests_raw"]=text
            # calculate total if possible
            total=0
            chosen=[]
            for k in text.lower().replace(","," ").split():
                if k in PRICE_MAP:
                    total+=PRICE_MAP[k]
                    chosen.append(f"{k.upper()}-Rs.{PRICE_MAP[k]}")
            if chosen:
                sdata["tests_parsed"]=", ".join(chosen)
                sdata["total"]=total
            else:
                sdata["tests_parsed"]=text
                sdata["total"]="To be confirmed"
            sess["step"]="ask_address"
            send_msg(phone, f"Selected: {sdata['tests_parsed']}\nTotal: Rs.{sdata['total']}\n\nEnter *Full Address for collection* in Sindgi/Puttur:")

        elif step=="ask_address":
            sdata["address"]=text
            sess["step"]="ask_time"
            send_msg(phone, "Enter *Preferred Date & Time* (e.g. Tomorrow 9AM):")

        elif step=="ask_time":
            sdata["time"]=text
            order_id = f"VIC{datetime.now().strftime('%m%d%H%M')}"
            summary = f"✅ *Booking Confirmed!* {order_id}\n\nPatient: {sdata['patient_name']}\nAge: {sdata['age']}\nTests: {sdata['tests_parsed']}\nTotal: Rs.{sdata['total']}\nAddress: {sdata['address']}\nTime: {text}\n\nOur team will come at {text}. Report in 6 hrs.\nThank you! - Victoria Lab Puttur"
            send_msg(phone, summary)

            staff_msg = f"🧪 *NEW LAB* {order_id}\nFrom: {phone} {name}\nPatient: {sdata['patient_name']} Age:{sdata['age']}\nTests: {sdata['tests_parsed']} Total:{sdata['total']}\nAddr: {sdata['address']}\nTime: {text}"
            try: send_msg("919980569579", staff_msg)
            except: pass
            sessions.pop(phone, None)

    except Exception as e:
        print(f"Error: {e}")
        import traceback; traceback.print_exc()
    return "OK",200

@app.route("/")
def home(): return "Victoria Lab Bot - Variable Price Live",200
