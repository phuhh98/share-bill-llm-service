
from langchain.output_parsers import OutputFixingParser
from langchain_core.output_parsers import PydanticOutputParser

from ..models import google
from ..outputSchemas.receiptExtractor import FormatInstructions
from ..prompts import receiptExtractor

"""
OutputFixingParser help to retry on parsing error
Refs:  https://python.langchain.com/docs/how_to/output_parser_fixing/
       https://python.langchain.com/api_reference/langchain/output_parsers/langchain.output_parsers.fix.OutputFixingParser.html#
"""
parserWithFixing = OutputFixingParser.from_llm(
    parser=PydanticOutputParser(pydantic_object=FormatInstructions),
    llm=google.generationModel,
    prompt=receiptExtractor.ouptutFixingPrompt,
    max_retries=2,
)

"""
This require two param on invoke:
format_instructions : output Schema
mediaMessage: Message compose from MediaMesage Class
"""
chain = receiptExtractor.prompt | google.chatModel | parserWithFixing
