import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

class Config:
    LLM_WRAPPER_URL = os.getenv("LLM_WRAPPER_URL")
    LLM_API_TOKEN = os.getenv("LLM_API_TOKEN")
    SECRET_KEY = os.getenv("SECRET_KEY")