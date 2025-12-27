import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

print(f"DEBUG: API Key loaded? {'Yes' if api_key else 'No'}")

if not api_key:
    print("ERROR: GROQ_API_KEY is missing from environment variables.")
    print("Please check if .env file exists and contains GROQ_API_KEY.")
    exit(1)

# Masked key for verification
print(f"DEBUG: API Key starts with: {api_key[:4]}...")

try:
    client = Groq(api_key=api_key)
    print("DEBUG: Groq client initialized.")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "Hello"}],
        max_tokens=10
    )
    print("SUCCESS: API call worked!")
    print("Response:", response.choices[0].message.content)

except Exception as e:
    print("\nERROR: API call failed.")
    print(f"Type: {type(e).__name__}")
    print(f"Message: {e}")
