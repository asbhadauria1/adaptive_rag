"""
OpenAI/OpenRouter LLM client configuration.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

api_key = (
    os.getenv("OPENROUTER_API_KEY")
    or os.getenv("OPENAI_API_KEY")
    or os.getenv("OPENOROUTER_API_KEY")
)

if not api_key:
    raise ValueError(
        "Missing API key! Please set OPENROUTER_API_KEY or OPENAI_API_KEY in Render Environment."
    )

os.environ["OPENAI_API_KEY"] = api_key
os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"

llm = ChatOpenAI(
    model="meta-llama/llama-3.3-70b-instruct",
    temperature=0,
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
)
