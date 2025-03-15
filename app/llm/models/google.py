
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

from app.external_services.googleAI import GEMINI_API_KEY

gemini = ChatGoogleGenerativeAI(model="gemini-1.5-pro", api_key=SecretStr(GEMINI_API_KEY), temperature=0, max_tokens=2000)

