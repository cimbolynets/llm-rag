import os
from time import time


from langchain_community.llms import Ollama, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain.memory import ChatMessageHistory
from langchain_core.runnables import RunnablePassthrough, Runnable
from langchain_core.output_parsers import StrOutputParser
from templates import simple_rag_template
from callbacks import MyCustomHandler
from storage.retriever import get_string_retriever

model = Ollama(model="mistral")
# model = HuggingFaceEndpoint(
#     repo_id="mistralai/Mistral-7B-Instruct-v0.2", 
#     temperature=0.1, 
#     huggingfacehub_api_token="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",
#     streaming=True,
# )

# template = docs_chatbot_template + "\n\nChat history: {chat_history}\n\n" + \
#                 "Context: {context}\n\n" + \
#                 "Question: {question}"
template = simple_rag_template
prompt = PromptTemplate.from_template(template)

history = ChatMessageHistory()
chain: Runnable = (
    {"context": get_string_retriever(), "chat_history": RunnablePassthrough(), "question": RunnablePassthrough()} 
    | prompt 
    | model
    | StrOutputParser()
)

questions = [
    "What is cloudwalker?",
    "How to upload files as consumer?",
    "Can you give an example of request body?"
    # "Can you give an example of a request body, to upload files as a consumer?"
]

start = time()
for question in questions:
    print(question)
    result = ""
    for chunk in chain.stream({"question": question, "chat_history": history}):
        result += chunk
        print(chunk, end="")
    history.add_user_message(question)
    history.add_ai_message(result)
    
    print(f"Time: {time() - start} \n")
    start = time()

# for chunk in chain.stream(questions[0]):
#     print(chunk, sep="", end="")