import pytest
from unittest.mock import AsyncMock, patch
from langrade import document_grader
from langrade.criteria import (
    RelevanceCriterion,
    ReadabilityCriterion,
    CoherenceCriterion,
)


@pytest.fixture
def mock_llm_provider():
    with patch("langrade.providers.LLMProviderFactory.create_provider") as mock:
        provider = AsyncMock()
        provider.agenerate.return_value = "Binary score (yes/no): yes\nReasoning: The document is relevant and readable."
        mock.return_value = provider
        yield mock


@pytest.mark.asyncio
async def test_grade_document_with_default_criteria(mock_llm_provider):
    grader = document_grader("openai", "fake_api_key")
    result = await grader.grade_document("Test document", "Test question")

    assert "Relevance" in result
    assert "Readability" in result
    assert "Coherence" in result
    assert result["Relevance"]["binary_score"] == "yes"
    assert "relevant" in result["Relevance"]["reasoning"].lower()


@pytest.mark.asyncio
async def test_grade_document_with_custom_criteria(mock_llm_provider):
    custom_criteria = [RelevanceCriterion(mock_llm_provider.return_value)]
    grader = document_grader("openai", "fake_api_key", criteria=custom_criteria)
    result = await grader.grade_document("Test document", "Test question")

    assert "Relevance" in result
    assert "Readability" not in result
    assert "Coherence" not in result


@pytest.mark.asyncio
async def test_grade_document_with_all_criteria(mock_llm_provider):
    all_criteria = [
        RelevanceCriterion(mock_llm_provider.return_value),
        ReadabilityCriterion(mock_llm_provider.return_value),
        CoherenceCriterion(mock_llm_provider.return_value),
    ]
    grader = document_grader("openai", "fake_api_key", criteria=all_criteria)
    result = await grader.grade_document("Test document", "Test question")

    assert "Relevance" in result
    assert "Readability" in result
    assert "Coherence" in result
