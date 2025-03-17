import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()  # Charge les variables d'environnement

app = Flask(__name__)
CORS(app)

MAILJET_API_KEY = os.getenv("MJ_APIKEY_PUBLIC")
MAILJET_API_SECRET = os.getenv("MJ_APIKEY_PRIVATE")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")


@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json()

    # Vérification des champs requis
    required_fields = ["recipientEmail", "recipientName", "subject", "text"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({"success": False, "error": f"Champs manquants: {', '.join(missing_fields)}"}), 400

    recipient_email = data["recipientEmail"]
    recipient_name = data["recipientName"]
    subject = data["subject"]
    text = data["text"]
    html = data.get("html", text)

    mailjet_url = "https://api.mailjet.com/v3.1/send"
    headers = {"Content-Type": "application/json"}
    payload = {
        "Messages": [
            {
                "From": {"Email": SENDER_EMAIL, "Name": "Moi"},
                "To": [{"Email": recipient_email, "Name": recipient_name}],
                "Subject": subject,
                "TextPart": text,
                "HTMLPart": html
            }
        ]
    }

    try:
        response = requests.post(mailjet_url, json=payload, auth=(MAILJET_API_KEY, MAILJET_API_SECRET), headers=headers)
        response_data = response.json()

        if response.status_code == 200:
            return jsonify({"success": True, "data": response_data}), 200
        else:
            return jsonify({"success": False, "error": response_data}), response.status_code
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)  # Permet d'écouter sur toutes les interfaces
