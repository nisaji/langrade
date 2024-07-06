from .base import LLMEngine
from google.generativeai import GenerativeModel


class GeminiEngine(LLMEngine):
    def __init__(self, api_key: str, model: str):
        self.model = GenerativeModel(model_name=model, api_key=api_key)

    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text

    def with_structured_output(self, output_parser_class):
        # Implement structured output for Gemini
        pass
