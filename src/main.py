"""
Main FastAPI application entry point with non-blocking port binding.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import threading
import sys
import traceback

app = FastAPI(title="Adaptive RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Track initialization state so you can see progress at the root URL
app_state = {"ready": False, "error": None}


def load_routes_in_background():
    """Load heavy RAG/LangGraph routes after Uvicorn has already bound to $PORT."""
    try:
        print("⏳ [Background] Importing src.api.routes...", flush=True)
        from src.api.routes import router

        app.include_router(router)
        app_state["ready"] = True
        print(
            "✅ [Background] Routes and RAG pipeline loaded successfully!", flush=True
        )
    except Exception as e:
        app_state["error"] = str(e)
        print(
            "\n================ CRITICAL TRACEBACK ================",
            file=sys.stderr,
            flush=True,
        )
        traceback.print_exc(file=sys.stderr)
        print(
            "=====================================================\n",
            file=sys.stderr,
            flush=True,
        )


@app.on_event("startup")
async def startup_event():
    print("🚀 FastAPI server booting — opening port immediately...", flush=True)
    threading.Thread(target=load_routes_in_background, daemon=True).start()


@app.get("/")
async def root():
    """Root endpoint to verify API and background initialization status."""
    return {
        "message": "Adaptive RAG API is running",
        "ready": app_state["ready"],
        "error": app_state["error"],
    }
