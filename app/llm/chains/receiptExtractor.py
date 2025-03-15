
from langchain_core.output_parsers import JsonOutputParser

from ..models import google
from ..prompts import receiptExtractor

# This require two param on invoke: 
# format_instructions : output Schema
# mediaMessage: Message compose from MediaMesage Class
chain = receiptExtractor.prompt | google.gemini | JsonOutputParser()