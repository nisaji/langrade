from langchain_core.prompts import ChatPromptTemplate
from ..domain.models import (
    KnowledgeInput,
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
                    "Retrieved document: \n\n {document} \n\n User question: \n\n {question}\n\nPlease provide your reasoning and a binary score (yes/no) for relevance.",  # noqa: E501
                ),
            ]
        )

    def grade_document(
        self,
        document: Union[str, KnowledgeInput],
        question: Union[str, KnowledgeInput],
    ):
        if isinstance(document, KnowledgeInput):
            document_content = document.get_content()
        else:
            document_content = document

        if isinstance(question, KnowledgeInput):
            question_content = question.get_content()
        else:
            question_content = question

        prompt = self.create_prompt()
        result = self.llm.generate(
            prompt.format(document=document_content, question=question_content)
        )

        print(f"Raw LLM Output: {result}")

        parsed_result = self.structured_llm.output_parser.parse_result(result)
        print(f"Parsed Result: {parsed_result}")

        if self.reasoning:
            return GradeDocumentsWithReasoning(**parsed_result)
        else:
            return GradeDocumentsWithoutReasoning(
                binary_score=parsed_result["binary_score"]
            )
