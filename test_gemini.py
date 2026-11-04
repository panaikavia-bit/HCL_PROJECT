
import os
from dotenv import load_dotenv
from google import genai

# Load API key from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL", "gemini-flash-latest")

if not api_key or api_key == "YOUR_ACTUAL_GEMINI_API_KEY":
    raise ValueError("Please add your Gemini API key to .env")

# Connect to Gemini
client = genai.Client(api_key=api_key)

# Send a test question
response = client.models.generate_content(
    model=model,
    contents="Explain what C# is in simple English."
)

print("\nGemini Response:")
print(response.text)


