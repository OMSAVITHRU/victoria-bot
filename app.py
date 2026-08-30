from flask import Flask, request
import os, requests
from datetime import datetime

app = Flask(__name__)

ALL_TESTS = {
1:"Hb, PCV",2:"Hb, TC, DC",3:"Hb, TC, DC, ALC",4:"Hb Hemoglobin",5:"PCV Packed Cell Volume",
6:"RBC Count",7:"TC Total Count",8:"DC Differential Count",9:"TC, DC Total Differential",
10:"Platelet Count",11:"Complete Blood Counts",12:"Complete Hemogram",13:"ALC Absolute Lymphocyte Count",
14:"AEC Eosinophil Count",15:"Peripheral Smear",16:"Reticulocyte Count",17:"ESR",
18:"Bone Marrow Aspiration & Biopsy",19:"Factor VIII Assay",20:"Factor IX Assay",21:"Inhibitor Assay",
22:"Bethesda system Inhibitor",23:"Hb electrophoresis",24:"Protein electrophoresis",25:"Urea solubility test",
26:"Clot retraction test",27:"Mixing studies",28:"MPO",29:"Immunofluorescence direct",30:"LE Cells",
31:"Osmotic fragility tests",32:"Prothrombin time",33:"APTT",34:"D-dimer",
35:"Fibrinogen",36:"Sickling test",37:"Urine routine",38:"Urine analysis",39:"BT CT",
40:"Urine bile salts and pigments",41:"Urine Ketone bodies",42:"24 hrs Urine protein",43:"Semen Analysis",
44:"Stool routine",45:"Stool reducing substances",46:"Stool occult blood",47:"FNAC USG guided",
48:"Fluid cell count and cell type",49:"CSF ASCITIC FLUID",50:"PLEURAL FLUID",51:"SYNOVIAL BAL FLUID",
52:"DRAIN FLUID SPUTUM",53:"Cytology malignant cells",54:"Pap smear",55:"Tzanck smear acantholyigic",
56:"Scrapings touch smear",57:"Cytology IHC",58:"Urine malignant cells",59:"Biopsy big",
60:"Biopsy Medium",61:"Biopsy small",62:"IHC each marker",63:"Second opinion HPE",
64:"NSE",65:"PAS",66:"AchE stain Hirschsprung",67:"Frozen section",68:"Perinatal autopsy",69:"Cell block",
70:"DIABETIC HEALTH",71:"FBS PPBS",72:"RBS",73:"HBA1C",74:"C-peptide",75:"Insulin",76:"GAD Antibodies",
77:"RENAL FUNCTION TEST",78:"Creatinine",79:"Uric acid",80:"Blood urea BUN",81:"Calcium total",
82:"Calcium Ionized",83:"Phosphorus",84:"Electrolytes NA/K/CI",85:"Cystatin C",86:"eGFR",
87:"LIVER FUNCTION TEST",88:"Total billirubin",89:"Direct Billirubin",90:"Total protein",91:"Albumin",92:"Globulin",
93:"SGOT AST",94:"SGPT ALT",95:"Alkaline phosphatase ALP",96:"GGT",97:"5 Nucleotidase",98:"LIPID PROFILE LP",
99:"Total Cholesterol",100:"HDL Cholesterol",101:"LDL Cholesterol",102:"VLDL Cholesterol",103:"Triglycerides",
104:"CARDIAC PROFILE",105:"LDH",106:"CK MB STAT",107:"CK TOTAL",108:"TROP T",109:"TROP I",
110:"Lp(a)",111:"Total homocysteine",112:"T3 T4 TSH",113:"fT3 fT4",114:"FSH LH",115:"Prolactin",
116:"Total testosterone",117:"Free testosterone",118:"17-OH PROGESTERONE",119:"Progesterone",120:"Cortisol",
121:"Intact PTH",122:"Growth Hormone",123:"Beta HCG",124:"Ammonia",125:"Magnesium",126:"Serum amylase",
127:"Serum lipase",128:"Pseudocholline esterase",129:"Ferritin",130:"Vit B12",131:"Vit D",132:"Folate",
133:"ADA",134:"Lithium",135:"CRP",136:"CSF ASCITIC PLEURAL",137:"SYNOVIAL",138:"Sugar",139:"Protein",
140:"Chloride",141:"Others",142:"URINE PANEL",143:"Spot Urine",144:"Spot urine creatinine",
145:"Spot Urine Electrolytes",146:"Urine others",147:"Urine PCR",148:"Urine ACR",149:"24 hour urine protein",
150:"24 hour urine creatinine",151:"Others urine",152:"TUMOR MARKERS",153:"CA-125",154:"CEA",155:"AFP",
156:"PSA total free",157:"IRON PARAMETERS",158:"Total Iron",159:"Ferritine iron",160:"Transferrin",161:"TIBC",
162:"GTT",163:"OGCT",164:"50G 75G 100G GLUCOSE",165:"ELECTROPHORESIS",166:"Protein electrophoresis",167:"Lipoprotein",
168:"MICROSCOPY",169:"Gram stain",170:"Koh mount",171:"Albert stain",172:"Acid fast stain",173:"Tzanck smear",
174:"Giemsa stain",175:"Smear MP",176:"Smear microfilaria",177:"Hanging drop",178:"Stool ova and cyst",
179:"Modified acid-fast stain",180:"India Ink stain",181:"Toluidine blue O",182:"Automated blood CS",
183:"Automated body fluid CS",184:"Urine CS",185:"Pus CS",186:"Stool CS",187:"Sputum CS",188:"Throat Swab CS",
189:"Cervical High vaginal Swab CS",190:"Conjunctival Swab CS",191:"Skin Hair Nail CS",192:"Others CS",
193:"TPHA",194:"HBsAg",195:"HCV",196:"WIDAL",197:"VDRL RPR",198:"ASLO",199:"RA",200:"Mantoux test",
201:"Well-Felix test",202:"Dengue NS1 IgM IgG",203:"CRP RAPID",204:"Dengue IgM ELISA",205:"Chikungunya IgM ELISA",
206:"JE IgM ELISA",207:"HSV1/2 IgM ELISA",208:"Hepatitis A IgM ELISA",209:"Hepatitis E IgM ELISA",
210:"Mumps IgM ELISA",211:"CMV ELISA",212:"VZV ELISA",213:"Measles ELISA",214:"IgM Leptospira",
215:"IgM Scrub typhus",216:"Rota Virus Ag",217:"IgM Rubella",218:"Hepatitis B PCR",219:"Hepatitis C PCR",
220:"HIV VIRAL LOAD",221:"CD4 COUNT",222:"H1N1 PCR",223:"COVID 19 PCR",224:"CBNAAT M.Tb"
}

sessions={}

def send_msg(to, text):
    token=os.environ.get("WHATSAPP_TOKEN")
    pid=os.environ.get("PHONE_NUMBER_ID")
    if not token or not pid:
        print("MISSING ENV TOKEN OR PID")
        return None
    url=f"https://graph.facebook.com/v19.0/{pid}/messages"
    headers={"Authorization":f"Bearer {token}","Content-Type":"application/json"}
    # WhatsApp limit 4096, split if needed
    for chunk in [text[i:i+3500] for i in range(0, len(text), 3500)]:
        payload={"messaging_product":"whatsapp","to":to,"type":"text","text":{"body":chunk}}
        r=requests.post(url, headers=headers, json=payload)
        print(f"Sent to {to}: {r.status_code} {r.text[:200]}")

@app.route("/webhook", methods=["GET"])
def verify():
    my=os.environ.get("VERIFY_TOKEN","victoria123")
    mode=request.args.get("hub.mode")
    token=request.args.get("hub.verify_token")
    challenge=request.args.get("hub.challenge")
    print(f"Verify attempt mode={mode} token={token}")
    if mode=="subscribe" and token==my:
        print("Verify OK")
        return challenge,200
    print("Verify FAIL")
    return "Forbidden",403

@app.route("/webhook", methods=["POST"])
def incoming():
    data=request.get_json()
    print(f"Incoming: {data}")
    try:
        entry=data['entry'][0]
        changes=entry['changes'][0]['value']
        if 'statuses' in changes:
            return "OK",200
        if 'messages' not in changes:
            return "OK",200

        msg=changes['messages'][0]
        phone=msg['from']
        name=changes['contacts'][0]['profile'].get('name','')
        txt=msg.get('text',{}).get('body','').strip() if msg.get('type')=='text' else ''
        low=txt.lower()

        if low in ["hi","hello","menu","start","hi bot","reset"]:
            sessions[phone]={"step":"ask_name","data":{}}
            send_msg(phone, f"Hi {name} 🙏\n*Victoria Hospital - Infosys Central Lab*\n\nLab Investigation Request Bot 🧪\n\n*Step 1/6* - Enter *Patient Full Name*")
            return "OK",200

        sess=sessions.get(phone)
        if not sess:
            sessions[phone]={"step":"ask_name","data":{}}
            send_msg(phone, "Send *Hi* to start new lab request")
            return "OK",200

        step=sess["step"]
        d=sess["data"]

        if step=="ask_name":
            d["patient_name"]=txt
            sess["step"]="ask_age"
            send_msg(phone, f"*Step 2/6* - Enter Age & Gender\nE.g. 45 M")

        elif step=="ask_age":
            d["age"]=txt
            sess["step"]="ask_uhid"
            send_msg(phone, f"*Step 3/6* - Enter *UHID* No\nIf NEW type NEW")

        elif step=="ask_uhid":
            d["uhid"]=txt.upper()
            sess["step"]="ask_ipid"
            send_msg(phone, "*Step 4/6* - Enter *IPID* / Ward\nIf OPD type OPD")

        elif step=="ask_ipid":
            d["ipid"]=txt.upper()
            sess["step"]="ask_tests"
            # Send short guide, not full 224 (too long)
            guide="*Step 5/6* - Enter Investigations\n\nType numbers e.g. 71,78,88\nOr names e.g. CBC, Creatinine\nOr search e.g. sugar, urine, thyroid\n\n*Popular:* 71 FBS, 73 HbA1c, 78 Creatinine, 88 Bilirubin, 112 TSH, 130 B12, 184 Urine CS\n\nSend your list:"
            send_msg(phone, guide)

        elif step=="ask_tests":
            d["tests_raw"]=txt
            # Parse
            final=[]
            for part in txt.replace(";",",").split(","):
                part=part.strip()
                if not part: continue
                if part.isdigit() and int(part) in ALL_TESTS:
                    final.append(f"{part}. {ALL_TESTS[int(part)]}")
                else:
                    # search by name
                    found=False
                    for num,name in ALL_TESTS.items():
                        if part.lower() in name.lower():
                            final.append(f"{num}. {name}")
                            found=True
                            break
                    if not found:
                        final.append(part)
            d["final"]=final
            sess["step"]="ask_clinical"
            send_msg(phone, f"Selected:\n"+"\n".join(final[:30])+"\n\n*Step 6/6* - Enter Referring Doctor / Unit & Diagnosis\nE.g. Medicine U3 / Fever with jaundice")

        elif step=="ask_clinical":
            d["clinical"]=txt
            order_id=f"VIC{datetime.now().strftime('%d%m%H%M')}"
            summary=f"✅ *Request Submitted* {order_id}\n\nPatient: {d['patient_name']}\nAge: {d['age']}\nUHID: {d['uhid']}\nIPID: {d['ipid']}\nClinical: {d['clinical']}\n\nTests:\n"+"\n".join(d["final"][:40])+"\n\nVictoria Infosys Lab - Report at central lab"
            send_msg(phone, summary)

            staff=f"🧪 *NEW LAB* {order_id}\nWA:{phone} {name}\nPt:{d['patient_name']} {d['age']}\nUHID:{d['uhid']} IPID:{d['ipid']}\nDx:{d['clinical']}\nTests:{', '.join(d['final'][:20])}"
            try:
                send_msg("919980569579", staff)
            except Exception as e:
                print(e)
            sessions.pop(phone,None)

    except Exception as e:
        print(f"Error: {e}")
        import traceback; traceback.print_exc()
    return "OK",200

@app.route("/")
def home():
    return "Victoria Lab Bot Live - 224 Tests + UHID IPID",200

@app.route("/privacy")
def privacy():
    return "Privacy: We only use WhatsApp to collect lab requests for Victoria Hospital",200

if __name__=="__main__":
    app.run(port=10000)
