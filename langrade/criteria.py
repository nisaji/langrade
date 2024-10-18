# criteria.py

from abc import ABC, abstractmethod
from pydantic import BaseModel, Field

from langrade.constants import BINARY_SCORE_DESCRIPTION, REASONING_DESCRIPTION
from .providers import LLMProvider


class CriterionResult(BaseModel):
    binary_score: str = Field(description=BINARY_SCORE_DESCRIPTION)
    reasoning: str = Field(description=REASONING_DESCRIPTION)


class EvaluationCriterion(ABC):
    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider

    @abstractmethod
    async def evaluate(self, document: str, question: str = None) -> CriterionResult:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def prompt(self) -> str:
        pass


class RelevanceCriterion(EvaluationCriterion):
    @property
    def name(self) -> str:
        return "Relevance"

    @property
    def prompt(self) -> str:
        from .constants import RELEVANCE_PROMPT

        return RELEVANCE_PROMPT

    async def evaluate(self, document: str, question: str) -> CriterionResult:
        response = await self.llm_provider.agenerate(
            self.prompt.format(document=document, question=question)
        )
        # Parse the response to extract score and explanation
        # This is a simplified example; you might need more robust parsing
        lines = response.split("\n")
        binary_score = lines[0].split(":")[1].strip().lower()
        reasoning = lines[1].split(":")[1].strip()
        return CriterionResult(binary_score=binary_score, reasoning=reasoning)


class ReadabilityCriterion(EvaluationCriterion):
    @property
    def name(self) -> str:
        return "Readability"

    @property
    def prompt(self) -> str:
        from .constants import READABILITY_PROMPT

        return READABILITY_PROMPT

    async def evaluate(self, document: str, question: str = None) -> CriterionResult:
        response = await self.llm_provider.agenerate(
            self.prompt.format(document=document)
        )
        lines = response.split("\n")
        binary_score = lines[0].split(":")[1].strip().lower()
        reasoning = lines[1].split(":")[1].strip()
        return CriterionResult(binary_score=binary_score, reasoning=reasoning)


class CoherenceCriterion(EvaluationCriterion):
    @property
    def name(self) -> str:
        return "Coherence"

    @property
    def prompt(self) -> str:
        from .constants import COHERENCE_PROMPT

        return COHERENCE_PROMPT

    async def evaluate(self, document: str, question: str = None) -> CriterionResult:
        response = await self.llm_provider.agenerate(
            self.prompt.format(document=document)
        )
        lines = response.split("\n")
        binary_score = lines[0].split(":")[1].strip().lower()
        reasoning = lines[1].split(":")[1].strip()
        return CriterionResult(binary_score=binary_score, reasoning=reasoning)
