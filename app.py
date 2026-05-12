from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load .env file manually
load_dotenv(dotenv_path="D:/AI_CHAT_WEBSITE/.env")

# Check API key
print("API KEY:", os.getenv("OPENROUTER_API_KEY"))

app = Flask(__name__)

# OpenRouter Client
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# Home Route
@app.route("/")
def home():
    return render_template("index.html")

# Chat Route
@app.route("/chat", methods=["POST"])
def chat():

    try:
        # Get user message
        user_message = request.json["message"]

        # AI response
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        # Extract AI reply
        reply = response.choices[0].message.content

        return jsonify({
            "reply": reply
        })

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "reply": str(e)
        })

# Run Flask App
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
