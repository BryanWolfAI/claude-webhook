from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)

ZAPIER_WEBHOOK_URL = "https://hooks.zapier.com/hooks/catch/23187372/2vf1g9a/"

@app.route("/", methods=["POST"])
def handle():
    try:
        data = request.get_json()
        print(f"Received data: {data}")  # This will show in Render logs
        
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
        
        print(f"Sending to Zapier: {payload}")  # This will show in Render logs
        
        response = requests.post(ZAPIER_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        
        return jsonify({"status": "success", "sent": payload}), 200
        
    except Exception as e:
        print(f"Error: {e}")  # This will show in Render logs
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
