import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

# Fix the typo and fallback to check both OPENAI_API_KEY and OPENROUTER_API_KEY
api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError(
        "Missing API key! Please set OPENAI_API_KEY or OPENROUTER_API_KEY in your environment."
    )

# Set OpenRouter credentials
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"
os.environ["OPENAI_API_KEY"] = api_key

# Use an open-source model available on OpenRouter
llm = ChatOpenAI(model="meta-llama/llama-3.3-70b-instruct", temperature=0)
