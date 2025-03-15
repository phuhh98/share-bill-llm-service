import os

from google import genai

GEMINI_API_KEY= os.getenv("GEMINI_API_KEY","nonsenseKey")

client = genai.Client(api_key=GEMINI_API_KEY)
