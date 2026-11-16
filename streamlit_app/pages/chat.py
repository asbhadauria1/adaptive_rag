import uuid
import streamlit as st
from utils.api_client import send_query, upload_document

# 1. Page Configuration
st.set_page_config(
    page_title="Adaptive RAG Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Auto-initialize Guest Session (if accessed directly)
if "session_id" not in st.session_state:
    st.session_state.session_id = f"guest-{uuid.uuid4().hex[:8]}"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "active_doc" not in st.session_state:
    st.session_state.active_doc = None

# 3. Custom CSS for Modern AI Chat Aesthetics
st.markdown(
    """
    <style>
    /* Center main chat column for comfortable reading */
    [data-testid="stMain"] .block-container {
        max-width: 840px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    /* Hide default Streamlit deploy button & footer clutter */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}

    /* Style chat message cards */
    [data-testid="stChatMessage"] {
        border-radius: 14px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
        border: 1px solid rgba(128, 128, 128, 0.16);
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
    }

    /* Subtle tint for user messages */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        background-color: rgba(99, 102, 241, 0.06);
        border-color: rgba(99, 102, 241, 0.22);
    }

    /* Welcome Hero Card */
    .hero-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(16, 185, 129, 0.06) 100%);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 1.75rem;
        margin-bottom: 1.25rem;
    }
    .hero-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.35rem;
    }
    .hero-subtitle {
        font-size: 0.95rem;
        opacity: 0.85;
        line-height: 1.5;
    }

    /* Pill buttons for starter prompts */
    div.stButton > button {
        border-radius: 10px;
        font-size: 0.86rem;
        padding: 0.55rem 0.85rem;
        transition: all 0.2s ease;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 4. Sidebar: Knowledge Base & Session Controls
with st.sidebar:
    st.markdown("### 🧠 Adaptive RAG")
    st.caption("Agentic Routing • FAISS • Tavily • MongoDB")

    st.divider()

    # Active Knowledge Base Status
    st.markdown("**📂 Knowledge Base**")
    if st.session_state.active_doc:
        st.badge(
            f"Indexed: {st.session_state.active_doc}",
            icon=":material/check_circle:",
            color="green",
        )
    else:
        st.badge(
            "No document uploaded",
            icon=":material/info:",
            color="gray",
        )

    # Document Upload Form
    with st.form("upload_form", clear_on_submit=True):
        uploaded_file = st.file_uploader(
            "Upload Document",
            type=["pdf", "txt", "docx"],
            help="Supported formats: PDF, TXT, DOCX",
        )
        doc_description = st.text_input(
            "Document Description",
            placeholder="e.g., Lab 2 Java OOP assignment & code",
            help="Helps the LangGraph router decide when to search this file.",
        )
        submitted = st.form_submit_button(
            "Index Document",
            icon=":material/upload_file:",
            use_container_width=True,
            type="primary",
        )

        if submitted:
            if not uploaded_file:
                st.warning("Please select a PDF, TXT, or DOCX file first.")
            elif not doc_description.strip():
                st.warning("Please enter a short description of the file.")
            else:
                with st.spinner("Chunking & embedding document..."):
                    success = upload_document(uploaded_file, doc_description.strip())
                if success:
                    st.session_state.active_doc = uploaded_file.name
                    st.toast(f"Indexed {uploaded_file.name}!", icon="✅")
                    st.rerun()
                else:
                    st.error("Upload failed. If the backend was sleeping, retry in 15s.")

    st.divider()

    # Session Management
    st.markdown("**⚙️ Session Controls**")
    st.caption(f"Session ID: `{st.session_state.session_id}`")

    if st.button(
        "New Conversation",
        icon=":material/refresh:",
        use_container_width=True,
    ):
        st.session_state.session_id = f"guest-{uuid.uuid4().hex[:8]}"
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption(
        "ℹ️ **Cold-Start Note:** Hosted on Render's free tier—first message after 15m idle takes ~30s to wake the server."
    )

# 5. Helper to Process a Prompt
def handle_user_prompt(prompt_text: str):
    st.session_state.messages.append({"role": "user", "content": prompt_text})
    with st.chat_message("user", avatar=":material/person:"):
        st.markdown(prompt_text)

    with st.chat_message("assistant", avatar=":material/smart_toy:"):
        with st.spinner("Routing query & generating response..."):
            response = send_query(prompt_text, st.session_state.session_id)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})


# 6. Main Chat Area: Empty-State Welcome Hero OR Message History
if not st.session_state.messages:
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">Adaptive RAG Multi-Agent Assistant</div>
            <div class="hero-subtitle">
                Ask a question below—the <b>LangGraph router</b> automatically decides whether to
                retrieve from your uploaded documents, search the live web via <b>Tavily</b>, or answer directly.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption("✨ Try a quick starter prompt:")
    col1, col2, col3 = st.columns(3)
    starter_prompt = None

    with col1:
        if st.button("📄 Summarize uploaded doc", use_container_width=True):
            starter_prompt = "Summarize the main points and key details from the uploaded document."
    with col2:
        if st.button("🌐 Latest AI news (Web)", use_container_width=True):
            starter_prompt = "What are the latest breakthroughs in agentic AI workflows?"
    with col3:
        if st.button("💡 Explain Adaptive RAG", use_container_width=True):
            starter_prompt = "How does Adaptive RAG differ from standard naive RAG pipelines?"

    if starter_prompt:
        handle_user_prompt(starter_prompt)
        st.rerun()
else:
    for msg in st.session_state.messages:
        avatar = ":material/person:" if msg["role"] == "user" else ":material/smart_toy:"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

# 7. Bottom Chat Input
if user_input := st.chat_input("Ask anything about your documents or the web..."):
    handle_user_prompt(user_input)