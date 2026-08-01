"""
config.py
---------
Central place to configure the LLM used by every agent + supervisor.

Set OPENAI_API_KEY / OPENAI_API_BASE as environment variables instead of
hardcoding secrets in source. Falls back to the values you originally used.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# find_dotenv() searches this file's directory (and parents) for a .env file,
# so it's found reliably no matter what folder you run `python main.py` from.
_ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH)

MODEL_NAME = os.getenv("AGENT_MODEL_NAME", "hy3")
API_KEY = os.getenv("OPENAI_API_KEY", "")
API_BASE = os.getenv("OPENAI_API_BASE", "https://opencode.ai/zen/go/v1")

_PLACEHOLDER_VALUES = {"", "your-api-key-here"}


def get_llm() -> ChatOpenAI:
    """Returns a fresh ChatOpenAI client using the configured model/endpoint."""
    if API_KEY in _PLACEHOLDER_VALUES:
        raise RuntimeError(
            f"OPENAI_API_KEY is not set.\n"
            f"Looked for a .env file at: {_ENV_PATH}\n"
            f"  - Make sure that file exists (copy .env.example to .env if not)\n"
            f"  - Make sure it contains a line like: OPENAI_API_KEY=sk-...\n"
            f"  - Make sure you replaced the placeholder value, not left it blank"
        )
    return ChatOpenAI(
        model=MODEL_NAME,
        openai_api_key=API_KEY,
        openai_api_base=API_BASE,
    )