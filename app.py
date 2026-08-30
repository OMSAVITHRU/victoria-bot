from flask import Flask, request
import os, requests
from datetime import datetime

app = Flask(__name__)

# In-memory sessions {phone: {step, data}}
sessions = {}

TESTS = {
"1": "CBC - Rs 300",
"2": "Blood Sugar (FBS/PPBS) - Rs 150",
"3": "Thyroid T3 T4 TSH - Rs 500",
"4": "Lipid Profile - Rs 600",
"5": "Liver Function LFT - Rs 600",
"6": "Kidney Function KFT - Rs 600",
"7": "HbA1c - Rs 400",
"8": "Vitamin D + B12 - Rs 1200",
"9": "Full Body Checkup - Rs 1999",
}

def send_msg(to, text):
    token = os.environ.get("WHATSAPP_TOKEN")
    pid = os.environ.get("PHONE_NUMBER_ID")
    url = f"https://graph.facebook.com/v19.0/{pid}/messages"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"messaging_product":"whatsapp","to":to,"type":"text","text":{"body":text}}
    r = requests.post(url, headers=headers, json=payload)
    print(f"Sent to {to}: {r.status_code} {r.text}")
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

        msg = val['messages'][0]
        phone = msg['from']
        name = val['contacts'][0]['profile']['name']
        text = msg.get('text',{}).get('body','').strip() if msg['type']=='text' else ''

        # Reset
        if text.lower() in ["hi","hello","menu","start","reset"]:
            sessions[phone] = {"step":"welcome","data":{"name":name}}
            send_msg(phone, f"Hi {name} 🙏 Welcome to *Victoria Hospital Lab - Puttur*\n\n🧪 *Lab Test Booking*\n1. Book a Test\n2. Test List & Prices\n3. Talk to Staff\n\nReply with 1,2,3")
            return "OK",200

        sess = sessions.get(phone)
        if not sess:
            sessions[phone] = {"step":"welcome","data":{"name":name}}
            send_msg(phone, f"Hi {name} 🙏 Send *Hi* to start booking lab tests.")
            return "OK",200

        step = sess["step"]
        sdata = sess["data"]

        if step=="welcome":
            if text=="1":
                sess["step"]="ask_name"
                send_msg(phone, "Great! Please enter *Patient Full Name*:")
            elif text=="2":
                list_msg = "*Our Tests:*\n" + "\n".join([f"{k}. {v}" for k,v in TESTS.items()]) + "\n\nSend *Hi* to book."
                send_msg(phone, list_msg)
            elif text=="3":
                send_msg(phone, "Please call: 08251-230000 or this number. Or send *Hi* to book.")
            else:
                send_msg(phone, "Please reply 1 to Book, 2 for Test List, 3 for Staff.")

        elif step=="ask_name":
            sdata["patient_name"]=text
            sess["step"]="ask_age"
            send_msg(phone, f"Thanks {text}. Enter *Age*:")

        elif step=="ask_age":
            sdata["age"]=text
            sess["step"]="ask_test"
            list_msg = "*Select Test Number:*\n" + "\n".join([f"{k}. {v}" for k,v in TESTS.items()]) + "\n\nYou can type multiple e.g. 1,3"
            send_msg(phone, list_msg)

        elif step=="ask_test":
            sdata["tests"]=text
            # parse test names
            chosen=[]
            for t in text.replace(","," ").split():
                if t in TESTS: chosen.append(TESTS[t])
            if not chosen: chosen=[text]
            sdata["tests_parsed"]=", ".join(chosen)
            sess["step"]="ask_address"
            send_msg(phone, "Enter *Full Address for sample collection* in Sindgi/Puttur:")

        elif step=="ask_address":
            sdata["address"]=text
            sess["step"]="ask_time"
            send_msg(phone, "Enter *Preferred Date & Time* (e.g. Tomorrow 9AM):")

        elif step=="ask_time":
            sdata["time"]=text
            sess["step"]="done"
            order_id = f"VIC{datetime.now().strftime('%m%d%H%M')}"
            # Final confirmation to patient
            summary = f"✅ *Booking Confirmed!* {order_id}\n\nPatient: {sdata['patient_name']}\nAge: {sdata['age']}\nTests: {sdata['tests_parsed']}\nAddress: {sdata['address']}\nTime: {text}\n\nOur phlebotomist will come at requested time. For queries call 08251-230000.\n\nThank you!"
            send_msg(phone, summary)

            # Notify you / lab staff - send to your number 919980569579
            staff_msg = f"🧪 *NEW LAB REQUEST* {order_id}\nFrom: {phone} ({name})\nPatient: {sdata['patient_name']}, Age {sdata['age']}\nTests: {sdata['tests_parsed']}\nAddr: {sdata['address']}\nTime: {text}"
            try:
                send_msg("919980569579", staff_msg) # your staff alert
            except: pass

            sessions.pop(phone, None)

    except Exception as e:
        print(f"Error: {e}")
        import traceback; traceback.print_exc()
    return "OK",200

@app.route("/")
def home(): return "Victoria Lab Bot Live",200
