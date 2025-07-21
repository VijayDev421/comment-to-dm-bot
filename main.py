from flask import Flask, request
import requests

app = Flask(__name__)

VERIFY_TOKEN = "taravi2025bot"  # Use the same token you gave in Meta
ACCESS_TOKEN = "EAAi2uqLZBOGEBPHVdrmHLQSOTUfCIYuDl8ZCaYp72ZBw8E8dq5gQ2RFRKARjX5cnTzIkGy7GIMwEmP01x6gXEAZCXGTCLS6WgbmMFAqs0vaZAgDZBD14bhZBURPtYqgEURZATFpZAKIUDFT1NQC2trUFaSyMonQArAMutYsShakAm8YEhRM8ZBNotmUl4lxmb57duta74VpH0yR5U1nexZBbgvqKNkLEyZAh9w3maQZDZD" 

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
                send_dm(sender_id, pdf_url="https://drive.google.com/file/d/1-7ck6TJMxKMFAXmtGX_vrb_YsquJTd13/view?usp=sharing")

    except Exception as e:
        print("Error processing webhook:", e)

    return "OK", 200

# Function to send DM using Instagram Messaging API
def send_dm(user_id, message_text=None, pdf_url=None):
    url = "https://graph.facebook.com/v19.0/me/messages"
    headers = {
        "Content-Type": "application/json"
    }

    if pdf_url:
        payload = {
            "recipient": {
                "id": user_id
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": [
                            {
                                "title": "Here's your requested PDF!",
                                "subtitle": "Tap below to open the document",
                                "image_url": "https://cdn-icons-png.flaticon.com/512/337/337946.png",  # Optional
                                "default_action": {
                                    "type": "web_url",
                                    "url": pdf_url
                                },
                                "buttons": [
                                    {
                                        "type": "web_url",
                                        "url": pdf_url,
                                        "title": "Open PDF"
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }
    else:
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
