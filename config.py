import os
from dotenv import load_dotenv
from google import genai  # Correct import for the new SDK

# Load variables from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize the Client
# The SDK will automatically use GEMINI_API_KEY or GOOGLE_API_KEY from os.environ
client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Hi Gemini, is the connection with you successful?"
)
print(response.text)