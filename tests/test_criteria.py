import pytest
from unittest.mock import AsyncMock
from langrade.criteria import (
    RelevanceCriterion,
    ReadabilityCriterion,
    CoherenceCriterion,
)
from langrade.providers import LLMProvider


@pytest.fixture
def mock_llm_provider():
    provider = AsyncMock(spec=LLMProvider)
    provider.agenerate.return_value = "Binary score (yes/no): yes\nReasoning: The document is relevant to the question."
    return provider


@pytest.mark.asyncio
async def test_relevance_criterion(mock_llm_provider):
    criterion = RelevanceCriterion(mock_llm_provider)
    result = await criterion.evaluate("Test document", "Test question")
    assert result.binary_score == "yes"
    assert "relevant" in result.reasoning.lower()


@pytest.mark.asyncio
async def test_readability_criterion(mock_llm_provider):
    criterion = ReadabilityCriterion(mock_llm_provider)
    result = await criterion.evaluate("Test document")
    assert result.binary_score == "yes"
    assert len(result.reasoning) > 0


@pytest.mark.asyncio
async def test_coherence_criterion(mock_llm_provider):
    criterion = CoherenceCriterion(mock_llm_provider)
    result = await criterion.evaluate("Test document")
    assert result.binary_score == "yes"
    assert len(result.reasoning) > 0


@pytest.mark.asyncio
async def test_criterion_with_negative_response(mock_llm_provider):
    mock_llm_provider.agenerate.return_value = "Binary score (yes/no): no\nReasoning: The document is not relevant to the question."
    criterion = RelevanceCriterion(mock_llm_provider)
    result = await criterion.evaluate("Irrelevant document", "Test question")
    assert result.binary_score == "no"
    assert "not relevant" in result.reasoning.lower()
