from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

ZAPIER_WEBHOOK_URL = "https://hooks.zapier.com/hooks/catch/23187372/2vf1g9a/"

@app.route("/", methods=["POST"])
def handle():
    data = request.get_json()
    
    # Extract expected fields from JSON
    name = data.get("name", "")
    note = data.get("note", "")
    category = data.get("category", "")
    timestamp = data.get("timestamp", datetime.utcnow().isoformat())

    payload = {
        "name": name,
        "note": note,
        "category": category,
        "timestamp": timestamp
    }

    try:
        response = requests.post(ZAPIER_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        return jsonify({"status": "success", "sent": payload}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
