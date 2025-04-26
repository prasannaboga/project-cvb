import logging

import chromadb
import streamlit as st
from ollama import Client
from langchain_ollama import OllamaEmbeddings

logging.basicConfig(level=logging.INFO)


CHROMA_DB_PATH = "project_cvb/data/chroma_db"
COLLECTION_NAME = "IndianPremierLeagueWikipedia"


ollama_client = Client(host="http://localhost:11434")
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = chroma_client.get_or_create_collection(COLLECTION_NAME)
embedding = OllamaEmbeddings(model="nomic-embed-text")


def get_dynamic_prompt(question, context):
  template = """Answer the question based on the context below using {style} style:
  {context}
  
  Question: {question}
  Answer in {length} sentences."""
  return template.format(style="formal", length="1-2", context=context, question=question)


def query_rag(question):
  query_embedding = embedding.embed_query(question)
  results = collection.query(
      query_embeddings=[query_embedding], n_results=3)
  context = "\n".join([doc for doc in results["documents"][0]]
                      ) if results["documents"] else "No context found."

  prompt = get_dynamic_prompt(question, context)
  response = ollama_client.generate(model="llama3.2", prompt=prompt)
  return response["response"].strip()


def main():
  st.title("IPL RAG Query System")
  st.write("Ask anything about IPL teams!")

  question = st.text_input(
      "Enter your question (e.g., 'list of IPL teams'):", "")
  if st.button("Submit"):
    if question:
      with st.spinner("Fetching response..."):
        response = query_rag(question)
        st.write("**Answer:**")
        st.write(response)
    else:
      st.write("Please enter a question!")


if __name__ == "__main__":
  #  poetry run streamlit run project_cvb/scripts/06_pdf_rag_streamlit.py
  main()
