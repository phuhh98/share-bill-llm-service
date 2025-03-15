from langchain_core.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)

sysPrompt = SystemMessagePromptTemplate(prompt=PromptTemplate(template="""
	Role: Tourism guidance assistant
	Job: Give general information about mentioned place include geography, history, culture and special cuisines.
	Fail safe: Formally sorry if the question is not related.

	User question: {question}
""", input_variables=["question"], input_types={"question":str}))

prompt = ChatPromptTemplate(messages=[
    sysPrompt
])