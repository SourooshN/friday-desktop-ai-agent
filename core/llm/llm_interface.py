# core/llm/llm_interface.py

import os
import requests
from urllib.parse import quote

# If you set OLLAMA_HOST in your .env, it’ll pick that up; otherwise defaults to localhost
BASE_URL = os.getenv("OLLAMA_HOST", "http://localhost:11434")

def query_model(model: str, prompt: str, timeout: int = 30) -> str:
    """
    Send `prompt` to the Ollama HTTP API for the given `model`,
    URL-encoding the model name so colons don’t break the path.
    Returns the generated completion text.
    """
    # URL-encode the entire model string (e.g. "nous-hermes:13b" → "nous-hermes%3A13b")
    enc_model = quote(model, safe="")
    url = f"{BASE_URL}/models/{enc_model}/predict"

    resp = requests.post(
        url,
        json={"prompt": prompt},
        timeout=timeout
    )
    # Will raise an HTTPError if Ollama returns 4xx/5xx
    resp.raise_for_status()

    data = resp.json()
    # Ollama’s payload uses "completion"
    return data.get("completion", "")
