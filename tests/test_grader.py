import unittest
from langrade import document_grader
from conftest import get_api_key


class TestDocumentGrader(unittest.TestCase):
    def setUp(self):
        self.api_key = get_api_key()
        self.provider = "openai"  # または適切なプロバイダー
        self.grader = document_grader(self.provider, self.api_key)

    def test_grade_document(self):
        document = "AI is a field of computer science that focuses on creating intelligent machines."  # noqa: E501
        question = "What is AI?"

        result = self.grader.grade_document(document, question)
        self.assertIsNotNone(result.binary_score)
        self.assertIsNotNone(result.reasoning)
