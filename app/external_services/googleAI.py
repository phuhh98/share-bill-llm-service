import os

from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "nonsenseKey")

GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "nonsenseKey")

client = genai.Client(api_key=GEMINI_API_KEY)
