import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print(f"DEBUG: Gemini API Key loaded? {'Yes' if api_key else 'No'}")

if not api_key:
    print("ERROR: GEMINI_API_KEY is missing from environment variables.")
    print("Please check if .env file exists and contains GEMINI_API_KEY.")
    exit(1)

# Masked key for verification
print(f"DEBUG: API Key starts with: {api_key[:4]}...")

try:
    genai.configure(api_key=api_key)
    print("DEBUG: Gemini client initialized.")

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content("Hello, reply with only the word SUCCESS")
    print("SUCCESS: API call worked!")
    print("Response:", response.text.strip())

except Exception as e:
    print("\nERROR: Listing models failed.")
    print(f"Type: {type(e).__name__}")
    print(f"Message: {e}")

