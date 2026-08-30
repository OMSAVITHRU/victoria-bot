@app.route("/webhook", methods=["GET"])
def verify():
    print(f"ALL ARGS: {dict(request.args)}")
    challenge = request.args.get("hub.challenge")
    if challenge:
        return challenge, 200
    return "OK", 200
