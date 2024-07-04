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


class ComparisonInput(ABC):
    @abstractmethod
    def get_content(self) -> str:
        pass


class TextInput(ComparisonInput):
    def __init__(self, text: str):
        self.text = text

    def get_content(self) -> str:
        return self.text


class DocumentInput(ComparisonInput):
    def __init__(self, document: dict):
        self.document = document

    def get_content(self) -> str:
        return self.document.get("content", "")


class URLInput(ComparisonInput):
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
            return result
        if isinstance(result, list) and isinstance(result[0], ChatGeneration):
            text = result[0].text
        else:
            text = result
        parts = text.lower().split("binary score:")
        reasoning = parts[0].strip() if len(parts) > 1 else ""
        binary_score = parts[-1].strip() if parts else ""
        binary_score = (
            "yes"
            if "yes" in binary_score
            else "no" if "no" in binary_score else ""  # noqa: E501
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
            return result
        if isinstance(result, list) and isinstance(result[0], ChatGeneration):
            text = result[0].text
        else:
            text = result
        binary_score = text.lower().strip()
        binary_score = (
            "yes"
            if "yes" in binary_score
            else "no" if "no" in binary_score else ""  # noqa: E501
        )
        return {"binary_score": binary_score}
