import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Target details
TARGET_NAME = "glo mbg"
DEFAULT_MESSAGE = "selamat pagi"

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "running", "service": "WhatsApp Cloud Scheduler Bot"})

@app.route("/send-scheduled-msg", methods=["POST", "GET"])
def send_msg():
    """
    Triggered by Google Cloud Scheduler every morning at 07:00 AM.
    """
    msg = request.args.get("message", DEFAULT_MESSAGE)
    target = request.args.get("target", TARGET_NAME)
    
    print(f"[CLOUD BOT] Sending '{msg}' to '{target}'...")
    
    # Place API integration endpoint here (e.g., Green API / WhatsApp Cloud Webhook)
    # response = requests.post(API_URL, json={"to": target, "body": msg})
    
    return jsonify({
        "success": True,
        "recipient": target,
        "message": msg,
        "status": "Scheduled message triggered successfully"
    }), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
