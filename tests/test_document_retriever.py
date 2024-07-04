import os
from dotenv import load_dotenv
import unittest
from langrade import (
    web_document_retriever,
    recursive_web_document_retriever,
    documentdb_retriever,
)
from langrade.domain.models import TextInput, URLInput

load_dotenv()


class TestDocumentRetriever(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api_key = os.getenv("OPENAI_API_KEY")
        if not cls.api_key:
            raise ValueError(
                "OPENAI_API_KEY is not set in the environment variables"
            )  # noqa: E501

    def test_web_document_retriever(self):
        urls = ["https://example.com/ai-article"]
        retriever = web_document_retriever(urls, api_key=self.api_key)
        question = "What is AI?"
        documents = retriever.get_relevant_documents(question, top_k=1)
        self.assertTrue(len(documents) > 0)

    def test_recursive_web_document_retriever(self):
        origin = "https://example.com"
        pages = 2
        retriever = recursive_web_document_retriever(
            origin, pages, api_key=self.api_key
        )
        question = "What is AI?"
        documents = retriever.get_relevant_documents(question, top_k=1)
        self.assertTrue(len(documents) > 0)

    def test_documentdb_retriever(self):
        # Note: This test requires a running MongoDB instance
        uri = "mongodb://localhost:27017"
        db_name = "test_db"
        collection_name = "test_collection"
        num_docs = 10
        retriever = documentdb_retriever(
            uri, db_name, collection_name, num_docs, api_key=self.api_key
        )
        question = "What is AI?"
        documents = retriever.get_relevant_documents(question, top_k=1)
        self.assertTrue(len(documents) > 0)

    def test_retriever_with_text_input(self):
        urls = ["https://example.com/ai-article"]
        retriever = web_document_retriever(urls, api_key=self.api_key)
        question = TextInput("What is AI?")
        documents = retriever.get_relevant_documents(question, top_k=1)
        self.assertTrue(len(documents) > 0)

    def test_retriever_with_url_input(self):
        urls = ["https://example.com/ai-article"]
        retriever = web_document_retriever(urls, api_key=self.api_key)
        question = URLInput("https://example.com/ai-question")
        documents = retriever.get_relevant_documents(question, top_k=1)
        self.assertTrue(len(documents) > 0)
