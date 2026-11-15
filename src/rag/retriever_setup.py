"""
Retriever setup and vector store configuration using OpenRouter API embeddings.
"""

import os
from langchain_core.documents import Document
from langchain_core.tools import tool
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Global variables for lazy initialization
_embeddings = None
_faiss_vectorstore = None


def get_embeddings():
    """Lazily initialize and return OpenRouter-backed OpenAI embeddings."""
    global _embeddings
    if _embeddings is None:
        api_key = (os.getenv("OPENROUTER_API_KEY") or "").strip()
        if not api_key:
            raise ValueError("Missing OPENROUTER_API_KEY environment variable.")

        print(
            "Initializing OpenRouter embeddings (openai/text-embedding-3-small)...",
            flush=True,
        )
        _embeddings = OpenAIEmbeddings(
            model="openai/text-embedding-3-small",
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1",
        )
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
    Return a LangChain tool connected to the FAISS vector store.
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
