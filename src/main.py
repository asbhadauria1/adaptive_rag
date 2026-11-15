"""
Main FastAPI application entry point with startup error logging.
"""

from fastapi import FastAPI
import sys
import traceback

app = FastAPI(title="Adaptive RAG API")


@app.on_event("startup")
async def startup_event():
    """
    Catch any startup errors and print the exact traceback to Render logs
    instead of failing silently or timing out on port binding.
    """
    try:
        print("Starting FastAPI app initialization...", flush=True)
        from src.api.routes import router

        app.include_router(router)
        print("Routes and modules loaded successfully!", flush=True)
    except Exception as e:
        print("CRITICAL STARTUP ERROR DETECTED:", file=sys.stderr)
        traceback.print_exc()
        raise e


@app.get("/")
async def root():
    """Root endpoint to verify API is running."""
    return {"message": "Adaptive RAG API is running"}
