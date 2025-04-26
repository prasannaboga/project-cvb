
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Define paths
PDF_PATH = "project_cvb/data/IndianPremierLeagueWikipedia.pdf"
CHROMA_PATH = "project_cvb/data/chroma_db"
COLLECTION_NAME = "IndianPremierLeagueWikipedia"


def main():
  print("Ingestion pdf.....")
  loader = PyPDFLoader(file_path=PDF_PATH)
  data = loader.load()
  print("Loaded PDF data successfully.")
  print(f"Number of documents: {len(data)}")

  print("splitting data into chunks....")
  text_splitter = RecursiveCharacterTextSplitter(
      chunk_size=1000, chunk_overlap=200)
  chunks = text_splitter.split_documents(data)
  print(f"Number of chunks: {len(chunks)}")

  print("Creating vector store...")
  vector_store = Chroma.from_documents(
      documents=chunks,
      embedding=OllamaEmbeddings(model="nomic-embed-text"),
      persist_directory=CHROMA_PATH,
      collection_name=COLLECTION_NAME,
  )
  print("Vector store saved!")


if __name__ == "__main__":
  main()
