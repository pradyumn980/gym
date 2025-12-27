from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()
from recommender import recommend_workout, generate_weekly_plan
from chatbot import chat_reply

app = Flask(__name__)

# IMPORTANT: allow all origins & methods
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/")
def home():
    return "ML API running"
    
@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    data = request.get_json()
    message = data.get("message", "")
    history = data.get("history", [])

    reply = chat_reply(message, history)
    return jsonify({ "reply": reply })

@app.route("/recommend-workout", methods=["POST", "OPTIONS"])
def recommend():
    # Explicit OPTIONS handling
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    data = request.get_json(force=True)
    history = data.get("history", [])

    print("🔥 ML API CALLED")
    print("📜 History:", history)

    result = recommend_workout(history)

    print("🤖 Result:", result)

    return jsonify(result)

@app.route("/generate-weekly-plan", methods=["POST", "OPTIONS"])
def generate_week():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    data = request.get_json(force=True)
    history = data.get("history", [])
    preferences = data.get("preferences", {}) # Extract preferences
    
    plan = generate_weekly_plan(history, preferences)
    return jsonify(plan)

if __name__ == "__main__":
    if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
