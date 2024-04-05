import os
from time import time

from langchain_community.llms import Ollama
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
# from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate


DB_PATH = "vector-db"
DATA_PATH = "./data/combined.md"
Embeddings = GPT4AllEmbeddings
model = Ollama(model="llama2")

template = """[CHAT_HISTORY]{chat_history}[/CHAT_HISTORY]

[CONTEXT]{context}[/CONTEXT]

You're an expert in T.A.R.D.I.S. documentation. You're helping a user to find out how different services work. Always try to provide an example code, if the one exists in your [CONTEXT].

Here is the question you need to answer: [QUESTION]{question}[/QUESTION]
"""
prompt = PromptTemplate.from_template(template)

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]


def read_file(filepath: str):
    file = open(filepath)
    content = file.read()
    file.close()
    return content


def split_markdown(data: str):
    text_splitter = MarkdownHeaderTextSplitter(headers_to_split_on)
    return text_splitter.split_text(data)

def load_db():
    if os.path.isdir(DB_PATH):
        return Chroma(embedding_function=Embeddings(), persist_directory=DB_PATH)
    else:
        texts = split_markdown(read_file(DATA_PATH))
        return Chroma.from_documents(texts, embedding=Embeddings(), persist_directory=DB_PATH)

def get_retriever(db):
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    return ConversationalRetrievalChain.from_llm(model, retriever)


db = load_db()
qa = get_retriever(db)

# expose this index in a retriever interface
start = time()
query = "What is cloudwalker?"
chat_history = []
answer = qa({"question": query, "chat_history": chat_history})['answer']
chat_history = [(query, answer)]
query = "How to upload files as consumer?"
answer = qa({"question": query, "chat_history": chat_history})['answer']

print(f"Time: {time() - start}, Result: {answer}")