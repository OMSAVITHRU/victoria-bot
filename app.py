from flask import Flask, request
import os, requests
from datetime import datetime
app = Flask(__name__)

ALL_TESTS = {1:"Hb, PCV",2:"Hb, TC, DC",3:"Hb, TC, DC, ALC",4:"Hb Hemoglobin",5:"PCV Packed Cell Volume",6:"RBC Count",7:"TC Total Count",8:"DC Differential Count",9:"TC, DC Total Differential",10:"Platelet Count",11:"Complete Blood Counts",12:"Complete Hemogram",13:"ALC Absolute Lymphocyte Count",14:"AEC Eosinophil Count",15:"Peripheral Smear",16:"Reticulocyte Count",17:"ESR",18:"Bone Marrow Aspiration & Biopsy",19:"Factor VIII Assay",20:"Factor IX Assay",21:"Inhibitor Assay",22:"Bethesda system Inhibitor",23:"Hb electrophoresis",24:"Protein electrophoresis",25:"Urea solubility test",26:"Clot retraction test",27:"Mixing studies",28:"MPO",29:"Immunofluorescence direct",30:"LE Cells",31:"Osmotic fragility tests",32:"Prothrombin time",33:"APTT",34:"D-dimer",35:"Fibrinogen",36:"Sickling test",37:"Urine routine",38:"Urine analysis",39:"BT CT",40:"Urine bile salts and pigments",41:"Urine Ketone bodies",42:"24 hrs Urine protein",43:"Semen Analysis",44:"Stool routine",45:"Stool reducing substances",46:"Stool occult blood",47:"FNAC USG guided",48:"Fluid cell count and cell type",49:"CSF ASCITIC FLUID",50:"PLEURAL FLUID",51:"SYNOVIAL BAL FLUID",52:"DRAIN FLUID SPUTUM",53:"Cytology malignant cells",54:"Pap smear",55:"Tzanck smear acantholyigic",56:"Scrapings touch smear",57:"Cytology IHC",58:"Urine malignant cells",59:"Biopsy big",60:"Biopsy Medium",61:"Biopsy small",62:"IHC each marker",63:"Second opinion HPE",64:"NSE",65:"PAS",66:"AchE stain Hirschsprung",67:"Frozen section",68:"Perinatal autopsy",69:"Cell block",70:"DIABETIC HEALTH",71:"FBS PPBS",72:"RBS",73:"HBA1C",74:"C-peptide",75:"Insulin",76:"GAD Antibodies",77:"RENAL FUNCTION TEST",78:"Creatinine",79:"Uric acid",80:"Blood urea BUN",81:"Calcium total",82:"Calcium Ionized",83:"Phosphorus",84:"Electrolytes NA/K/CI",85:"Cystatin C",86:"eGFR",87:"LIVER FUNCTION TEST",88:"Total billirubin",89:"Direct Billirubin",90:"Total protein",91:"Albumin",92:"Globulin",93:"SGOT AST",94:"SGPT ALT",95:"Alkaline phosphatase ALP",96:"GGT",97:"5 Nucleotidase",98:"LIPID PROFILE LP",99:"Total Cholesterol",100:"HDL Cholesterol",101:"LDL Cholesterol",102:"VLDL Cholesterol",103:"Triglycerides",104:"CARDIAC PROFILE",105:"LDH",106:"CK MB STAT",107:"CK TOTAL",108:"TROP T",109:"TROP I",110:"Lp(a)",111:"Total homocysteine",112:"T3 T4 TSH",113:"fT3 fT4",114:"FSH LH",115:"Prolactin",116:"Total testosterone",117:"Free testosterone",118:"17-OH PROGESTERONE",119:"Progesterone",120:"Cortisol",121:"Intact PTH",122:"Growth Hormone",123:"Beta HCG",124:"Ammonia",125:"Magnesium",126:"Serum amylase",127:"Serum lipase",128:"Pseudocholline esterase",129:"Ferritin",130:"Vit B12",131:"Vit D",132:"Folate",133:"ADA",134:"Lithium",135:"CRP",136:"CSF ASCITIC PLEURAL",137:"SYNOVIAL",138:"Sugar",139:"Protein",140:"Chloride",141:"Others",142:"URINE PANEL",143:"Spot Urine",144:"Spot urine creatinine",145:"Spot Urine Electrolytes",146:"Urine others",147:"Urine PCR",148:"Urine ACR",149:"24 hour urine protein",150:"24 hour urine creatinine",151:"Others urine",152:"TUMOR MARKERS",153:"CA-125",154:"CEA",155:"AFP",156:"PSA total free",157:"IRON PARAMETERS",158:"Total Iron",159:"Ferritine iron",160:"Transferrin",161:"TIBC",162:"GTT",163:"OGCT",164:"50G 75G 100G GLUCOSE",165:"ELECTROPHORESIS",166:"Protein electrophoresis",167:"Lipoprotein",168:"MICROSCOPY",169:"Gram stain",170:"Koh mount",171:"Albert stain",172:"Acid fast stain",173:"Tzanck smear",174:"Giemsa stain",175:"Smear MP",176:"Smear microfilaria",177:"Hanging drop",178:"Stool ova and cyst",179:"Modified acid-fast stain",180:"India Ink stain",181:"Toluidine blue O",182:"Automated blood CS",183:"Automated body fluid CS",184:"Urine CS",185:"Pus CS",186:"Stool CS",187:"Sputum CS",188:"Throat Swab CS",189:"Cervical High vaginal Swab CS",190:"Conjunctival Swab CS",191:"Skin Hair Nail CS",192:"Others CS",193:"TPHA",194:"HBsAg",195:"HCV",196:"WIDAL",197:"VDRL RPR",198:"ASLO",199:"RA",200:"Mantoux test",201:"Well-Felix test",202:"Dengue NS1 IgM IgG",203:"CRP RAPID",204:"Dengue IgM ELISA",205:"Chikungunya IgM ELISA",206:"JE IgM ELISA",207:"HSV1/2 IgM ELISA",208:"Hepatitis A IgM ELISA",209:"Hepatitis E IgM ELISA",210:"Mumps IgM ELISA",211:"CMV ELISA",212:"VZV ELISA",213:"Measles ELISA",214:"IgM Leptospira",215:"IgM Scrub typhus",216:"Rota Virus Ag",217:"IgM Rubella",218:"Hepatitis B PCR",219:"Hepatitis C PCR",220:"HIV VIRAL LOAD",221:"CD4 COUNT",222:"H1N1 PCR",223:"COVID 19 PCR",224:"CBNAAT M.Tb"}

PRICES = {1:50,2:80,3:100,4:30,5:30,6:50,7:50,8:80,9:80,10:50,11:300,12:350,13:50,14:50,15:150,16:100,17:50,18:2000,19:1500,20:1500,21:1000,22:1000,23:500,24:500,25:200,26:200,27:800,28:300,29:400,30:200,31:300,32:200,33:250,34:600,35:400,36:100,37:50,38:50,39:100,40:100,41:100,42:150,43:100,44:50,45:50,46:100,47:600,48:200,49:200,50:200,51:200,52:200,53:400,54:300,55:200,56:200,57:800,58:400,59:2000,60:1500,61:800,62:800,63:500,64:200,65:200,66:500,67:1500,68:3000,69:400,70:0,71:60,72:40,73:300,74:400,75:400,76:800,77:0,78:80,79:80,80:80,81:80,82:150,83:80,84:200,85:600,86:0,87:0,88:80,89:80,90:80,91:80,92:80,93:80,94:80,95:100,96:150,97:200,98:0,99:80,100:80,101:80,102:80,103:80,104:0,105:100,106:300,107:100,108:600,109:600,110:500,111:500,112:250,113:300,114:300,115:200,116:250,117:350,118:400,119:250,120:250,121:500,122:400,123:300,124:300,125:80,126:150,127:150,128:200,129:250,130:300,131:400,132:250,133:200,134:200,135:200,136:200,137:200,138:80,139:80,140:80,141:100,142:0,143:80,144:80,145:100,146:100,147:200,148:200,149:200,150:200,151:100,152:0,153:400,154:400,155:400,156:400,157:0,158:100,159:250,160:200,161:200,162:400,163:200,164:200,165:0,166:300,167:300,168:0,169:100,170:100,171:100,172:150,173:100,174:100,175:100,176:100,177:100,178:100,179:150,180:150,181:150,182:800,183:800,184:400,185:400,186:400,187:400,188:400,189:400,190:400,191:400,192:400,193:200,194:100,195:100,196:100,197:100,198:150,199:150,200:200,201:200,202:300,203:150,204:500,205:500,206:500,207:500,208:500,209:500,210:500,211:500,212:500,213:500,214:500,215:500,216:400,217:500,218:2000,219:2000,220:2500,221:800,222:3000,223:1500,224:1000}

# ===== FLAG UNAVAILABLE TESTS HERE =====
UNAVAILABLE = {18,19,20,21,22,62,68,218,219,220,222} # Edit this list

sessions={}

def send_msg(to, text):
    token=os.environ.get("WHATSAPP_TOKEN"); pid=os.environ.get("PHONE_NUMBER_ID")
    url=f"https://graph.facebook.com/v19.0/{pid}/messages"
    headers={"Authorization":f"Bearer {token}","Content-Type":"application/json"}
    for c in [text[i:i+3000] for i in range(0,len(text),3000)]:
        requests.post(url, headers=headers, json={"messaging_product":"whatsapp","to":to,"type":"text","text":{"body":c}})

def parse_tests(tests_raw):
    tests_raw_clean = tests_raw.replace(",", " ")
    parts = tests_raw_clean.split()
    total=0; details=[]; nums=[]; unavailable_found=[]
    for part in parts:
        part=part.strip()
        if not part: continue
        if part.isdigit() and int(part) in ALL_TESTS:
            num=int(part)
            if num in UNAVAILABLE:
                unavailable_found.append(f"{num}. {ALL_TESTS[num]} - UNAVAILABLE")
                continue
            price=PRICES.get(num,0); total+=price; nums.append(str(num))
            details.append(f"{num}. {ALL_TESTS[num]} - Rs.{price}")
        else:
            # name search
            for num,n in ALL_TESTS.items():
                if part.lower() in n.lower():
                    if num in UNAVAILABLE:
                        unavailable_found.append(f"{num}. {n} - UNAVAILABLE")
                        break
                    price=PRICES.get(num,0); total+=price; nums.append(str(num))
                    details.append(f"{num}. {n} - Rs.{price}")
                    break
    return total, details, nums, unavailable_found

MENU_MSG = """Reply with:
F1 - Book lab tests (label format)
F2 - Book lab tests (line-by-line)
F3 - View all 224 tests with price"""

F1_TEMPLATE = """*Victoria Lab - F1 Format - Send ONE message like this:*

Name: Ramesh Kumar
Age: 45
Sex: M
UHID: 12345678999
IPID: 123456
Tests: 71 78 88 112
Dr: Medicine
Diagnosis/Remarks: Fever

Tests: use space - 71 78 88
Copy, fill & send 👆"""

F2_TEMPLATE = """*Victoria Lab - F2 Format - Send details line-by-line:*

Name:
Age:
Sex:
UHID:
IPID:
Tests:
Dr:
Diagnosis/Remarks:

*Example - Copy & fill:*
Ramesh Kumar
45 y
M
12345678999
123456
71 78 88 112
Med U3
Fever - Patient will be allocated UHID first and investigations are advised only after registration and allocation of UHID.

Send 8 lines in order 👆"""

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token")==os.environ.get("VERIFY_TOKEN","victoria123"):
        return request.args.get("hub.challenge"),200
    return "Forbidden",403

@app.route("/webhook", methods=["POST"])
def incoming():
    data=request.get_json()
    try:
        val=data['entry'][0]['changes'][0]['value']
        if 'messages' not in val: return "OK",200
        m=val['messages'][0]; phone=m['from']; prof=val['contacts'][0]['profile'].get('name','')
        txt=m.get('text',{}).get('body','').strip() if m.get('type')=='text' else ''
        low=txt.lower()

        # FIRST MESSAGE - SHOW MENU
        if low in ["hi","hello","start","menu","reset","hey"]:
            sessions[phone]={"step":"await_f","data":{}}
            send_msg(phone, f"Hi {prof} 🙏\n*Welcome to Victoria Hospital Infosys Lab*\n\n{MENU_MSG}")
            return "OK",200

        sess=sessions.get(phone)
        if not sess:
            sessions[phone]={"step":"await_f","data":{}}
            send_msg(phone, f"Hi {prof} 🙏\n*Welcome to Victoria Hospital Infosys Lab*\n\n{MENU_MSG}")
            return "OK",200

        step=sess["step"]; d=sess["data"]

        if step=="await_f":
            if low=="f1":
                sess["step"]="f1_input"; send_msg(phone, F1_TEMPLATE)
            elif low=="f2":
                sess["step"]="f2_input"; send_msg(phone, F2_TEMPLATE)
            elif low=="f3":
                # Send list in chunks
                full="*ALL 224 INVESTIGATIONS WITH PRICE:*\n"
                for num in range(1,225):
                    name=ALL_TESTS[num]; price=PRICES.get(num,0)
                    flag=" ❌ UNAVAILABLE" if num in UNAVAILABLE else ""
                    full+=f"{num}. {name} - Rs.{price}{flag}\n"
                    if len(full)>2800:
                        send_msg(phone, full); full=""
                if full: send_msg(phone, full)
                send_msg(phone, f"\n{MENU_MSG}")
            else:
                send_msg(phone, f"Please reply only *F1* or *F2* or *F3*\n\n{MENU_MSG}")
            return "OK",200

        # F1 - label format Name: etc
        if step=="f1_input":
            parsed={}
            for l in txt.split("\n"):
                if ":" in l:
                    k,v=l.split(":",1); parsed[k.strip().lower()]=v.strip()
            pname=parsed.get("name",""); age=parsed.get("age",""); sex=parsed.get("sex","")
            uhid=parsed.get("uhid",""); ipid=parsed.get("ipid","")
            tests_raw=parsed.get("tests",""); dr=parsed.get("dr",""); diag=parsed.get("diagnosis/remarks", parsed.get("diagnosis",""))

            total, details, nums, una = parse_tests(tests_raw)
            d.update({"pname":pname,"age":age,"sex":sex,"uhid":uhid,"ipid":ipid,"tests_raw":tests_raw,"dr":dr,"diag":diag,"total":total,"details":details,"nums":nums,"una":una})

            bill="\n".join(details) if details else "No valid tests"
            una_msg="\n⚠️ *Unavailable:*\n"+"\n".join(una) if una else ""
            summary=f"*Confirm Details:*\n\nPatient: {pname}\nAge: {age}\nSex: {sex}\nUHID: {uhid}\nIPID: {ipid}\nDr: {dr}\nDiagnosis: {diag}\n\n{bill}\n*TOTAL: Rs.{total}*"+una_msg+"\n\nIf correct type *YES* to book\nIf wrong, send corrected format again"
            sess["step"]="confirm"
            send_msg(phone, summary)
            return "OK",200

        # F2 - line by line 8 lines
        if step=="f2_input":
            lines=[l.strip() for l in txt.split("\n") if l.strip()!=""]
            if len(lines)<6:
                send_msg(phone, "Please send 8 lines like example:\n"+F2_TEMPLATE)
                return "OK",200
            # map 8 lines
            # Expected: Name, Age, Sex, UHID, IPID, Tests, Dr, Diagnosis
            pname=lines[0] if len(lines)>0 else ""
            age=lines[1] if len(lines)>1 else ""
            sex=lines[2] if len(lines)>2 else ""
            uhid=lines[3] if len(lines)>3 else ""
            ipid=lines[4] if len(lines)>4 else ""
            tests_raw=lines[5] if len(lines)>5 else ""
            dr=lines[6] if len(lines)>6 else ""
            diag=" ".join(lines[7:]) if len(lines)>7 else ""

            total, details, nums, una = parse_tests(tests_raw)
            d.update({"pname":pname,"age":age,"sex":sex,"uhid":uhid,"ipid":ipid,"tests_raw":tests_raw,"dr":dr,"diag":diag,"total":total,"details":details,"nums":nums,"una":una})

            bill="\n".join(details) if details else "No valid tests"
            una_msg="\n⚠️ *Unavailable:*\n"+"\n".join(una) if una else ""
            summary=f"*Confirm Details:*\n\nPatient: {pname}\nAge: {age}\nSex: {sex}\nUHID: {uhid}\nIPID: {ipid}\nDr: {dr}\nDiagnosis: {diag}\n\n{bill}\n*TOTAL: Rs.{total}*"+una_msg+"\n\nIf correct type *YES* to book\nIf wrong, send 8 lines again corrected"
            sess["step"]="confirm"
            send_msg(phone, summary)
            return "OK",200

        if step=="confirm":
            if low in ["yes","y","confirm","book","ok","correct"]:
                order_id=f"VIC{datetime.now().strftime('%d%m%H%M')}"
                bill="\n".join(d["details"])
                final=f"✅ *Lab Request Booked* {order_id}\n\nPatient: {d['pname']}\nAge: {d['age']}\nSex: {d['sex']}\nUHID: {d['uhid']}\nIPID: {d['ipid']}\nDr: {d['dr']}\nDiagnosis: {d['diag']}\n\n{bill}\n\n*TOTAL: Rs.{d['total']}*\n\nVictoria Infosys Lab - Report at lab counter"
                send_msg(phone, final)

                staff=f"🧪 *NEW BOOKING* {order_id}\nWA:{phone}\nPt:{d['pname']} Age:{d['age']} Sex:{d['sex']}\nUHID:{d['uhid']} IPID:{d['ipid']}\nTests: {' '.join(d['nums'])} Rs.{d['total']}\nDr:{d['dr']} Dx:{d['diag']}"
                if d["una"]: staff+="\nUNAVAIL TRIED: "+", ".join(d["una"])
                try: send_msg("919980569579", staff)
                except: pass
                sessions.pop(phone,None)
            else:
                # treat as correction - go back to input
                send_msg(phone, "Send corrected details again in same format (F1 or F2)\nOr type YES to confirm previous.")
                sess["step"]="await_f"
                send_msg(phone, MENU_MSG)
            return "OK",200

    except Exception as e:
        print(e); import traceback; traceback.print_exc()
    return "OK",200

@app.route("/")
def home(): return "Victoria F1 F2 F3 Menu Live",200
