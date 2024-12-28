import unittest
from unittest.mock import patch, MagicMock
from .utils import get_provider_credentials
from langrade import create_retriever


class TestRetriever(unittest.TestCase):
    def setUp(self):
        _, self.api_key = get_provider_credentials("openai")
        if not self.api_key:
            self.skipTest("OpenAI API key not available")

        self.urls = [
            "https://lilianweng.github.io/posts/2023-06-23-agent/",
            "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
            "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
        ]
        self.mock_content = "This is a test document"
        self.mock_ai_content = "AI is a field of computer science."

    def _setup_mocks(self, mock_web_loader, mock_chroma):
        mock_doc = MagicMock()
        mock_doc.page_content = self.mock_content
        mock_web_loader.return_value.load.return_value = [mock_doc]
        return mock_doc

    @patch("langrade.retriever.WebBaseLoader")
    @patch("langrade.retriever.Chroma")
    def test_create_retriever(self, mock_chroma, mock_web_loader):
        self._setup_mocks(mock_web_loader, mock_chroma)
        mock_chroma.from_documents.return_value.as_retriever.return_value = MagicMock()

        retriever = create_retriever(self.urls, self.api_key)

        self.assertIsNotNone(retriever)
        mock_web_loader.assert_called()
        mock_chroma.from_documents.assert_called()

    @patch("langrade.retriever.WebBaseLoader")
    @patch("langrade.retriever.Chroma")
    def test_retriever_get_relevant_documents(self, mock_chroma, mock_web_loader):
        self._setup_mocks(mock_web_loader, mock_chroma)

        mock_retriever = MagicMock()
        mock_chroma.from_documents.return_value.as_retriever.return_value = (
            mock_retriever
        )
        mock_retriever.get_relevant_documents.return_value = [
            MagicMock(page_content=self.mock_ai_content)
        ]

        retriever = create_retriever(self.urls, self.api_key)
        docs = retriever.get_relevant_documents("What is AI?")

        self.assertEqual(len(docs), 1)
        self.assertIn("AI", docs[0].page_content)
        mock_retriever.get_relevant_documents.assert_called_once()
