from langchain_core.pydantic_v1 import BaseModel, Field
from ..src.langrade.constants import (
    GRADE_REASONING_DESCRIPTION,
    BINARY_SCORE_DESCRIPTION,
)
from abc import ABC, abstractmethod
from langchain_community.document_loaders import WebBaseLoader


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


class GradeDocumentsWithReasoning(BaseModel):
    """Binary score and reasoning for relevance check on retrieved documents."""  # noqa: E501

    reasoning: str = Field(description=GRADE_REASONING_DESCRIPTION)
    binary_score: str = Field(description=BINARY_SCORE_DESCRIPTION)


class GradeDocumentsWithoutReasoning(BaseModel):
    """Binary score for relevance check on retrieved documents."""

    binary_score: str = Field(description=BINARY_SCORE_DESCRIPTION)
