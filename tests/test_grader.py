import unittest
from unittest.mock import patch, MagicMock
from langrade import document_grader
from .conftest import get_api_key


class TestDocumentGrader(unittest.TestCase):
    def setUp(self):
        self.api_key = get_api_key()
        self.grader = document_grader(self.api_key, reasoning=True)

    @patch("langrade.grader.ChatOpenAI")
    def test_grade_document_with_reasoning(self, mock_chat_openai):
        mock_llm = MagicMock()
        mock_chat_openai.return_value = mock_llm
        mock_llm.with_structured_output.return_value.invoke.return_value = MagicMock(  # noqa: E501
            binary_score="yes",
            reasoning="The document is relevant because it discusses AI concepts.",  # noqa: E501
        )

        document = "AI is a field of computer science that focuses on creating intelligent machines."  # noqa: E501
        question = "What is AI?"

        result = self.grader.grade_document(document, question)

        self.assertEqual(result.binary_score, "yes")
        self.assertIn("relevant", result.reasoning.lower())

    @patch("langrade.grader.ChatOpenAI")
    def test_grade_document_without_reasoning(self, mock_chat_openai):
        grader = document_grader(self.api_key, reasoning=False)
        mock_llm = MagicMock()
        mock_chat_openai.return_value = mock_llm
        mock_llm.with_structured_output.return_value.invoke.return_value = MagicMock(
            binary_score="no",
        )

        document = "This document is about biology and ecosystems."
        question = "What is AI?"

        result = grader.grade_document(document, question)

        self.assertEqual(result.binary_score, "no")
        self.assertFalse(hasattr(result, "reasoning"))


if __name__ == "__main__":
    unittest.main()
