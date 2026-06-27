from recommender import recommend_workout
from fatigue import check_fatigue
from ai_fallback import ai_reply


def chat_reply(message, history):
    # Fetch local baseline calculations to provide as context to the AI
    try:
        rec = recommend_workout([])
        default_recommendation = (
            f"Recommended next workout: {rec['workout']} "
            f"for {rec['duration']} minutes. Reason: {rec['reason']}"
        )
    except Exception:
        default_recommendation = "Recommended next workout: Chest (30 mins)."

    try:
        fatigue = check_fatigue([])
        fatigue_status = f"Fatigue status: {'Overtrained/Fatigued' if fatigue else 'Healthy/Not Fatigued'}"
    except Exception:
        fatigue_status = "Fatigue status: Healthy/Not Fatigued"

    context = {
        "default_recommendation": default_recommendation,
        "fatigue_status": fatigue_status
    }

    # Delegate all conversation logic to the Gemini-powered ai_reply
    return ai_reply(message, history, context=context)

