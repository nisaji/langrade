from abc import ABC, abstractmethod
import json
from typing import Union
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from google.oauth2 import service_account
from vertexai.generative_models import (
    GenerativeModel,
    Tool,
    FunctionDeclaration,
)


import vertexai
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


class VertexAIProvider(LLMProvider):
    def _create_llm(self, credentials: Union[str, dict], model: str):
        if isinstance(credentials, str):
            try:
                with open(credentials) as f:
                    credentials_dict = json.load(f)
            except Exception as e:
                raise ValueError(f"Failed to load credentials file: {str(e)}")
        else:
            credentials_dict = credentials

        project_id = credentials_dict.get("project_id")
        location = credentials_dict.get("location", "asia-northeast1")

        if not project_id:
            raise ValueError("project_id is required in credentials")

        # Convert dict credentials to Google credentials object
        credentials_object = service_account.Credentials.from_service_account_info(
            credentials_dict
        )

        # Initialize VertexAI with the proper credentials object
        vertexai.init(
            project=project_id, location=location, credentials=credentials_object
        )

        # Rest of your function remains the same
        grade_function = FunctionDeclaration(
            name="grade_document",
            description="Grade a document based on its relevance to a question",
            parameters={
                "type": "object",
                "properties": {
                    "reasoning": {
                        "type": "string",
                        "description": "Explanation for the grading decision",
                    },
                    "binary_score": {
                        "type": "string",
                        "enum": ["yes", "no"],
                        "description": "Whether the document is relevant",
                    },
                },
                "required": ["reasoning", "binary_score"],
            },
        )

        self.model = GenerativeModel(
            model, tools=[Tool(function_declarations=[grade_function])]
        )
        return self.model

    def grade_document(self, document: str, question: str) -> GradeDocuments:
        prompt = self._create_prompt().format(document=document, question=question)
        chat = self.model.start_chat()
        response = chat.send_message(prompt)

        # process function calling result
        if response.candidates and response.candidates[0].function_calls:
            function_call = response.candidates[0].function_calls[0]
            if function_call.name == "grade_document":
                args = function_call.args
                return GradeDocuments(
                    reasoning=args["reasoning"], binary_score=args["binary_score"]
                )

        # fallback
        return GradeDocuments(reasoning="Failed to grade document", binary_score="no")


class LLMProviderFactory:
    @staticmethod
    def create_provider(provider: str, api_key: str, model: str) -> LLMProvider:
        if provider == "openai":
            return OpenAIProvider(api_key, model)
        elif provider == "anthropic":
            return AnthropicProvider(api_key, model)
        elif provider == "vertexai":
            return VertexAIProvider(api_key, model)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
