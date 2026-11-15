import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

# Set OpenRouter credentials
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"
os.environ["OPENAI_API_KEY"] = os.getenv("OPENOROUTER_API_KEY", "")

# Use an open-source model available on OpenRouter (e.g., Llama 3 or Mistral)
llm = ChatOpenAI(model="meta-llama/llama-3.3-70b-instruct", temperature=0)
