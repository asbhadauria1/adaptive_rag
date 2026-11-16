# Adaptive RAG - Agentic AI Chatbot

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit%20Cloud-FF4B4B?logo=streamlit&logoColor=white)](YOUR_STREAMLIT_APP_URL_HERE)
[![Backend API](https://img.shields.io/badge/API%20Docs-FastAPI%20on%20Render-009688?logo=fastapi&logoColor=white)](https://adaptive-rag-backend-c8m7.onrender.com/docs)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.5.4-orange.svg)](https://python.langchain.com/langgraph/)
[![FAISS](https://img.shields.io/badge/FAISS-VectorDB-purple.svg)](https://github.com/facebookresearch/faiss)

## 📋 Overview

**Adaptive RAG** is an intelligent, end-to-end Retrieval-Augmented Generation (RAG) system powered by agentic AI architecture. It combines dynamic query routing, multi-format document retrieval, and LLM reasoning to provide accurate, context-aware answers to user queries.

Instead of running blind vector retrieval on every prompt, the system dynamically adapts its retrieval strategy based on query intent—routing across **uploaded documents (FAISS)**, **general LLM knowledge (OpenRouter)**, or **real-time web search (Tavily)** while persisting per-session chat history in **MongoDB Atlas**.

---

## 🎯 Key Features

### 🧠 Intelligent Query Routing

- **Adaptive Classification**: Automatically routes queries to the most appropriate processing pipeline
- **Three Query Types**:
  - **Index**: Queries answerable from uploaded documents
  - **General**: Queries answerable with general knowledge
  - **Search**: Queries requiring real-time web search

### 📚 Advanced RAG Pipeline

- **Document Processing**: Recursive character chunking (`1000` chars / `150` overlap) and LLM-enhanced document descriptions
- **Vector Search**: Fast similarity-based retrieval using **FAISS** (`faiss-cpu`)
- **OpenRouter Cloud Embeddings**: Lightweight OpenRouter API embeddings (`OpenAIEmbeddings` routed via OpenRouter) paired with lazy-loaded singletons to eliminate local PyTorch RAM overhead and run within a 512MB cloud container
- **Relevance Grading & Rewriting**: Evaluates retrieved chunks and refines queries for stronger retrieval accuracy

### 🤖 Agentic AI Architecture

- **LangGraph Workflow**: Stateful orchestration across query analysis, retrieval, web search, and response generation
- **ReAct Framework**: Reasoning and Acting tool-calling loop with dynamic retriever tool descriptions
- **Tool Integration**: Seamless routing between custom document retrieval and Tavily web search

### 💾 State Management

- **MongoDB Atlas Backend**: Persistent asynchronous chat history via `motor`
- **Session Isolation**: Independent conversation contexts tracked per visitor `session_id`

### 🎨 User Interface

- **Streamlit Web App**: Centered chat layout with custom message cards, quick-start prompt buttons, and live indexed-document status badges
- **Zero-Friction Guest Access**: Automatically initializes a guest session (`guest-<id>`) on load—no login wall required
- **Multi-Format File Support**: Upload **PDF, TXT, and DOCX** documents directly from the sidebar

### ⚡ API-First Architecture

- **FastAPI Backend**: High-performance asynchronous REST API deployed on Render
- **RESTful Endpoints**: Clean JSON and multipart endpoints documented via Swagger UI (`/docs`)

---

## 🏗️ Architecture

### System Components

```text
+-----------------------------------------------------------------+
|                         User Interface                          |
|  +-----------------------------------------------------------+  |
|  |  Streamlit Web Application (Streamlit Community Cloud)    |  |
|  |  • Chat Interface & Starter Prompts                       |  |
|  |  • Document Upload (PDF, TXT, DOCX)                       |  |
|  |  • Automatic Guest Session Management                     |  |
|  +-----------------------------------------------------------+  |
+-----------------------------------------------------------------+
                                 |
                                 v
+-----------------------------------------------------------------+
|                   FastAPI Backend (Render)                      |
|  +-----------------------------------------------------------+  |
|  |  REST API Endpoints                                       |  |
|  |  • POST /rag/query                                        |  |
|  |  • POST /rag/documents/upload                             |  |
|  +-----------------------------------------------------------+  |
+-----------------------------------------------------------------+
                                 |
                                 v
+-----------------------------------------------------------------+
|                    LangGraph Orchestration                      |
|  +---------+   +----------+   +---------+   +----------+        |
|  | Query   |-->| Classify |-->| Router  |-->| Pipeline |        |
|  | Analyze |   | Query    |   | Output  |   | Exec     |        |
|  +---------+   +----------+   +---------+   +----------+        |
+-----------------------------------------------------------------+
                                 |
        +------------------------+------------------------+
        v                        v                        v
   +----------+            +-----------+           +-------------+
   | Retriever|            | General   |           | Web Search  |
   | (FAISS)  |            | LLM       |           | (Tavily)    |
   +----------+            +-----------+           +-------------+
        |                        |                        |
        +------------------------+------------------------+
                                 |
                                 v
                  +-----------------------------+
                  | Response + MongoDB History  |
                  +-----------------------------+
```

### Graph Nodes

1. **query_analysis**: Analyzes and classifies incoming queries
2. **retriever**: Retrieves relevant chunks from the FAISS vector store
3. **grade**: Evaluates relevance of retrieved documents
4. **rewrite**: Optimizes query phrasing for better retrieval results
5. **generate**: Generates final response from retrieved context
6. **web_search**: Performs real-time web search via Tavily when needed
7. **general_llm**: Provides direct general knowledge answers

---

## 📦 Project Structure

```text
adaptive_rag/
├── src/                              # Main backend source code
│   ├── main.py                       # FastAPI application entry point & CORS
│   ├── api/                          # API routes and endpoints
│   │   └── routes.py                 # /rag/query and /rag/documents/upload endpoints
│   ├── config/                       # Configuration management
│   │   ├── settings.py               # OpenRouter, Tavily & MongoDB settings
│   │   └── prompts.yaml              # LLM prompts and system messages
│   ├── core/                         # Core utilities
│   │   ├── config.py                 # Core configuration
│   │   └── logger.py                 # Logging setup
│   ├── db/                           # Database layer
│   │   └── mongo_client.py           # Async MongoDB Atlas client initialization
│   ├── llms/                         # Language model integrations
│   │   └── openai.py                 # OpenRouter LLM initialization (OpenAI-compatible client)
│   ├── memory/                       # Chat memory management
│   │   ├── chat_history_mongo.py     # MongoDB-backed session chat history
│   │   └── chathistory_in_memory.py  # In-memory chat history (fallback)
│   ├── models/                       # Pydantic data models and schemas
│   │   ├── state.py                  # LangGraph state definition
│   │   ├── query_request.py          # Query request schema
│   │   ├── grade.py                  # Relevance grade model
│   │   ├── route_identifier.py       # Route classification model
│   │   └── verification_result.py    # Answer verification model
│   ├── rag/                          # RAG pipeline implementation
│   │   ├── graph_builder.py          # LangGraph workflow construction
│   │   ├── nodes.py                  # Graph node implementations
│   │   ├── retriever_setup.py        # OpenRouter embeddings & FAISS retriever setup
│   │   ├── document_upload.py        # PDF, TXT, and DOCX parsing & chunking
│   │   └── reAct_agent.py            # ReAct agent setup
│   └── tools/                        # Utility tools and functions
│       ├── common_tools.py           # Description enhancement & shared utilities
│       └── graph_tools.py            # Graph routing and decision tools
│
├── streamlit_app/                    # Streamlit web application
│   ├── home.py                       # Auto-guest session initializer & entry point
│   ├── pages/                        # Multi-page application
│   │   └── chat.py                   # Chat interface & multi-format document upload
│   └── utils/                        # Streamlit utilities
│       └── api_client.py             # Backend REST API client
│
├── README.md                         # Project overview & setup guide
├── requirements.txt                  # Python dependencies
├── CODE_STYLE_GUIDE.md               # Code formatting standards
├── DOCUMENTATION_INDEX.md            # Documentation navigation index
├── DOCUMENT_FLOW_VISUAL.md           # Visual architecture diagrams
├── DOCUMENT_UPLOAD_FLOW.md           # Document ingestion details
└── QUICK_REFERENCE.md                # Quick reference guide
```

---

## 🔌 API Endpoints

### Live & Local Base URLs

- **Production (Render):** `https://adaptive-rag-backend-c8m7.onrender.com`
- **Local Development:** `http://localhost:8000`

### 1. Query Endpoint

**Process a RAG query and get an intelligent response**

```http
POST /rag/query
Content-Type: application/json

{
  "query": "What is the main topic of the document?",
  "session_id": "guest-a1b2c3d4"
}
```

**Response:**

```json
{
  "result": {
    "type": "ai",
    "content": "Based on the document, the main topic is..."
  }
}
```

**Parameters:**

- `query` (string, required): User's question or query
- `session_id` (string, required): Unique session identifier for conversation tracking

---

### 2. Document Upload Endpoint

**Upload documents for FAISS vector indexing**

```http
POST /rag/documents/upload
X-Description: Brief description of the document

Form Data:
- file: <PDF, TXT, or DOCX file>
```

**Response:**

```json
{
  "status": true
}
```

**Headers:**

- `X-Description` (string, required): Document description used by the agent router

**Supported Formats:**

- PDF (`.pdf`)
- Plain Text (`.txt`)
- Word Document (`.docx`)

---

## 📖 Usage Guide

### 1. Prerequisites

- Python 3.9 or higher
- MongoDB Atlas URI (or local MongoDB instance)
- OpenRouter API key (used across LLM generation, query routing, and vector embeddings)
- Tavily API key (for real-time web search)

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/asbhadauria1/adaptive_rag.git
cd adaptive_rag

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the project root:

```env
# OpenRouter Configuration (LLM & Embeddings across settings.py, openai.py, retriever_setup.py)
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Tavily Search Configuration
TAVILY_API_KEY=your_tavily_api_key_here

# MongoDB Atlas Configuration
MONGODB_URL=your_mongodb_connection_string_here
MONGODB_DB_NAME=adaptive_rag
```

### 4. Running the Application Locally

**Start FastAPI Backend:**

```bash
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Start Streamlit Frontend:**

```bash
streamlit run streamlit_app/home.py
```

**Access Locally:**

- Web Interface: `http://localhost:8501`
- Swagger API Docs: `http://localhost:8000/docs`

### 5. Example Usage

**Using the Web Interface:**

1. Open the live Streamlit app (or `http://localhost:8501`)—a guest session is initialized automatically
2. Upload a `.pdf`, `.txt`, or `.docx` file with a brief description in the sidebar
3. Click a starter prompt or ask any question in the chat input

**Using cURL:**

```bash
# Upload a document
curl -X POST https://adaptive-rag-backend-c8m7.onrender.com/rag/documents/upload \
  -H "X-Description: Sample document about Python" \
  -F "file=@document.pdf"

# Query the RAG system
curl -X POST https://adaptive-rag-backend-c8m7.onrender.com/rag/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Summarize the uploaded document",
    "session_id": "user_123"
  }'
```

---

## ☁️ Deployment

- **Backend (Render):** Deployed as a FastAPI web service at `https://adaptive-rag-backend-c8m7.onrender.com`. Because it runs on Render's free tier (512MB RAM), the container sleeps after 15 minutes of inactivity—allow ~30 seconds for the first request to wake the server.
- **Frontend (Streamlit Community Cloud):** Runs `streamlit_app/home.py` and connects to the Render backend via `PYTHON_BASE_URL` (configured in Streamlit Secrets, defaulting to the live Render URL).

---

## 📊 Performance Optimization

- **Low-Memory Cloud Architecture**: Replaced local PyTorch/HuggingFace embedding weights with OpenRouter API embeddings and lazy-loaded singletons, reducing backend RAM footprint to ~130MB
- **Document Chunking**: Configurable recursive splitting (`1000` chars, `150` overlap) via `RecursiveCharacterTextSplitter`
- **Fast Vector Lookup**: In-memory **FAISS** similarity search with dynamic tool descriptions
- **Async Persistence**: Non-blocking MongoDB Atlas operations via `motor`

---

## 📚 Technology Stack

| Component | Technology | Version |
| :--- | :--- | :--- |
| **LLM Framework** | LangChain | `~0.3.27` |
| **Workflow Orchestration** | LangGraph | `~0.5.4` |
| **Web Framework** | FastAPI | Latest |
| **ASGI Server** | Uvicorn | Latest |
| **UI Framework** | Streamlit | Latest |
| **Vector Store** | FAISS (`faiss-cpu`) | Latest |
| **Embeddings** | OpenRouter API Embeddings | Latest |
| **Chat Database** | MongoDB Atlas (`motor`) | Latest |
| **Document Loaders** | `pypdf`, `docx2txt`, `TextLoader` | Latest |
| **LLM Provider** | OpenRouter | Latest |
| **Web Search** | Tavily | Latest |
| **Data Validation** | Pydantic | `~2.11.7` |

---

## 📝 Documentation References

- [CODE_STYLE_GUIDE.md](CODE_STYLE_GUIDE.md) - Comprehensive coding standards
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Quick patterns and templates
- [DOCUMENT_FLOW_VISUAL.md](DOCUMENT_FLOW_VISUAL.md) - Visual pipeline flows
- [DOCUMENT_UPLOAD_FLOW.md](DOCUMENT_UPLOAD_FLOW.md) - Document ingestion details
- [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) - Full documentation index

---

## ❓ FAQ

**Q: How do I upload multiple documents?**  
A: Upload one document at a time through the Streamlit sidebar (`PDF`, `TXT`, or `DOCX`). Each upload indexes the new document into the active FAISS store.

**Q: Why does the first request sometimes take ~30 seconds?**  
A: The backend runs on Render's free tier, which spins down after 15 minutes of inactivity. Once awake, subsequent queries respond within seconds.

**Q: How is conversation history stored?**  
A: MongoDB Atlas stores chat messages keyed by `session_id` for multi-turn context retention.

---

## 📄 License

This project is open-source under the MIT License.

---

## 👤 Author

**Aditya Singh Bhadauria**

- GitHub: [@asbhadauria1](https://github.com/asbhadauria1)
- Project: [Adaptive RAG](https://github.com/asbhadauria1/adaptive_rag)