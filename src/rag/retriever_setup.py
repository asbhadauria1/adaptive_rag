"""
Retriever setup and vector store configuration (True Lazy-Loading).
"""

import os
from langchain_core.documents import Document
from langchain_core.tools import tool
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Global variables for lazy initialization
_embeddings = None
_faiss_vectorstore = None


def get_embeddings():
    """Lazily initialize and return the HuggingFace embeddings model on first use."""
    global _embeddings
    if _embeddings is None:
        print(
            "Initializing HuggingFace embeddings model (all-MiniLM-L6-v2)...",
            flush=True,
        )
        _embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return _embeddings


def retriever_chain(chunks: list[Document]):
    """
    Initialize and store documents in FAISS vector database.
    """
    global _faiss_vectorstore

    try:
        embeddings = get_embeddings()
        vectorstore = FAISS.from_documents(documents=chunks, embedding=embeddings)
        _faiss_vectorstore = vectorstore

        print("FAISS vector store initialized with documents", flush=True)
        print(f"Vectorstore contains {len(chunks)} document chunks", flush=True)
        return True
    except Exception as e:
        print(f"Error storing documents in FAISS: {e}", flush=True)
        return False


def get_retriever():
    """
    Return a LangChain tool connected to the FAISS vector store WITHOUT
    loading HuggingFace/PyTorch models at import time.
    """
    if os.path.exists("description.txt"):
        with open("description.txt", "r", encoding="utf-8") as f:
            description = f.read().strip()
    else:
        description = "customer uploaded documents"

    @tool("retriever_customer_uploaded_documents")
    def retriever_tool(query: str) -> str:
        """Search and return information from uploaded customer documents."""
        global _faiss_vectorstore
        if _faiss_vectorstore is None:
            return (
                "No documents have been uploaded yet. Please upload a document first."
            )

        retriever = _faiss_vectorstore.as_retriever()
        docs = retriever.invoke(query)
        return "\n\n".join(doc.page_content for doc in docs)

    retriever_tool.description = (
        f"Use this tool **only** to answer questions about: {description}\n"
        "Don't use this tool to answer anything else."
    )

    return retriever_tool
