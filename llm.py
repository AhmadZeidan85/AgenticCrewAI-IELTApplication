import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_HUB_TOKEN")
MODEL_NAME = os.getenv(
    "MODEL_NAME", "mistralai/Mistral-7B-Instruct-v0.2:featherless-ai"
)

def load_hf_llm():
    """
    Load Hugging Face Mistral-7B-Instruct via OpenAI-compatible Router API.
    Works for gated models with token access.
    """
    if not HF_TOKEN:
        raise ValueError("HF_HUB_TOKEN is not set in environment.")

    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=HF_TOKEN
    )
    return client
