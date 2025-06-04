from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

ZAPIER_WEBHOOK_URL = "https://hooks.zapier.com/hooks/catch/23187372/2vf1g9a/"
CLAUDE_API_KEY = "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"

@app.route("/", methods=["POST"])
def handle_request():
    data = request.get_json()
    user_input = data.get("text", "")

    claude_response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": CLAUDE_API_KEY,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        },
        json={
            "model": "claude-3-sonnet-20240229",
            "max_tokens": 300,
            "temperature": 0.3,
            "messages": [
                {"role": "user", "content": f"Extract name, note, and category from this message: '{user_input}' and return only JSON like {{'name':'...', 'note':'...', 'category':'...'}}."}
            ]
        }
    )

    structured = claude_response.json()
    try:
        extracted = structured["content"][0]["text"]
        payload = eval(extracted)  # Convert string to dict

        zapier_response = requests.post(ZAPIER_WEBHOOK_URL, json=payload)
        zapier_response.raise_for_status()

        return jsonify({"status": "success", "sent": payload}), 200

    except Exception as e:
        return jsonify({"error": str(e), "raw": structured}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
