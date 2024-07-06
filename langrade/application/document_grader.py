from langchain_core.prompts import ChatPromptTemplate
from ..domain.models import (
    ComparisonInput,
    GradeDocumentsWithReasoning,
    GradeDocumentsWithoutReasoning,
)
from langrade.constants import SYSTEM_PROMPT
from typing import Union
from langrade.infrastructure.llm.base import LLMEngine


class DocumentGrader:
    def __init__(self, llm: LLMEngine, reasoning: bool):
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
                    "Retrieved document: \n\n {document} \n\n User question: \n\n {question}\n\nPlease provide a binary score (yes/no) for relevance, and if applicable, reasoning.",  # noqa: E501
                ),
            ]
        )

    def grade_document(
        self,
        document: Union[str, ComparisonInput],
        question: Union[str, ComparisonInput],
    ):
        if isinstance(document, ComparisonInput):
            document_content = document.get_content()
        else:
            document_content = document

        if isinstance(question, ComparisonInput):
            question_content = question.get_content()
        else:
            question_content = question

        result = self.structured_llm(
            {"document": document_content, "question": question_content}
        )

        print(f"API Response: {result}")

        if isinstance(result, dict) and "binary_score" in result:
            binary_score = result["binary_score"]
        else:
            binary_score = ""

            print(f"Binary Score: {binary_score}")

        if isinstance(result, dict) and "text" in result:
            result = result["text"]

        parsed_result = self.structured_llm.output_parser.parse_result(result)
        return (
            GradeDocumentsWithReasoning(**parsed_result)
            if self.reasoning
            else GradeDocumentsWithoutReasoning(**parsed_result)
        )
