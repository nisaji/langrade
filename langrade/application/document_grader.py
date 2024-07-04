from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseLLM as LLM
from ..domain.models import (
    ComparisonInput,
    GradeDocumentsWithReasoning,
    GradeDocumentsWithoutReasoning,
)  # noqa: E501
from langrade.constants import SYSTEM_PROMPT
from typing import Union


class DocumentGrader:
    def __init__(self, llm: LLM, reasoning: bool):
        self.llm = llm
        self.reasoning = reasoning
        self.structured_llm = self._create_structured_llm()

    def _create_structured_llm(self):
        if self.reasoning:
            return self.llm.with_structured_output(GradeDocumentsWithReasoning)
        else:
            return self.llm.with_structured_output(
                GradeDocumentsWithoutReasoning
            )  # noqa: E501

    def create_prompt(self):
        return ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_PROMPT),
                (
                    "human",
                    "Retrieved document: \n\n {document} \n\n User question: \n\n {question}",  # noqa: E501
                ),
            ]
        )

    def grade_document(
        self,
        document: Union[str, ComparisonInput],
        question: Union[str, ComparisonInput],
    ):
        prompt = self.create_prompt()

        if isinstance(document, ComparisonInput):
            document_content = document.get_content()
        else:
            document_content = document

        if isinstance(question, ComparisonInput):
            question_content = question.get_content()
        else:
            question_content = question

        return prompt | self.structured_llm.invoke(
            {"document": document_content, "question": question_content}
        )
