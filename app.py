from flask import Flask, request
import os, requests
from datetime import datetime

app = Flask(__name__)

ALL_TESTS = {
1:"Hb, PCV",2:"Hb, TC, DC",3:"Hb, TC, DC, ALC",4:"Hb : Hemoglobin",5:"PCV : Packed Cell Volume",
6:"RBC Count",7:"TC : Total Count",8:"DC : Differential Count",9:"TC, DC - Total Count, Differential Count",
10:"Platelet Count",11:"Complete Blood Counts",12:"Complete Hemogram",13:"ALC : Absolute Lymphocyte Count",
14:"AEC : Eosinophil Count",15:"Peripheral Smear",16:"Reticulocyte Count",17:"ESR",
18:"Bone Marrow Aspiration & Biopsy",19:"Factor VIII Assay",20:"Factor IX Assay",21:"Inhibitor Assay",
22:"Bethesda system for Inhibitor",23:"Hb electrophoresis",24:"Protein electrophoresis",25:"Urea solubility test",
26:"Clot retraction test",27:"Mixing studies",28:"MPO",29:"Immunofluorescence - direct",30:"LE Cells",
31:"Osmotic fragility tests",32:"Prothrombin time",33:"Activated partial thrombin time",34:"D-dimer",
35:"Fibrinogen",36:"Sickling test",37:"Urine routine",38:"Urine analysis",39:"BT, CT",
40:"Urine bile salts and pigments",41:"Urine Ketone bodies",42:"24 hrs. Urine protein",43:"Semen Analysis",
44:"Stool routine",45:"Stool for reducing substances",46:"Stool for occult blood",47:"FNAC USG guided / without guidance",
48:"Fluid cell count and cell type",49:"CSF ASCITIC FLUID",50:"PLEURAL FLUID",51:"SYNOVIAL FLUID BAL FLUID",
52:"DRAIN FLUID SPUTUM",53:"Cytology for malignant cells",54:"Pap smear examination",
55:"Tzanck smear for acantholyigic cells",56:"Scrapings / touch smear",57:"Cytology IHC",58:"Urine for malignant cells",
59:"Biopsy (big)",60:"Biopsy (Medium)",61:"Biopsy (small)",62:"IHC (each marker)",63:"Second opinion HPE",
64:"NSE",65:"PAS",66:"AchE stain for Hirschsprung",67:"Frozen section",68:"Perinatal autopsy",69:"Cell block",
70:"DIABETIC HEALTH",71:"FBS, PPBS",72:"RBS",73:"HBA1C",74:"C-peptide",75:"Insulin",76:"GAD Antibodies",
77:"RENAL FUNCTION TEST",78:"Creatinine",79:"Uric acid",80:"Blood urea / BUN",81:"Calcium total",
82:"Calcium Ionized",83:"Phosphorus",84:"Electrolytes / NA/K/CI",85:"Cystatin C",86:"eGFR",
87:"LIVER FUNCTION TEST",88:"Total billirubin",89:"Direct Billirubin",90:"Total protein",91:"Albumin",92:"Globulin",
93:"SGOT/AST",94:"SGPT/ALT",95:"Alkaline phosphatase/ALP",96:"GGT",97:"5 Nucleotidase",98:"LIPID PROFILE (LP)",
99:"Total Cholesterol",100:"HDP Cholesterol",101:"LDL Cholesterol",102:"VLDL Cholesterol",103:"Triglycerides",
104:"CARDIAC PROFILE",105:"LDH",106:"CK MB STAT/LPG MB",107:"CK (TOTAL)",108:"TROP - T",109:"TROP - I",
110:"Lp(a)",111:"Total homocysteine",112:"T3, T4, TSH",113:"fT3, fT4",114:"FSH LH",115:"Prolactin",
116:"Total testosterone",117:"Free testosterone",118:"17-OH PROGESTERONE",119:"Progesterone",120:"Cortisol",
121:"Intact PTH",122:"Growth Hormone",123:"β HCG",124:"Ammonia",125:"Magnesium",126:"Serum amylase",
127:"Serum lipase",128:"Pseudocholline esterase",129:"Ferritin",130:"Vit B12",131:"Vit D",132:"Folate",
133:"ADA",134:"Lithium",135:"CRP",136:"CSF ASCITIC PLEURAL",137:"SYNOVIAL",138:"Sugar",139:"Protein",
140:"Chloride",141:"Others",142:"URINE PANEL",143:"Spot Urine",144:"Spot urine creatinine",
145:"Spot Urine Electrolytes",146:"Urine others",147:"Urine Protein Creatinine Ration (PCR)",
148:"Urine Albumin Ratio (ACR)",149:"24 hour urine protein",150:"24 hour urine creatinine",151:"Others",
152:"TUMOR MARKETS",153:"CA-125",154:"CEA",155:"α feto protein",156:"PSA - total / free",157:"IRON PARAMETERS",
158:"Total Iron",159:"Ferritine",160:"Transferrin",161:"TIBC",162:"GTT",163:"OGCT",164:"50G/75G/100G GLUCOSE",
165:"ELECTROPHORESIS",166:"Protein",167:"Lipoprotein",168:"MICROSCOPY",169:"Gram stain",170:"Koh mount",
171:"Albert's stain",172:"Acid fast stain",173:"Tzanck smear",174:"Glemsa stain",175:"Smear for MP",
176:"Smear for microfilaria",177:"Hanging drop",178:"Stool for ova and cyst",179:"Modified acid-fast stain",
180:"India Ink stain",181:"Toluidine blue O",182:"Automated blood C/S",183:"Automated body fluid C/S",
184:"Urine C/S",185:"Pus C/S",186:"Stool C/S",187:"Sputum C/S",188:"Throat Swab C/S",
189:"Cervical / High vaginal Swab C/S",190:"Conjunctival Swab C/S",191:"Skin / Hair / Nail C/S",192:"Others (Specify)",
193:"TPHA",194:"HBsAg",195:"HCV",196:"WIDAL",197:"VDRL/RPR",198:"ASLO",199:"RA",200:"Mantoux test",
201:"Well-Felix test",202:"Dengue NS1 / IgM/IgG",203:"CRP RAPID",204:"Dengue IgM ELISA",205:"Chikungunya IgM ELISA",
206:"JE IgM ELISA",207:"HSV1/2 IgM ELISA",208:"Hepatitis A IgM ELISA",209:"Hepatitis E IgM ELISA",
210:"Mumps IgM ELISA",211:"CMV ELISA",212:"VZV ELISA",213:"Measles ELISA",214:"IgM ELISA for Leptospira",
215:"IgM ELISA for Scrub typhus",216:"Ag DETECTION FOR ROTA Virus",217:"IgM ELISA for Rubella",
218:"Hepatitis B PCR",219:"Hepatitis C PCR",220:"HIV VIRAL LOAD",221:"CD 4 COUNT",222:"H1N1 PCR",
223:"COVID 19 PCR",224:"CBNAAT FOR M.Tb."
}

sessions={}

def send_msg(to, text):
    token=os.environ.get("WHATSAPP_TOKEN")
    pid=os.environ.get("PHONE_NUMBER_ID")
    url=f"https://graph.facebook.com/v19.0/{pid}/messages"
    headers={"Authorization":f"Bearer {token}","Content-Type":"application/json"}
    # Split long messages for WhatsApp limit
    if len(text)>3500:
        for i in range(0,len(text),3000):
            payload={"messaging_product":"whatsapp","to":to,"type":"text","text":{"body":text[i:i+3000]}}
            requests.post(url, headers=headers, json=payload)
        return
    payload={"messaging_product":"whatsapp","to":to,"type":"text","text":{"body":text}}
    requests.post(url, headers=headers, json=payload)

def search_tests(q):
    q=q.lower()
    res=[]
    for num,name in ALL_TESTS.items():
        if q in name.lower() or q==str(num):
            res.append(f"{num}. {name}")
    return res[:20]

@app.route("/webhook", methods=["GET"])
def verify():
    my_token=os.environ.get("VERIFY_TOKEN","victoria123")
    if request.args.get("hub.mode")=="subscribe" and request.args.get("hub.verify_token")==my_token:
        return request.args.get("hub.challenge"),200
    return "Forbidden",403

@app.route("/webhook", methods=["POST"])
def incoming():
    data=request.json
    print(data)
    try:
        val=data['entry'][0]['changes'][0]['value']
        if 'statuses' in val: return "OK",200
        if 'messages' not in val: return "OK",200
        m=val['messages'][0]
        phone=m['from']
        profile=val['contacts'][0]['profile'].get('name','')
        text=m.get('text',{}).get('body','').strip() if m['type']=='text' else ''
        low=text.lower()

        if low in ["hi","hello","menu","start","reset"]:
            sessions[phone]={"step":"ask_name","data":{}}
            send_msg(phone, f"Hi {profile} 🙏 *Victoria Hospital Lab - BMCRI*\n\nThis is Lab Investigation Request Bot.\n\n*Step 1/6* - Enter *Patient Full Name*:")
            return "OK",200

        sess=sessions.get(phone)
        if not sess:
            sessions[phone]={"step":"ask_name","data":{}}
            send_msg(phone, "Send *Hi* to start lab request")
            return "OK",200

        step=sess["step"]; d=sess["data"]

        if step=="ask_name":
            d["patient_name"]=text
            sess["step"]="ask_age"
            send_msg(phone, f"*Step 2/6* - Age & Gender of {text}?\nE.g. 45 M or 30 F")

        elif step=="ask_age":
            d["age_gender"]=text
            sess["step"]="ask_uhid"
            send_msg(phone, "*Step 3/6* - Enter *UHID* (Hospital No.)?\nIf NEW patient type NEW")

        elif step=="ask_uhid":
            d["uhid"]=text.upper()
            sess["step"]="ask_ipid"
            send_msg(phone, "*Step 4/6* - Enter *IPID* (IP No / Ward)?\nIf OPD type OPD or NA")

        elif step=="ask_ipid":
            d["ipid"]=text.upper()
            sess["step"]="ask_tests"
            send_msg(phone, f"*Step 5/6* - Enter Investigations\n\nYou can type:\n- Numbers: e.g. 71,78,88\n- Names: e.g. CBC, Creatinine, FBS\n- Search: e.g. type *sugar* to find tests\n\n*Tip:* Send comma separated list.\n\nType a test name to search, or full list numbers:")

        elif step=="ask_tests":
            # If user searches
            if len(text)<15 and not "," in text and text not in ["done","book"]:
                matches=search_tests(text)
                if matches:
                    send_msg(phone, f"Found for '{text}':\n"+"\n".join(matches)+"\n\nAdd numbers like 71,78 or type more names. When finished type DONE")
                    # stay in same step but save partial
                    d.setdefault("tests_raw_list", []).append(text)
                    return "OK",200
            if low in ["done","finish","book"]:
                # finalize
                raw=",".join(d.get("tests_raw_list",[])+[d.get("last", "")])
            else:
                d["last"]=text
                d.setdefault("tests_raw_list", []).append(text)
                # parse final list
                final_tests=[]
                for item in ",".join(d["tests_raw_list"]).replace(";",",").split(","):
                    item=item.strip()
                    if not item: continue
                    if item.isdigit() and int(item) in ALL_TESTS:
                        final_tests.append(f"{item}. {ALL_TESTS[int(item)]}")
                    else:
                        # try name match
                        ms=search_tests(item)
                        if ms:
                            final_tests.append(ms[0])
                        else:
                            final_tests.append(item)
                d["final_tests"]=final_tests
                sess["step"]="ask_clinical"
                send_msg(phone, f"Selected:\n"+"\n".join(final_tests[:30]) + f"\n\n*Step 6/6* - Enter *Referring Dr / Unit & Provisional Diagnosis*?\nE.g. Medicine Unit 3 / Fever")
                return "OK",200

        elif step=="ask_clinical":
            d["clinical"]=text
            # Final booking
            order_id=f"VIC{datetime.now().strftime('%d%m%H%M')}"
            summary = f"✅ *Lab Request Submitted* {order_id}\n\nPatient: {d['patient_name']}\nAge/Gender: {d['age_gender']}\nUHID: {d['uhid']}\nIPID/Ward: {d['ipid']}\nDiagnosis: {d['clinical']}\n\n*Investigations:*\n"+"\n".join(d['final_tests'][:40])+"\n\nVictoria Hospital - Infosys Central Lab\nReport will be available at lab."
            send_msg(phone, summary)

            staff_msg = f"🧪 *NEW LAB REQUEST* {order_id}\nFrom WA: {phone} {profile}\nPt: {d['patient_name']} {d['age_gender']}\nUHID:{d['uhid']} IPID:{d['ipid']}\nDr/Dx: {d['clinical']}\nTests:\n"+"\n".join(d['final_tests'][:50])
            try:
                send_msg("919980569579", staff_msg)
            except: pass
            sessions.pop(phone,None)

    except Exception as e:
        print(e); import traceback; traceback.print_exc()
    return "OK",200

@app.route("/")
def home(): return "Victoria Lab Request Bot - 224 Tests + UHID/IPID Live",200
