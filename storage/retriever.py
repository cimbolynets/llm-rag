import os

from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.messages import HumanMessage

from templates import summarization_template
Embeddings = HuggingFaceEmbeddings

DB_PATH = "./storage/vector-db"
DATA_PATH = "./data/combined.md"

model = Ollama(model="mistral")
chain = PromptTemplate.from_template(summarization_template) | model

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
    ("####", "Header 4"),
    ("#####", "Header 5"),
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

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_summarized_human_messages(chat_history):
    return "\n".join(
        map(
            lambda m: m.content, 
            filter(lambda m: isinstance(m, HumanMessage), chat_history.messages)
        )
    )

def get_string_retriever():
    db = load_db()
    def summarize(ctx):
        summarized_conversation = chain.invoke({
            "question": ctx["question"],
            "prev_questions": get_summarized_human_messages(ctx["chat_history"]) 
        })
        print("Summarized: " + summarized_conversation)
        return format_docs(db.similarity_search(summarized_conversation, k=5))
    # return db.as_retriever(search_type="similarity", search_kwargs={"k": 5}) | format_docs
    return summarize