import os
from groq import Groq

def ai_reply(message, history):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return (
            "🤖 I’m your AI fitness coach.\n\n"
            "Ask me about workouts, diet, or recovery!"
        )

    try:
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # fast + smart
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI fitness coach. "
                        "Give safe, beginner-friendly fitness advice. "
                        "No medical advice. Keep answers short and motivating."
                    )
                },
                {"role": "user", "content": message}
            ],
            temperature=0.6,
            max_tokens=200
        )

        return response.choices[0].message.content.strip()

    except Exception:
        return (
            "⚠️ AI is temporarily unavailable.\n\n"
            "Here’s a tip instead:\n"
            "• Rotate muscle groups\n"
            "• Focus on recovery\n"
            "• Stay consistent 💪"
        )
