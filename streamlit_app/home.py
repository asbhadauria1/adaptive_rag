"""
Home page for Streamlit Adaptive RAG Assistant.
Automatically initializes a unique guest session and launches the chat interface.
"""

import uuid
import streamlit as st

st.set_page_config(page_title="Adaptive RAG Assistant", page_icon="🤖", layout="wide")

# Hide default sidebar page nav if desired
hide_sidebar_style = """
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

# Initialize unique session state per visitor so MongoDB chat history stays isolated
if "session_id" not in st.session_state:
    st.session_state["session_id"] = f"demo-{uuid.uuid4().hex[:8]}"

st.session_state["jwt_token"] = "demo-jwt-token"
st.session_state["username"] = "Guest"

# Immediately redirect to the chat interface
st.switch_page("pages/chat.py")
