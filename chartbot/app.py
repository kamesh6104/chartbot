from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Replace with your OpenRouter API key
OPENROUTER_API_KEY = "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"

# Use a free model
MODEL = "openai/gpt-oss-20b:free"

# Store chat history
conversation_history = [
    {
        "role": "system",
        "content": "You are a helpful AI assistant."
    }
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data["message"]

        conversation_history.append({
            "role": "user",
            "content": user_message
        })

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:5000",
                "X-Title": "ChartBot"
            },
            json={
                "model": MODEL,
                "messages": conversation_history
            },
            timeout=60
        )

        print("Status:", response.status_code)
        print("Response:", response.text)

        if response.status_code != 200:
            return jsonify({
                "reply": f"API Error: {response.text}"
            })

        result = response.json()

        bot_reply = result["choices"][0]["message"]["content"]

        conversation_history.append({
            "role": "assistant",
            "content": bot_reply
        })

        return jsonify({
            "reply": bot_reply
        })

    except Exception as e:
        return jsonify({
            "reply": f"Error: {str(e)}"
        })


if __name__ == "__main__":
    app.run(debug=True)