
from langchain_core.output_parsers import StrOutputParser

from ..models import google
from ..prompts import travelAssisstant

chain = travelAssisstant.prompt | google.generationModel | StrOutputParser()