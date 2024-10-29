# Import required libraries
from sqlalchemy import create_engine, inspect
from langchain import LLMChain, PromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from chromadb import Client , Settings
from langchain.vectorstores import Chroma as VectorStore
from langchain.chains import RetrievalQA
from llama import Llama

# Step 1: Connect to MySQL Database and Extract Schema
# Replace with your MySQL credentials
engine = create_engine('mysql+pymysql://root:123456789@localhost/llm_db')

# Inspect database schema
inspector = inspect(engine)
tables = inspector.get_table_names()
schema = {}
for table in tables:
    columns = inspector.get_columns(table)
    schema[table] = [col['name'] for col in columns]

# Step 2: Initialize the Llama Model
llm = Llama(model_path="models/llama-2-7b-chat.ggmlv3.q8_0.bin")  # Update with your Llama model path

# Step 3: Set up Chroma Vector Store for Sample Queries
# Initialize Chroma with OpenAI embeddings (or any compatible embeddings model)

client = Client(Settings())

vector_db = VectorStore(
    collection_name="sql_sample_queries",
    embedding_function=OpenAIEmbeddings(),
    client=client  # Pass the initialized Chroma client
)

# Seed vector store with sample questions and SQL queries
sample_queries = [
    {"question": "List all customers who made a purchase in the last 30 days", 
     "sql": "SELECT customer_id FROM purchases WHERE purchase_date >= NOW() - INTERVAL 30 DAY;"},
    {"question": "Find products that have low stock", 
     "sql": "SELECT product_id, stock_quantity FROM products WHERE stock_quantity < 10;"},
    {"question": "Show total sales for each month", 
     "sql": "SELECT DATE_FORMAT(sale_date, '%Y-%m') AS month, SUM(amount) AS total_sales FROM sales GROUP BY month;"}
]

# Add sample queries to Chroma vector store
for sample in sample_queries:
    vector_db.add_texts(
        texts=[sample["question"]],
        metadatas=[{"sql": sample["sql"]}]
    )

# Step 4: Set up LangChain Prompt Template for SQL Generation
prompt_template = """
Generate an SQL query based on the following question and schema.

Question: {question}
Schema: {schema}
Examples:
{examples}

SQL Query:
"""

prompt = PromptTemplate(template=prompt_template, input_variables=["question", "schema", "examples"])

# Define an LLMChain for query generation
chain = LLMChain(llm=llm, prompt=prompt)

# Step 5: Set up the Retrieval QA Chain to Fetch Similar Examples
retriever = vector_db.as_retriever()
retrieval_chain = RetrievalQA(llm=llm, retriever=retriever)

# Step 6: Run the Query Generation Tool
# Collect user input
question = input("Please enter your question: ")

# Format schema description for the prompt
schema_description = "\n".join([f"{table}: {', '.join(cols)}" for table, cols in schema.items()])

# Retrieve similar sample queries to use as context for the LLM
retrieved_samples = retrieval_chain({"query": question})
similar_queries = retrieved_samples["result"]

# Format examples for the prompt
examples = "\n".join([f"Question: {sample['question']}\nSQL: {sample['sql']}" for sample in similar_queries])

# Generate the SQL using Llama and LangChain
sql_query = chain.run({
    "question": question,
    "schema": schema_description,
    "examples": examples
})

print("\nGenerated SQL Query:\n", sql_query)

# Step 7 (Optional): Validate and Execute the Generated SQL Query
try:
    with engine.connect() as connection:
        result = connection.execute(sql_query)
        for row in result:
            print(row)
except Exception as e:
    print("Error executing SQL query:", e)
