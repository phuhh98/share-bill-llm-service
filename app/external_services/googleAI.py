from typing import Annotated

from google import genai
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class GeminiSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GEMINI_")

    api_key: Annotated[str, Field(default="nonsenseKey")]
    model_name: Annotated[str, Field(default="nonsenseModel")]
    max_output_token: Annotated[int, Field(default=2000)]
    model_temp: Annotated[float, Field(default=0)]
    thinking_budget: Annotated[
        int,
        Field(
            default=1024,
            description="Number of token allowed for thinking feature when enable",
        ),
    ]
    enable_thinking: Annotated[bool, Field(default=False)]


geminiModelSettings = GeminiSettings()

client = genai.Client(api_key=geminiModelSettings.api_key)
