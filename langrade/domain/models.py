from typing import Any, Dict, List
from langchain_core.pydantic_v1 import BaseModel, Field
from langrade.constants import (
    GRADE_REASONING_DESCRIPTION,
    BINARY_SCORE_DESCRIPTION,
)
from abc import ABC, abstractmethod
from langchain_community.document_loaders import WebBaseLoader
from langchain.schema import BaseLLMOutputParser
from typing import Optional


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

    def parse_result(self, result: List[str]) -> Dict[str, Any]:
        text = "\n".join(result)  # リストを文字列に結合
        parts = text.split("\n")
        self.reasoning = parts[0] if len(parts) > 1 else ""
        self.binary_score = parts[-1].lower() if parts else ""
        return self.dict()


class GradeDocumentsWithoutReasoning(BaseModel, BaseLLMOutputParser):
    binary_score: Optional[str] = Field(
        default=None, description=BINARY_SCORE_DESCRIPTION
    )

    def parse_result(self, result: List[str]) -> Dict[str, Any]:
        text = "\n".join(result)  # リストを文字列に結合
        self.binary_score = text.strip().lower()
        return self.dict()
