"""
Chat page for Streamlit Adaptive RAG Assistant.
"""

import uuid
import streamlit as st
from utils.api_client import query_backend, document_upload_rag

st.set_page_config(page_title="Adaptive RAG Assistant", page_icon="💬", layout="wide")

# Ensure session_id exists even if a user opens /chat directly
if "session_id" not in st.session_state:
    st.session_state["session_id"] = f"demo-{uuid.uuid4().hex[:8]}"

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Sidebar: Document Upload for RAG
with st.sidebar:
    st.header("📂 Upload Documents")
    uploaded_file = st.file_uploader(
        "Upload a PDF, TXT, or DOCX file",
        type=["pdf", "txt", "docx"],
    )
    doc_description = st.text_input(
        "Document description",
        placeholder="e.g., Project architecture or resume",
    )

    if st.button("Upload to Knowledge Base", disabled=uploaded_file is None):
        if not doc_description.strip():
            st.warning("Please enter a short description for the document.")
        else:
            with st.spinner("Indexing document into FAISS..."):
                success = document_upload_rag(uploaded_file, doc_description.strip())
                if success:
                    st.success(f"Uploaded '{uploaded_file.name}' successfully!")
                else:
                    st.error("Failed to upload document. Please try again.")

    st.divider()
    if st.button("🗑️ Clear Chat"):
        st.session_state["messages"] = []
        st.session_state["session_id"] = f"demo-{uuid.uuid4().hex[:8]}"
        st.rerun()

st.title("💬 LangGraph Chat")

# 1. Render all existing chat messages first
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 2. Capture new user input
if prompt := st.chat_input("Ask anything or query your uploaded documents..."):
    # Append and immediately render user message so it stays visible while waiting
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Show spinner inside the assistant bubble until the backend responds
    with st.chat_message("assistant"):
        with st.spinner("Thinking & routing query..."):
            reply = query_backend(prompt, st.session_state["session_id"])
            st.markdown(reply)

    # Save assistant reply to session history
    st.session_state["messages"].append({"role": "assistant", "content": reply})
