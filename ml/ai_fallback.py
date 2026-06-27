import os
import google.generativeai as genai

def ai_reply(message, history, context=None):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return (
            "🤖 I’m your AI fitness coach.\n\n"
            "Ask me about workouts, diet, or recovery!"
        )

    try:
        genai.configure(api_key=api_key)
        
        system_instruction = (
            "You are an AI fitness coach. "
            "Give safe, beginner-friendly fitness advice. "
            "No medical advice. Keep answers relatively short and motivating.\n\n"
        )
        if context:
            system_instruction += (
                f"Context about the user:\n"
                f"- {context.get('default_recommendation', '')}\n"
                f"- {context.get('fatigue_status', '')}\n\n"
                "Use this context only if the user asks about their specific recommended next workout, "
                "fatigue, or if they need a recommendation. Otherwise, answer "
                "their gym, fitness, exercise, diet, or recovery query using your general knowledge."
            )

        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_instruction
        )

        # Convert history from frontend format to Gemini format
        gemini_history = []
        for msg in history:
            # Avoid duplicate user message in history
            if msg.get("from") == "user" and msg.get("text") == message:
                continue
            role = "user" if msg.get("from") == "user" else "model"
            gemini_history.append({
                "role": role,
                "parts": [msg.get("text", "")]
            })

        chat = model.start_chat(history=gemini_history)
        response = chat.send_message(
            message,
            generation_config=genai.types.GenerationConfig(
                temperature=0.6,
                max_output_tokens=300
            )
        )

        return response.text.strip()

    except Exception:
        return (
            "⚠️ AI is temporarily unavailable.\n\n"
            "Here’s a tip instead:\n"
            "• Rotate muscle groups\n"
            "• Focus on recovery\n"
            "• Stay consistent 💪"
        )
