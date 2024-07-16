from .providers import LLMProviderFactory, GradeDocuments
from .constants import DEFAULT_MODEL


class DocumentGrader:
    def __init__(
        self, provider: str, api_key: str, model: str = DEFAULT_MODEL
    ):  # noqa: E501
        self.provider = LLMProviderFactory.create_provider(
            provider, api_key, model
        )  # noqa: E501

    def grade_document(self, document: str, question: str) -> GradeDocuments:
        return self.provider.grade_document(document, question)


def document_grader(
    provider: str, api_key: str, model: str = DEFAULT_MODEL
) -> DocumentGrader:
    return DocumentGrader(provider, api_key, model)
