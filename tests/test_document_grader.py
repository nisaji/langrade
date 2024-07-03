import unittest
from langrade import document_grader


class TestDocumentGrader(unittest.TestCase):
    def test_grade_document_with_reasoning(self):
        grader = document_grader(reasoning=True)
        document = "This is a test document about AI."
        question = "What is AI?"
        result = grader.grade_document(document, question)
        self.assertIn(result.binary_score, ["yes", "no"])

    def test_grade_document_without_reasoning(self):
        grader = document_grader(reasoning=False)
        document = "This is a test document about AI."
        question = "What is AI?"
        result = grader.grade_document(document, question)
        self.assertIn(result.binary_score, ["yes", "no"])


if __name__ == "__main__":
    unittest.main()
