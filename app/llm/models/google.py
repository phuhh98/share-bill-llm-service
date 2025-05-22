
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAI
from pydantic import SecretStr

from app.external_services.googleAI import GEMINI_API_KEY, GEMINI_MODEL_NAME

chatModel = ChatGoogleGenerativeAI(model=GEMINI_MODEL_NAME, api_key=SecretStr(
    GEMINI_API_KEY), temperature=0, max_tokens=2000)
generationModel = GoogleGenerativeAI(model=GEMINI_MODEL_NAME, api_key=SecretStr(
    GEMINI_API_KEY), temperature=0, max_tokens=2000)
