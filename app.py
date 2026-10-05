# MarvelX Web AI - Glitch Version
from flask import Flask, request
import requests
import os

app = Flask(__name__)

# This one will read from.env file
TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_ID = os.environ.get("PHONE_NUMBER_ID")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")

@app.route('/')
def home():
    return "MarvelX Web AI is LIVE on Glitch! 🚀"

@app.route('/webhook', methods=['GET'])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK VERIFIED!")
        return challenge, 200
    else:
        return "Verification failed", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print(data) # for debugging

    try:
        # Check if na WhatsApp message
        if 'entry' in data and data['entry'][0]['changes'][0]['value'].get('messages'):
            msg = data['entry'][0]['changes'][0]['value']['messages'][0]
            from_number = msg['from']
            text = msg['text']['body']

            print(f"Message from {from_number}: {text}")

            # --- MarvelX AI Logic ---
            lower_text = text.lower()
            if "hello" in lower_text or "hi" in lower_text:
                reply = "Welcome to MarvelX Web AI! 🚀\n\nI be your AI assistant. How I fit help you today?"
            elif "price" in lower_text or "cost" in lower_text:
                reply = "For MarvelX Web AI price, our team go reply you shortly. But wetin you need make I help you with?"
            else:
                reply = f"You talk say: '{text}'\n\nI don receive am for MarvelX Web AI!"

            # Send back to WhatsApp
            url = f"https://graph.facebook.com/v20.0/{PHONE_ID}/messages"
            headers = {
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json"
            }
            payload = {
                "messaging_product": "whatsapp",
                "to": from_number,
                "type": "text",
                "text": {"body": reply}
            }

            r = requests.post(url, headers=headers, json=payload)
            print(r.text)

    except Exception as e:
        print(f"Error: {e}")

    return "ok", 200

if __name__ == '__main__':
    app.run()
