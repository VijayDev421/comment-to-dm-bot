from flask import Flask, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
IG_USER_ID = os.getenv("IG_USER_ID")

@app.route("/", methods=["GET"])
def home():
    return "✅ Insta Comment to DM Bot is Live"

# Webhook verification (required by Meta)
@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("🔒 Webhook verified successfully")
        return challenge, 200
    else:
        return "Verification failed", 403

# Webhook event handler
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📥 Webhook Received:", data)

    if data.get("entry"):
        for entry in data["entry"]:
            changes = entry.get("changes", [])
            for change in changes:
                value = change.get("value", {})
                if value.get("field") == "comments":
                    comment_text = value.get("text", "")
                    user_id = value.get("from", {}).get("id")
                    if "pdf" in comment_text.lower():
                        send_dm(user_id, "Here’s your free PDF as promised! 📄")

    return "Event Received", 200

# Function to send DM
def send_dm(recipient_id, message_text):
    url = f"https://graph.facebook.com/v18.0/{IG_USER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text},
        "messaging_type": "RESPONSE"
    }
    response = requests.post(url, json=payload, headers=headers)
    print("📤 DM Send Response:", response.json())

if __name__ == "__main__":
    app.run(debug=True)
