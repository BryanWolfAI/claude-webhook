from flask import Flask, request, jsonify
import requests
from datetime import datetime
import re

app = Flask(__name__)

ZAPIER_WEBHOOK_URL = "https://hooks.zapier.com/hooks/catch/23187372/2vf1g9a/"  # Replace if needed

def parse_sentence(text):
    name = ""
    time = ""
    notes = ""
    category = ""

    name_match = re.search(r"met with\s+([A-Z][a-z]+\s[A-Z][a-z]+)", text, re.I)
    time_match = re.search(r"at\s+([0-9]{1,2}\s*(?:AM|PM))", text, re.I)
    notes_match = re.search(r"notes?:\s*(.+)", text, re.I)
    category_match = re.search(r"category:\s*(\w+)", text, re.I)

    if name_match:
        name = name_match.group(1)
    if time_match:
        time = time_match.group(1)
    if notes_match:
        notes = notes_match.group(1)
    if category_match:
        category = category_match.group(1)

    return {
        "Name": name,
        "Time": time,
        "Notes": notes,
        "Category": category,
        "Timestamp": datetime.utcnow().isoformat()
    }

@app.route("/", methods=["POST"])
def receive_data():
    incoming = request.get_json()
    message = incoming.get("message", "")

    structured_data = parse_sentence(message)

    try:
        zap_response = requests.post(ZAPIER_WEBHOOK_URL, json=structured_data)
        zap_response.raise_for_status()
        return jsonify({"success": True, "sent": structured_data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run()
