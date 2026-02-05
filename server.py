from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

OPENROUTER_API_KEY = "your_api_key"

def get_ai_reply(message):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:5000",
                "X-Title": "Voice Assistant"
            },
            json={
                "model": "openrouter/auto",
                "messages": [
                    {"role": "system", "content": "You are a friendly voice assistant. Detect whether the user speaks Telugu or English and reply in the SAME language. Keep responses short and natural."},
                    {"role": "user", "content": message}
                ]
            }
        )

        print("STATUS:", response.status_code)
        print("RAW RESPONSE:", response.text)

        data = response.json()

        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        else:
            return "API Error. Check terminal."

    except Exception as e:
        print("ERROR:", e)
        return "Connection error."


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    print("User:", user_message)

    reply = get_ai_reply(user_message)
    print("AI:", reply)

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)

