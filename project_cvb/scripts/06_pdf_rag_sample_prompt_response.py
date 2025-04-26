import argparse

from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama, OllamaEmbeddings

CHROMA_PATH = "project_cvb/data/chroma_db"
COLLECTION_NAME = "IndianPremierLeagueWikipedia"

vector_db = Chroma(persist_directory=CHROMA_PATH, collection_name=COLLECTION_NAME,
                   embedding_function=OllamaEmbeddings(model="nomic-embed-text"))

llm = ChatOllama(model="llama3.2", temperature=0.2)
prompt_template = PromptTemplate(
    input_variables=["question"],
    template="""You are an AI language model assistant. Your task is to generate five
    different versions of the given user question to retrieve relevant documents from
    a vector database. By generating multiple perspectives on the user question, your
    goal is to help the user overcome some of the limitations of the distance-based
    similarity search. Provide these alternative questions separated by newlines.
    Original question: {question}""",
)

retriever = MultiQueryRetriever.from_llm(
    vector_db.as_retriever(search_kwargs={"k": 5}), llm, prompt=prompt_template
)

template = """Answer the question based ONLY on the following context:
{context}
Question: {question}
"""
chat_prompt_template = ChatPromptTemplate.from_template(template)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--prompt", type=str, required=True, help="User prompt")

  args = parser.parse_args()
  input_prompt = args.prompt

  print(f"Prompt: {input_prompt}\n")

  chain = (
      {"context": retriever, "question": RunnablePassthrough()}
      | chat_prompt_template
      | llm
      | StrOutputParser()
  )
  result = chain.invoke(input=(input_prompt,))
  print(result)


if __name__ == "__main__":
  main()
