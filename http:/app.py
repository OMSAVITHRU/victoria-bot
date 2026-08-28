import os, json
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "victoria_secret_123")

DB_FILE = "data.json"
def load_db():
    try:
        import json
        with open(DB_FILE) as f: return json.load(f)
    except: return {"doctors": [], "labs": [], "orders": []}
def save_db(db):
    with open(DB_FILE, "w") as f: json.dump(f, db, indent=2)

@app.route("/")
def home(): return "Victoria Bot Live"

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Invalid", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    print(request.json)
    return jsonify({"status":"ok"})

@app.route("/admin")
def admin():
    db = load_db()
    return f"<h2>Victoria Hospital Admin</h2><p>Labs: {db['labs']}</p><p>Doctors: {db['doctors']}</p><form method=post action=/admin/add_lab>Lab Name<input name=name> Phone<input name=phone><button>Add</button></form>"

@app.route("/admin/add_lab", methods=["POST"])
def add_lab():
    db=load_db(); db["labs"].append({"name":request.form["name"],"phone":request.form["phone"]}); save_db(db); return "Added <a href=/admin>Back</a>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
