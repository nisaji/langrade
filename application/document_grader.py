from langchain_core.prompts import ChatPromptTemplate
from langchain import LLM
from ..domain.models import (
    GradeDocumentsWithReasoning,
    GradeDocumentsWithoutReasoning,
)  # noqa: E501
from ..constants import SYSTEM_PROMPT


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

    def grade_document(self, document: str, question: str):
        prompt = self.create_prompt()
        return prompt | self.structured_llm.invoke(
            {"document": document, "question": question}
        )
