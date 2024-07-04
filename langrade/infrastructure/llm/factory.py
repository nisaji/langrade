from .base import LLMEngine
from .openai_engine import OpenAIEngine


def create_llm_engine(engine_type: str, api_key: str, model: str) -> LLMEngine:
    if engine_type == "openai":
        return OpenAIEngine(api_key, model)
    else:
        raise ValueError(f"Unsupported LLM engine type: {engine_type}")
