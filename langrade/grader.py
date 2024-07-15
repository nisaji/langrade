from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from .constants import (
    SYSTEM_PROMPT,
    DEFAULT_MODEL,
    REASONING_DESCRIPTION,
    BINARY_SCORE_DESCRIPTION,
)
import html


class GradeDocuments(BaseModel):
    reasoning: str = Field(description=REASONING_DESCRIPTION)
    binary_score: str = Field(description=BINARY_SCORE_DESCRIPTION)


class DocumentGrader:
    def __init__(self, api_key: str, model: str = DEFAULT_MODEL):
        self.llm = ChatOpenAI(api_key=api_key, model=model)
        self.prompt = self._create_prompt()

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

    def grade_document(self, document: str, question: str):
        # Sanitize inputs
        safe_document = html.escape(document)
        safe_question = html.escape(question)

        structured_llm = self.llm.with_structured_output(GradeDocuments)
        chain = self.prompt | structured_llm
        result = chain.invoke(
            {"document": safe_document, "question": safe_question}
        )  # noqa: E501
        return result


def document_grader(
    api_key: str, model: str = DEFAULT_MODEL
) -> DocumentGrader:  # noqa: E501
    return DocumentGrader(api_key, model)
