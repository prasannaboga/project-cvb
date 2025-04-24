import os

import ollama
from langchain_community.document_loaders import (PyPDFLoader,
                                                  UnstructuredPDFLoader)
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

print("PDF RAG SAMPLE")

doc_path = "project_cvb/data/IndianPremierLeagueWikipedia.pdf"
model = "llama3.2"

# loader = UnstructuredPDFLoader(file_path=doc_path)
loader = PyPDFLoader(file_path=doc_path)
data = loader.load()
print("pdf file loading....")


# Preview first page
# content = data[0].page_content
# print(content[:1000])

print("Loaded PDF data successfully.")
print(f"Number of documents: {len(data)}")

# ==== End of PDF Ingestion ====


# ==== Extract Text from PDF Files and Split into Small Chunks ====


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200, chunk_overlap=300)
chunks = text_splitter.split_documents(data)
print("data splitting is done")

# print(f"Number of chunks: {len(chunks)}")
# print(f"Example chunk: {chunks[0]}")

# ==== Create Vector Store ====

ollama.pull("nomic-embed-text")

vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=OllamaEmbeddings(model="nomic-embed-text"),
    collection_name="simple-rag",
)
print("data adding to vector database is done")



from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_ollama import ChatOllama

from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever

# set up our model to use
llm = ChatOllama(model=model)


QUERY_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""You are an AI language model assistant. Your task is to generate five
    different versions of the given user question to retrieve relevant documents from
    a vector database. By generating multiple perspectives on the user question, your
    goal is to help the user overcome some of the limitations of the distance-based
    similarity search. Provide these alternative questions separated by newlines.
    Original question: {question}""",
)

retriever = MultiQueryRetriever.from_llm(
    vector_db.as_retriever(), llm, prompt=QUERY_PROMPT
)

# RAG prompt
template = """Answer the question based ONLY on the following context:
{context}
Question: {question}
"""


prompt = ChatPromptTemplate.from_template(template)

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)



# result = chain.invoke(input=("what is the document about?",))
result = chain.invoke(input=("how many ipl teams?",))
print(result)
print("--------------------")

result = chain.invoke(input=("how many ipl teams in 2018?",))
print(result)
print("--------------------")

result = chain.invoke(input=("winners list",))
print(result)
print("--------------------")
