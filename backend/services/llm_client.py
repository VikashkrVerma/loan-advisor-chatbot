import requests
import json
from ..config import Config

def call_llm(prompt):
    url = Config.LLM_WRAPPER_URL
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {Config.LLM_API_TOKEN}"
    }
    payload = {
        "prompt": prompt,
        "metadata": {"client": "loan-advisor", "traceId": "demo"}
    }
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        return data.get("response") or data.get("text") or data.get("content") or str(data)
    except Exception as e:
        print(f"LLM call failed: {e}")
        return None