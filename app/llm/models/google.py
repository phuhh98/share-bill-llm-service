from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAI

from app.external_services.googleAI import geminiModelSettings

chatModel = ChatGoogleGenerativeAI(
    model=geminiModelSettings.model_name,
    api_key=geminiModelSettings.api_key,
    temperature=geminiModelSettings.model_temp,
    max_tokens=geminiModelSettings.max_output_token,
)
generationModel = GoogleGenerativeAI(
    model=geminiModelSettings.model_name,
    api_key=geminiModelSettings.api_key,
    temperature=geminiModelSettings.model_temp,
    max_tokens=geminiModelSettings.max_output_token,
    thinking_budget=geminiModelSettings.thinking_budget,
    include_thoughts=geminiModelSettings.enable_thinking,
)
