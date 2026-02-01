import os
import requests
from dotenv import load_dotenv

load_dotenv()
LLAMA_ENDPOINT = os.getenv("LLAMA_ENDPOINT", "http://localhost:11434/api/generate")

# Call local Llama-3.2-3B via Ollama
def call_llama(prompt: str, model_name: str = "llama3.2:3b") -> str:
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False  # disable streaming for simplicity
    }

    resp = requests.post(LLAMA_ENDPOINT, json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json()

    # Ollama returns {"response": "...", "done": true}
    return data.get("response", "")