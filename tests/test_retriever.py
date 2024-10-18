import pytest
from unittest.mock import patch, AsyncMock
from langrade.retriever import create_retriever
from langchain.schema import Document


@pytest.fixture
def api_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "fake_api_key")
    return "fake_api_key"


@pytest.fixture
def urls():
    return [
        "https://lilianweng.github.io/posts/2023-06-23-agent/",
        "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
        "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
    ]


@patch("langrade.retriever.WebBaseLoader")
@patch("langrade.retriever.Chroma")
def test_create_retriever(mock_chroma, mock_web_loader, api_key, urls):
    mock_doc = Document(page_content="This is a test document", metadata={})
    mock_web_loader.return_value.load.return_value = [mock_doc]
    mock_chroma.from_documents.return_value.as_retriever.return_value = AsyncMock()

    retriever = create_retriever(urls, api_key)

    assert retriever is not None
    mock_web_loader.assert_called()
    mock_chroma.from_documents.assert_called()


@pytest.mark.asyncio
@patch("langrade.retriever.WebBaseLoader")
@patch("langrade.retriever.Chroma")
async def test_retriever_get_relevant_documents(
    mock_chroma, mock_web_loader, api_key, urls
):
    mock_doc = Document(page_content="This is a test document", metadata={})
    mock_web_loader.return_value.load.return_value = [mock_doc]
    mock_retriever = AsyncMock()
    mock_chroma.from_documents.return_value.as_retriever.return_value = mock_retriever

    retriever = create_retriever(urls, api_key)
    question = "What is AI?"
    mock_retriever.get_relevant_documents.return_value = [
        Document(page_content="AI is a field of computer science.", metadata={})
    ]

    docs = await retriever.get_relevant_documents(question)

    assert len(docs) == 1
    assert "AI" in docs[0].page_content
