# app/core/vector_store.py

import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document

# Define your vector DB path
VECTOR_DB_PATH = "vector_store"

# Load embeddings model (e.g., `all-MiniLM-L6-v2`)
def get_embedder(model_name="all-MiniLM-L6-v2"):
    return HuggingFaceEmbeddings(model_name=model_name)

# Save vector store to local disk
def save_vector_store(vector_store):
    vector_store.save_local(VECTOR_DB_PATH)

# Load vector store from local disk
def load_vector_store(embedder):
    return FAISS.load_local(VECTOR_DB_PATH, embedder, allow_dangerous_deserialization=True)

# Create and save a vector store from a list of documents
def create_and_save_vector_store(docs: list[Document], embedder):
    if not docs:
        raise ValueError("No documents provided to create vector store.")

    vector_store = FAISS.from_documents(docs, embedder)
    save_vector_store(vector_store)
    return vector_store
