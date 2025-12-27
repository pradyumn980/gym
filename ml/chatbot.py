from recommender import recommend_workout
from fatigue import check_fatigue
from ai_fallback import ai_reply


def detect_intent(message):
    msg = message.lower()

    intents = {
        "WORKOUT": ["tomorrow", "next", "recommend", "should i"],
        "DIET": ["diet", "food", "eat", "nutrition", "calorie", "fat loss"],
        "FATIGUE": ["tired", "fatigue", "sore", "overtrain", "rest"],
        "WHY": ["why", "reason", "explain"],
        "WEEKLY": ["week", "weekly", "7 days", "schedule"],
    }

    scores = {intent: 0 for intent in intents}

    for intent, keywords in intents.items():
        for k in keywords:
            if k in msg:
                scores[intent] += 1

    best_intent = max(scores, key=scores.get)

    return best_intent if scores[best_intent] > 0 else "AI_FALLBACK"


def chat_reply(message, history):
    intent = detect_intent(message)

    # 🔹 WHY / EXPLANATION
    if intent == "WHY":
        rec = recommend_workout(history)
        return (
            f"Good question 👍\n\n"
            f"You’re seeing **{rec['workout']}** because:\n"
            f"🧠 {rec['reason']}"
        )

    # 🔹 WEEKLY PLAN
    if intent == "WEEKLY":
        return (
            "💪 **Here’s a balanced weekly workout plan:**\n\n"
            "🟢 Monday – Chest + Triceps\n"
            "🔵 Tuesday – Back + Biceps\n"
            "🟠 Wednesday – Legs\n"
            "🟣 Thursday – Shoulders + Core\n"
            "🔴 Friday – Cardio / HIIT\n"
            "🟡 Saturday – Full Body or Weak Areas\n"
            "⚪ Sunday – Rest / Active Recovery\n\n"
            "📌 I’ll adjust this automatically if you feel fatigued."
        )

    # 🔹 NEXT WORKOUT
    if intent == "WORKOUT":
        rec = recommend_workout(history)
        return (
            f"Based on your recent training 💪\n\n"
            f"👉 I recommend **{rec['workout']}** for "
            f"**{rec['duration']} minutes**.\n\n"
            f"🧠 {rec['reason']}"
        )

    # 🔹 FATIGUE / RECOVERY
    if intent == "FATIGUE":
        if check_fatigue(history):
            return (
                "😴 You might be overtraining.\n\n"
                "I recommend **Active Recovery or rest** today "
                "to prevent injury."
            )
        return (
            "👍 You’re doing well!\n\n"
            "Keep rotating muscle groups and stay consistent."
        )

    # 🔹 DIET (handled by AI)
    if intent == "DIET":
        return ai_reply(message, history)

    # 🔹 AI FALLBACK (IMPORTANT)
    return ai_reply(message, history)
