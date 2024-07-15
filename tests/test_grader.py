import unittest
from unittest.mock import patch, MagicMock
from langrade import document_grader
from conftest import get_api_key


class TestDocumentGrader(unittest.TestCase):
    def setUp(self):
        self.api_key = get_api_key()
        self.grader = document_grader(self.api_key)

    @patch("langrade.grader.ChatOpenAI")
    def test_grade_document(self, mock_chat_openai):
        mock_llm = MagicMock()
        mock_chat_openai.return_value = mock_llm
        mock_result = MagicMock(
            binary_score="yes",
            reasoning="The document provides a definition of AI as a field of computer science creating intelligent machines, which directly answers the user question.",  # noqa: E501
        )
        mock_llm.with_structured_output.return_value.invoke.return_value = (
            mock_result  # noqa: E501
        )

        document = "AI is a field of computer science that focuses on creating intelligent machines."  # noqa: E501
        question = "What is AI?"

        result = self.grader.grade_document(document, question)
        print("result", result)
        self.assertEqual(result.binary_score, "yes")
        self.assertIsNotNone(result.reasoning)
