app = Flask(__name__)
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "victoria_secret_123")

@app.route('/')
def home():
    return "Victoria Bot Live - Puttur"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Verification failed", 403
    
    if request.method == 'POST':
        print("Message received:", request.get_json())
        return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
