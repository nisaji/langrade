from abc import ABC, abstractmethod
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from .constants import SYSTEM_PROMPT, DEFAULT_MODEL


class LLMProvider(ABC):
    def __init__(self, api_key: str, model: str):
        self.llm = self._create_llm(api_key, model)

    @abstractmethod
    def _create_llm(self, api_key: str, model: str):
        pass

    async def agenerate(self, prompt: str) -> str:
        messages = [
            ("human", prompt),
        ]
        chat_prompt = ChatPromptTemplate.from_messages(messages)
        chain = chat_prompt | self.llm
        result = await chain.ainvoke({})
        return result.content


class OpenAIProvider(LLMProvider):
    def _create_llm(self, api_key: str, model: str):
        return ChatOpenAI(api_key=api_key, model=model)


class AnthropicProvider(LLMProvider):
    def _create_llm(self, api_key: str, model: str):
        return ChatAnthropic(api_key=api_key, model_name=model)


class GoogleProvider(LLMProvider):
    def _create_llm(self, api_key: str, model: str):
        return ChatGoogleGenerativeAI(google_api_key=api_key, model=model)


class GroqProvider(LLMProvider):
    def _create_llm(self, api_key: str, model: str):
        return ChatGroq(groq_api_key=api_key, model_name=model)


class LLMProviderFactory:
    @staticmethod
    def create_provider(
        provider: str, api_key: str, model: str = DEFAULT_MODEL
    ) -> LLMProvider:
        if provider == "openai":
            return OpenAIProvider(api_key, model)
        elif provider == "anthropic":
            return AnthropicProvider(api_key, model)
        elif provider == "google":
            return GoogleProvider(api_key, model)
        elif provider == "groq":
            return GroqProvider(api_key, model)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
