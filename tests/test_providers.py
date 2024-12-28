import unittest
from .utils import get_provider_credentials
from langrade.providers import LLMProviderFactory, GradeDocuments


class TestProviders(unittest.TestCase):
    def setUp(self):
        self.test_document = "Artificial Intelligence (AI) is the simulation of human intelligence processes by machines, especially computer systems."
        self.test_question = "What is AI?"

    def _run_provider_test(self, provider_name: str):
        credentials, model = get_provider_credentials(provider_name)
        if not all([credentials, model]):
            self.skipTest(f"Required configuration for {provider_name} not available")

        provider = LLMProviderFactory.create_provider(provider_name, credentials, model)
        result = provider.grade_document(self.test_document, self.test_question)

        self.assertIsInstance(result, GradeDocuments)
        self.assertIn(result.binary_score.lower(), ["yes", "no"])
        self.assertIsNotNone(result.reasoning)

    def test_openai_provider(self):
        self._run_provider_test("openai")

    def test_anthropic_provider(self):
        self._run_provider_test("anthropic")

    def test_vertexai_provider(self):
        self._run_provider_test("vertexai")

    def test_invalid_provider(self):
        with self.assertRaises(ValueError):
            LLMProviderFactory.create_provider(
                "invalid_provider", "dummy_key", "dummy_model"
            )
