from abc import ABC, abstractmethod


class LLMEngine(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass
