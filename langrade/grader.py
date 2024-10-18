from typing import List, Dict
from .providers import LLMProviderFactory
from .criteria import (
    EvaluationCriterion,
    RelevanceCriterion,
    ReadabilityCriterion,
    CoherenceCriterion,
)
from .constants import DEFAULT_MODEL


class DocumentGrader:
    def __init__(
        self,
        provider: str,
        api_key: str,
        model: str = DEFAULT_MODEL,
        criteria: List[EvaluationCriterion] = None,
    ):
        self.llm_provider = LLMProviderFactory.create_provider(provider, api_key, model)
        self.criteria = criteria or [
            RelevanceCriterion(self.llm_provider),
            ReadabilityCriterion(self.llm_provider),
            CoherenceCriterion(self.llm_provider),
        ]

    async def grade_document(
        self, document: str, question: str = None
    ) -> Dict[str, Dict[str, float]]:
        results = {}
        for criterion in self.criteria:
            result = await criterion.evaluate(document, question)
            results[criterion.name] = {
                "binary_score": result.binary_score,
                "reasoning": result.reasoning,
            }
        return results


def document_grader(
    provider: str,
    api_key: str,
    model: str = DEFAULT_MODEL,
    criteria: List[EvaluationCriterion] = None,
) -> DocumentGrader:
    return DocumentGrader(provider, api_key, model, criteria)
