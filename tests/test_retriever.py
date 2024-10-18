import unittest
from unittest.mock import patch, MagicMock
from langrade import create_retriever
from conftest import get_api_key
from langchain.schema import Document


class TestRetriever(unittest.TestCase):
    def setUp(self):
        self.api_key = get_api_key()
        self.urls = [
            "https://lilianweng.github.io/posts/2023-06-23-agent/",
            "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
            "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
        ]

    @patch("langrade.retriever.WebBaseLoader")
    @patch("langrade.retriever.Chroma")
    def test_create_retriever(self, mock_chroma, mock_web_loader):
        mock_doc = Document(page_content="This is a test document", metadata={})
        mock_web_loader.return_value.load.return_value = [mock_doc]
        mock_chroma.from_documents.return_value.as_retriever.return_value = MagicMock()

        retriever = create_retriever(self.urls, self.api_key)

        self.assertIsNotNone(retriever)
        mock_web_loader.assert_called()
        mock_chroma.from_documents.assert_called()

    @patch("langrade.retriever.WebBaseLoader")
    @patch("langrade.retriever.Chroma")
    def test_retriever_get_relevant_documents(self, mock_chroma, mock_web_loader):
        mock_doc = Document(page_content="This is a test document", metadata={})
        mock_web_loader.return_value.load.return_value = [mock_doc]
        mock_retriever = MagicMock()
        mock_chroma.from_documents.return_value.as_retriever.return_value = (
            mock_retriever
        )

        retriever = create_retriever(self.urls, self.api_key)
        question = "What is AI?"
        mock_retriever.get_relevant_documents.return_value = [
            Document(page_content="AI is a field of computer science.", metadata={})
        ]

        docs = retriever.get_relevant_documents(question)

        self.assertEqual(len(docs), 1)
        self.assertIn("AI", docs[0].page_content)
