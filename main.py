from flask import Flask, request
import requests

app = Flask(__name__)

VERIFY_TOKEN = "your_webhook_verify_token"  # Use the same token you gave in Meta
ACCESS_TOKEN = "your_long_lived_page_access_token"  # Replace this with the real one

# Webhook verification (GET)
@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK VERIFIED")
        return challenge, 200
    else:
        return "Verification failed", 403

# Webhook to receive Instagram comment events (POST)
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Received webhook:", data)

    try:
        changes = data['entry'][0]['changes'][0]
        if changes['field'] == 'comments':
            comment_text = changes['value']['text']
            sender_id = changes['value']['from']['id']
            username = changes['value']['from']['username']

            print(f"Comment from @{username}: '{comment_text}' (ID: {sender_id})")

            # Trigger keyword check
            if "send" in comment_text.lower():
                send_dm(sender_id, f"Hi @{username}, here is the info you requested! 💌")
    except Exception as e:
        print("Error processing webhook:", e)

    return "OK", 200

# Function to send DM using Instagram Messaging API
def send_dm(user_id, message_text):
    url = "https://graph.facebook.com/v19.0/me/messages"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_type": "RESPONSE",
        "recipient": {
            "id": user_id
        },
        "message": {
            "text": message_text
        }
    }
    params = {
        "access_token": ACCESS_TOKEN
    }

    response = requests.post(url, headers=headers, json=payload, params=params)
    print("DM sent:", response.status_code, response.text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
