import os

from langchain_google_genai import GoogleGenerativeAI
from pydantic import SecretStr

GEMINI_API_KEY= os.getenv("GEMINI_API_KEY","nonsenseKey")

gemini = GoogleGenerativeAI(model="gemini-1.5-pro", api_key=SecretStr(GEMINI_API_KEY), temperature=0, max_tokens=2000)

