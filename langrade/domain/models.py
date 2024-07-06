from typing import Any, Dict, List, Union
from langchain_core.pydantic_v1 import BaseModel, Field
from langrade.constants import (
    GRADE_REASONING_DESCRIPTION,
    BINARY_SCORE_DESCRIPTION,
)
from abc import ABC, abstractmethod
from langchain_community.document_loaders import WebBaseLoader
from langchain.schema import BaseLLMOutputParser
from typing import Optional
from langchain.schema import ChatGeneration


class KnowledgeInput(ABC):
    @abstractmethod
    def get_content(self) -> str:
        pass


class TextInput(KnowledgeInput):
    def __init__(self, text: str):
        self.text = text

    def get_content(self) -> str:
        return self.text


class DocumentInput(KnowledgeInput):
    def __init__(self, document: dict):
        self.document = document

    def get_content(self) -> str:
        return self.document.get("content", "")


class URLInput(KnowledgeInput):
    def __init__(self, url: str):
        self.url = url

    def get_content(self) -> str:
        try:
            loader = WebBaseLoader(self.url)
            documents = loader.load()
            if documents:
                return documents[0].page_content
            return ""
        except Exception as e:
            print(f"Error loading URL content: {e}")
            return ""


class GradeDocumentsWithReasoning(BaseModel, BaseLLMOutputParser):
    reasoning: Optional[str] = Field(
        default=None, description=GRADE_REASONING_DESCRIPTION
    )
    binary_score: Optional[str] = Field(
        default=None, description=BINARY_SCORE_DESCRIPTION
    )

    @classmethod
    def parse_result(
        cls, result: Union[str, List[ChatGeneration], Dict[str, Any]]
    ) -> Dict[str, Any]:
        if isinstance(result, dict):
            binary_score = result.get("binary_score", "")
            reasoning = result.get("reasoning", "")
        else:
            if isinstance(result, list) and isinstance(
                result[0], ChatGeneration
            ):  # noqa: E501
                text = result[0].text
            else:
                text = str(result)

            text = text.lower()
            parts = text.split("binary score:")
            reasoning = parts[0].strip() if len(parts) > 1 else ""
            binary_score = parts[-1].strip() if parts else ""

        binary_score = (
            "yes"
            if "yes" in binary_score.lower()
            else (
                "no" if "no" in binary_score.lower() else "no"
            )  # Default to "no" if neither "yes" nor "no" is found
        )

        return {
            "reasoning": reasoning,
            "binary_score": binary_score,
        }


class GradeDocumentsWithoutReasoning(BaseModel, BaseLLMOutputParser):
    binary_score: Optional[str] = Field(
        default=None, description=BINARY_SCORE_DESCRIPTION
    )

    @classmethod
    def parse_result(
        cls, result: Union[str, List[ChatGeneration], Dict[str, Any]]
    ) -> Dict[str, Any]:
        if isinstance(result, dict):
            binary_score = result.get("binary_score", "")
        else:
            if isinstance(result, list) and isinstance(
                result[0], ChatGeneration
            ):  # noqa: E501
                text = result[0].text
            else:
                text = str(result)

            text = text.lower()
            binary_score = "yes" if "yes" in text else "no"

        # Ensure binary_score is always 'yes' or 'no'
        if binary_score.lower() not in ["yes", "no"]:
            binary_score = "no"

        return {
            "binary_score": binary_score,
        }
