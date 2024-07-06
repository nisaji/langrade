import unittest
import os
from dotenv import load_dotenv
from langrade import document_grader
from langrade.domain.models import TextInput, DocumentInput, URLInput

load_dotenv()


class TestDocumentGrader(unittest.TestCase):
    def setUp(self):
        api_key = os.getenv("OPENAI_API_KEY")
        print(f"API Key: {api_key}")  # 追加：APIキーの確認
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY is not set in the environment variables"
            )  # noqa: E501
        self.grader_with_reasoning = document_grader(api_key, reasoning=True)
        self.grader_without_reasoning = document_grader(
            api_key, reasoning=False
        )  # noqa: E501

    def test_grade_document_with_reasoning(self):
        document = "This is a test document about AI."
        question = "What is AI?"
        result = self.grader_with_reasoning.grade_document(document, question)
        print(f"Result with reasoning: {result}")  # 追加：結果の確認
        self.assertIn(result.binary_score, ["yes", "no"])
        self.assertIsNotNone(result.reasoning)

    def test_grade_document_without_reasoning(self):
        document = "This is a test document about AI."
        question = "What is AI?"
        result = self.grader_without_reasoning.grade_document(
            document, question
        )  # noqa: E501
        print(f"Result without reasoning: {result}")  # 追加：結果の確認
        self.assertIn(result.binary_score, ["yes", "no"])
        self.assertFalse(hasattr(result, "reasoning"))

    def test_grade_document_with_text_input(self):
        document = TextInput("This is a test document about AI.")
        question = TextInput("What is AI?")
        result = self.grader_with_reasoning.grade_document(document, question)
        print(f"Result with text input: {result}")  # 追加：結果の確認
        self.assertIn(result.binary_score, ["yes", "no"])
        self.assertIsNotNone(result.reasoning)

    def test_grade_document_with_document_input(self):
        document = DocumentInput(
            {"content": "This is a test document about AI."}
        )  # noqa: E501
        question = "What is AI?"
        result = self.grader_with_reasoning.grade_document(document, question)
        print(f"Result with document input: {result}")  # 追加：結果の確認
        self.assertIn(result.binary_score, ["yes", "no"])
        self.assertIsNotNone(result.reasoning)

    def test_grade_document_with_url_input(self):
        document = URLInput("https://example.com/ai-article")
        question = "What is AI?"
        result = self.grader_with_reasoning.grade_document(document, question)
        print(f"Result with URL input: {result}")  # 追加：結果の確認
        self.assertIn(result.binary_score, ["yes", "no"])
        self.assertIsNotNone(result.reasoning)


if __name__ == "__main__":
    unittest.main()
