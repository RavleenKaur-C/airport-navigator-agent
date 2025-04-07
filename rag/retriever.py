import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain_openai import OpenAIEmbeddings

from fetch_wikivoyage import fetch_airport_text

# Load environment variables (including OPENAI_API_KEY)
load_dotenv()

class AirportRetriever:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = None

    def load_and_index(self, airport_name: str):
        raw_text = fetch_airport_text(airport_name)
        if not raw_text:
            print(f"[!] No text found for: {airport_name}")
            return False

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = splitter.create_documents([raw_text])

        self.vectorstore = FAISS.from_documents(chunks, self.embeddings)
        return True

    def retrieve_passages(self, query: str, k: int = 3) -> list[str]:
        if not self.vectorstore:
            return []

        docs = self.vectorstore.similarity_search(query, k=k)
        return [doc.page_content for doc in docs]
