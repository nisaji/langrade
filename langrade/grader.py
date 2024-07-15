from typing import Optional
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

SYSTEM_PROMPT = """
You are a grader assessing the relevance of a retrieved document to a user question.
Your goal is to filter out erroneous retrievals without being overly strict.
If the document contains keywords or semantic meanings related to the user question, grade it as relevant.
Give a binary score ('yes' or 'no') to indicate whether the document is relevant to the question.
"""


class GradeDocumentsWithReasoning(BaseModel):
    reasoning: str = Field(
        description="Thinking process to give a correct binary score shortly."
    )
    binary_score: str = Field(
        description="Documents are relevant to the question, 'yes' or 'no'"
    )


class GradeDocumentsWithoutReasoning(BaseModel):
    binary_score: str = Field(
        description="Documents are relevant to the question, 'yes' or 'no'"
    )


class DocumentGrader:
    def __init__(
        self, api_key: str, model: str = "gpt-3.5-turbo-0125", reasoning: bool = True
    ):
        self.llm = ChatOpenAI(api_key=api_key, model=model)
        self.reasoning = reasoning
        self.prompt = self._create_prompt()

    def _create_prompt(self):
        return ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_PROMPT),
                (
                    "human",
                    "Retrieved document: \n\n {document} \n\n User question: \n\n {question}",
                ),
            ]
        )

    def grade_document(self, document: str, question: str):
        if self.reasoning:
            structured_llm = self.llm.with_structured_output(
                GradeDocumentsWithReasoning
            )
        else:
            structured_llm = self.llm.with_structured_output(
                GradeDocumentsWithoutReasoning
            )

        chain = self.prompt | structured_llm
        return chain.invoke({"document": document, "question": question})


def document_grader(
    api_key: str, model: str = "gpt-3.5-turbo-0125", reasoning: bool = True
) -> DocumentGrader:
    return DocumentGrader(api_key, model, reasoning)
