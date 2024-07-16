import os
import unittest
from dotenv import load_dotenv
from langrade.providers import LLMProviderFactory, GradeDocuments

# 環境変数を読み込む
load_dotenv()


class TestProviders(unittest.TestCase):

    def setUp(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_model = os.getenv("OPENAI_MODEL")
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.gemini_model = os.getenv("GEMINI_MODEL")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.claude_model = os.getenv("CLAUDE_MODEL")

        self.test_document = "Artificial Intelligence (AI) is the simulation of human intelligence processes by machines, especially computer systems."  # noqa: E501
        self.test_question = "What is AI?"

    def test_openai_provider(self):
        provider = LLMProviderFactory.create_provider(
            "openai", self.openai_api_key, self.openai_model
        )
        result = provider.grade_document(
            self.test_document, self.test_question
        )  # noqa: E501
        self.assertIsInstance(result, GradeDocuments)
        self.assertIn(result.binary_score.lower(), ["yes", "no"])
        self.assertIsNotNone(result.reasoning)

    def test_google_provider(self):
        provider = LLMProviderFactory.create_provider(
            "google", self.google_api_key, self.gemini_model
        )
        result = provider.grade_document(
            self.test_document, self.test_question
        )  # noqa: E501
        self.assertIsInstance(result, GradeDocuments)
        self.assertIn(result.binary_score.lower(), ["yes", "no"])
        self.assertIsNotNone(result.reasoning)

    def test_anthropic_provider(self):
        provider = LLMProviderFactory.create_provider(
            "anthropic", self.anthropic_api_key, self.claude_model
        )
        result = provider.grade_document(
            self.test_document, self.test_question
        )  # noqa: E501
        self.assertIsInstance(result, GradeDocuments)
        self.assertIn(result.binary_score.lower(), ["yes", "no"])
        self.assertIsNotNone(result.reasoning)

    def test_invalid_provider(self):
        with self.assertRaises(ValueError):
            LLMProviderFactory.create_provider(
                "invalid_provider", "dummy_key", "dummy_model"
            )


if __name__ == "__main__":
    unittest.main()
