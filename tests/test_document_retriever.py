import unittest
from langrade import web_document_retriever


class TestDocumentRetriever(unittest.TestCase):
    def test_get_relevant_documents(self):
        urls = [
            "https://lilianweng.github.io/posts/2023-06-23-agent/",
            "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",  # noqa: E501
        ]
        retriever = web_document_retriever(urls)
        question = "agent memory"
        documents = retriever.get_relevant_documents(question, top_k=1)
        self.assertTrue(len(documents) > 0)


if __name__ == "__main__":
    unittest.main()
