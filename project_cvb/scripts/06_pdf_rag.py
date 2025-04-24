import os
from langchain_community.document_loaders import UnstructuredPDFLoader, PyPDFLoader

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
