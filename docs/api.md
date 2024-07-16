# API Reference

## document_grader

```python
def document_grader(provider: str, api_key: str, model: str = DEFAULT_MODEL) -> DocumentGrader:
    """
    Create a DocumentGrader instance.

    Args:
        provider (str): The LLM provider ("openai", "anthropic", or "google").
        api_key (str): The API key for the chosen provider.
        model (str, optional): The model to use. Defaults to DEFAULT_MODEL.

    Returns:
        DocumentGrader: An instance of the DocumentGrader class.
    """
```

## DocumentGrader

```python
class DocumentGrader:
    def __init__(self, provider: str, api_key: str, model: str = DEFAULT_MODEL):
        """
        Initialize a DocumentGrader instance.

        Args:
            provider (str): The LLM provider.
            api_key (str): The API key for the chosen provider.
            model (str, optional): The model to use. Defaults to DEFAULT_MODEL.
        """

    def grade_document(self, document: str, question: str) -> GradeDocuments:
        """
        Grade a document based on its relevance to a question.

        Args:
            document (str): The document text to grade.
            question (str): The question to grade the document against.

        Returns:
            GradeDocuments: An object containing the grading result.
        """
```

## create_retriever

```python
def create_retriever(urls: list[str], api_key: str) -> BaseRetriever:
    """
    Create a retriever for fetching relevant documents.

    Args:
        urls (list[str]): A list of URLs to fetch documents from.
        api_key (str): The API key for the embedding model.

    Returns:
        BaseRetriever: A retriever instance.
    """
```

For more details on the returned objects and their properties, see the source code documentation.
