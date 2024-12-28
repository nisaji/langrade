import unittest
from unittest.mock import patch, MagicMock
from .utils import get_provider_credentials
from langrade import create_retriever


class TestRetriever(unittest.TestCase):
    def setUp(self):
        _, self.api_key = get_provider_credentials("vertexai")
        if not self.api_key:
            self.skipTest("VertexAI credentials not available")

        self.urls = [
            "https://lilianweng.github.io/posts/2023-06-23-agent/",
            "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
            "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
        ]
        self.mock_content = "This is a test document"
        self.mock_ai_content = "AI is a field of computer science."

    def _setup_mocks(self, mock_web_loader, mock_embeddings):
        mock_doc = MagicMock()
        mock_doc.page_content = self.mock_content
        mock_web_loader.return_value.load.return_value = [mock_doc]
        return mock_doc

    @patch("langrade.retriever.WebBaseLoader")
    @patch("langrade.retriever.VertexAIEmbeddings")
    def test_create_retriever(self, mock_embeddings, mock_web_loader):
        self._setup_mocks(mock_web_loader, mock_embeddings)
        mock_embeddings.return_value.embed_documents.return_value = [[0.1, 0.2, 0.3]]
        mock_embeddings.return_value.embed_query.return_value = [0.1, 0.2, 0.3]

        retriever = create_retriever(self.urls, self.api_key)
        self.assertIsNotNone(retriever)
        mock_web_loader.assert_called()
        mock_embeddings.assert_called()

    @patch("langrade.retriever.WebBaseLoader")
    @patch("langrade.retriever.VertexAIEmbeddings")
    def test_retriever_get_relevant_documents(self, mock_embeddings, mock_web_loader):
        mock_doc = self._setup_mocks(mock_web_loader, mock_embeddings)
        mock_embeddings.return_value.embed_documents.return_value = [[0.1, 0.2, 0.3]]
        mock_embeddings.return_value.embed_query.return_value = [0.1, 0.2, 0.3]

        retriever = create_retriever(self.urls, self.api_key)
        docs = retriever.get_relevant_documents("What is AI?")

        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0].page_content, self.mock_content)
