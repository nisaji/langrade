from abc import ABC, abstractmethod
from langchain_core.pydantic_v1 import BaseModel, Field, SecretStr
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from .constants import (
    SYSTEM_PROMPT,
    DEFAULT_MODEL,
    REASONING_DESCRIPTION,
    BINARY_SCORE_DESCRIPTION,
)


class GradeDocuments(BaseModel):
    reasoning: str = Field(description=REASONING_DESCRIPTION)
    binary_score: str = Field(description=BINARY_SCORE_DESCRIPTION)


class LLMProvider(ABC):
    def __init__(self, api_key: str, model: str):
        self.llm = self._create_llm(api_key, model)
        self.prompt = self._create_prompt()

    @abstractmethod
    def _create_llm(self, api_key: str, model: str):
        pass

    def _create_prompt(self):
        return ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_PROMPT),
                (
                    "human",
                    "Retrieved document: \n\n {document} \n\n User question: \n\n {question}",  # noqa: E501
                ),
            ]
        )

    def grade_document(self, document: str, question: str) -> GradeDocuments:
        structured_llm = self.llm.with_structured_output(GradeDocuments)
        chain = self.prompt | structured_llm
        return chain.invoke({"document": document, "question": question})


class OpenAIProvider(LLMProvider):
    def _create_llm(self, api_key: str, model: str):
        return ChatOpenAI(api_key=api_key, model=model)


class AnthropicProvider(LLMProvider):
    def _create_llm(self, api_key: str, model: str):
        return ChatAnthropic(api_key=api_key, model_name=model)


class GoogleProvider(LLMProvider):
    def _create_llm(self, api_key: str, model: str):
        return ChatGoogleGenerativeAI(google_api_key=api_key, model=model)  # noqa: E501


class GroqProvider(LLMProvider):
    def _create_llm(self, api_key: str, model: str):
        return ChatGroq(groq_api_key=api_key, model_name=model)  # noqa: E501


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
