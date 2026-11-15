"""
API client for communicating with backend services.
"""

import logging
import os

import requests
import streamlit as st

logger = logging.getLogger(__name__)

# Backend service URL
try:
    PYTHON_BASE_URL = (
        st.secrets.get("PYTHON_BASE_URL")
        or os.getenv("PYTHON_BASE_URL")
        or "https://adaptive-rag-backend-c8m7.onrender.com"
    ).rstrip("/")
except Exception:
    PYTHON_BASE_URL = os.getenv(
        "PYTHON_BASE_URL", "https://adaptive-rag-backend-c8m7.onrender.com"
    ).rstrip("/")


def query_backend(query: str, session_id: str) -> str:
    """
    Send a query to the RAG backend.

    Args:
        query: The user's query text.
        session_id: Session identifier for tracking conversation.

    Returns:
        Response text from the backend or error message.
    """
    url = f"{PYTHON_BASE_URL}/rag/query"
    logger.info("[query_backend] Calling: %s", url)

    try:
        response = requests.post(
            url,
            json={"query": query, "session_id": session_id},
            allow_redirects=False,
            timeout=90,
        )

        if response.status_code == 200:
            return response.json()["result"]["content"]
        return f"Error: {response.status_code}\n{response.text}"
    except requests.RequestException as e:
        logger.exception("Request to /rag/query failed: %s", e)
        return f"Connection error (backend may be waking up, please retry): {str(e)}"


def document_upload_rag(file, description: str) -> bool:
    """
    Upload a document to the RAG system.

    Args:
        file: File object to upload.
        description: Description of the document.

    Returns:
        True if upload succeeds, False otherwise.
    """
    headers = {"X-Description": description}
    url = f"{PYTHON_BASE_URL}/rag/documents/upload"

    if file:
        try:
            files = {"file": (file.name, file, file.type)}
            response = requests.post(url, files=files, headers=headers, timeout=90)
            logger.info("Document upload status: %s", response.status_code)

            if response.status_code == 200:
                return True
        except requests.RequestException as e:
            logger.exception("Document upload failed: %s", e)

    return False


def create_user(username: str, password: str, api_token: str) -> bool:
    """Stub for unused authentication endpoint."""
    return True


def login_user(username: str, password: str, api_token: str) -> dict:
    """Stub for unused authentication endpoint."""
    return {"token": "demo-token"}


def get_api_token() -> str:
    """Stub for unused authentication endpoint."""
    return "demo-token"
