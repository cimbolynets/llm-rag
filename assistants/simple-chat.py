import os

from langchain_community.llms import HuggingFaceEndpoint, Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from callbacks import MyCustomHandler
from templates import docs_chatbot_template

model = Ollama(model="llama2")
# model = HuggingFaceEndpoint(repo_id="mistralai/Mistral-7B-Instruct-v0.2", temperature=0.1, huggingfacehub_api_token="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")
prompt = PromptTemplate.from_template(
    docs_chatbot_template + "\n\nQuestion: {question}", 
)

chain = {"question": RunnablePassthrough()} | prompt | model | StrOutputParser()

print(chain.invoke("Can you give an example of sending events to horizon?", config={"callbacks":[MyCustomHandler()]}))
