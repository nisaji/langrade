from .base import LLMEngine
from .openai_engine import OpenAIEngine
import os


def create_llm_engine(engine_type: str) -> LLMEngine:
    if engine_type == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo-0125")
        return OpenAIEngine(api_key, model)
    else:
        raise ValueError(f"Unsupported LLM engine type: {engine_type}")
