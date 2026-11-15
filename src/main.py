"""
Main FastAPI application entry point with deep traceback printing.
"""

from fastapi import FastAPI
import sys
import traceback

app = FastAPI(title="Adaptive RAG API")


@app.on_event("startup")
async def startup_event():
    """
    Catch and print the precise exception traceback during route import.
    """
    print("Starting FastAPI app initialization...", flush=True)
    try:
        from src.api.routes import router

        app.include_router(router)
        print("Routes and modules loaded successfully!", flush=True)
    except Exception as e:
        print("\n================ CRITICAL TRACEBACK ================", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        print(
            "=====================================================\n", file=sys.stderr
        )
        sys.exit(1)


@app.get("/")
async def root():
    """Root endpoint to verify API is running."""
    return {"message": "Adaptive RAG API is running"}
