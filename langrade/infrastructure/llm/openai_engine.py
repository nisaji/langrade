from .base import LLMEngine
from langchain_openai import ChatOpenAI


class OpenAIEngine(LLMEngine):
    def __init__(self, api_key: str, model: str):
        self.llm = ChatOpenAI(api_key=api_key, model=model)

    def generate(self, prompt: str) -> str:
        return self.llm.predict(prompt)
