from flask import Flask, request, jsonify
import requests
import re
from datetime import datetime

app = Flask(__name__)

ZAPIER_WEBHOOK_URL = "https://hooks.zapier.com/hooks/catch/23187372/2vf1g9a/"

# Helper function to parse Claude's natural language
def extract_fields(message):
    fields = {"name": "", "note": "", "category": "", "timestamp": ""}
    matches = re.findall(r'(name|note|category)\s*=\s*([^;]+)', message, re.IGNORECASE)

    for key, value in matches:
        key = key.lower()
        fields[key] = value.strip()

    fields["timestamp"] = datetime.now().isoformat()
    return fields

@app.route("/", methods=["GET", "POST"])
def handle():
    if request.method == "GET":
        return jsonify({"status": "ok", "message": "Render server is online"}), 200

    try:
        data = request.get_json()
        message = data.get("text", "")
        parsed = extract_fields(message)

        response = requests.post(ZAPIER_WEBHOOK_URL, json=parsed)
        response.raise_for_status()

        return jsonify({"status": "success", "sent": parsed}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
