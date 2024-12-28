import unittest
from .utils import get_provider_credentials, load_env_config
from langrade import document_grader


class TestDocumentGrader(unittest.TestCase):
    def setUp(self):
        config = load_env_config()
        provider = config["provider"]
        credentials, model = get_provider_credentials(provider)

        if not all([provider, credentials, model]):
            self.skipTest(f"Required configuration for {provider} not available")

        self.grader = document_grader(provider, credentials, model)

    def test_grade_document(self):
        document = "AI is a field of computer science that focuses on creating intelligent machines."
        question = "What is AI?"

        result = self.grader.grade_document(document, question)
        self.assertIsNotNone(result.binary_score)
        self.assertIsNotNone(result.reasoning)
