from .base import LLMEngine
from anthropic import Anthropic


class ClaudeEngine(LLMEngine):
    def __init__(self, api_key: str, model: str):
        self.client = Anthropic(api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> str:
        response = self.client.completions.create(
            model=self.model, prompt=prompt, max_tokens_to_sample=300
        )
        return response.completion

    def with_structured_output(self, output_parser_class):
        # Implement structured output for Claude
        pass
