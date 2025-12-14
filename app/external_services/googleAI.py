import os

from google import genai

GEMINI_API_KEY = os.getenv(key="GEMINI_API_KEY", default="nonsenseKey")

GEMINI_MODEL_NAME = os.getenv(key="GEMINI_MODEL_NAME", default="nonsenseKey")

GEMINI_MAX_OUTPUT_TOKEN = os.getenv(key="GEMINI_MAX_OUTPUT_TOKEN", default=2000)

client = genai.Client(api_key=GEMINI_API_KEY)
