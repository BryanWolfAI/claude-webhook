from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

ZAPIER_WEBHOOK_URL = "https://hooks.zapier.com/hooks/catch/23187372/2vf1g9a/"
CLAUDE_API_KEY = "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"

@app.route("/", methods=["POST"])
def handle():
    data = request.get_json()
    message = data.get("text", "")

    payload = {
        "name": message,
    }

    try:
        response = requests.post(ZAPIER_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        return jsonify({"status": "success", "sent": payload}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
