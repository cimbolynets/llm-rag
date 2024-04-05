from langchain_community.utilities import SQLDatabase  # Import the missing class
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.llms import Ollama

template = """### Chat history 
{chat_history}

### Task
Generate a SQL query to answer [QUESTION]{question}[/QUESTION]

### Database Schema
The query will run on a database with the following schema:
{schema}

### Answer
Given the database schema, here is the SQL query that [QUESTION]{question}[/QUESTION]
[SQL]
"""
prompt = PromptTemplate.from_template(template)

db = SQLDatabase.from_uri("sqlite:///llm.db")
llm = Ollama(model="llama2")

def get_schema(_):
    return db.get_table_info()

chain = RunnablePassthrough.assign(schema=get_schema) | prompt | llm.bind(stop=["\nSQLResult:"]) | StrOutputParser()
question = "Select male users under 30 with all fields" 
# chain.invoke(question)
chat_history = []
result1 = chain.invoke({"question": question, "chat_history": chat_history})
print("Query: " + result1)
print(db.run(result1))
# chat_history.append((question, result1))
# print(chain.invoke({"question": "Reformat previous query to return all table fields, preserving other conditions.", "chat_history": chat_history}))
