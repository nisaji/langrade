# Basic Usage

## Initializing the Grader

```python
from langrade import document_grader

provider = "openai"  # or "anthropic" or "google"
api_key = "your_api_key_here"
model = "gpt-3.5-turbo-0125"  # or appropriate model for the chosen provider

grader = document_grader(provider, api_key, model)
```

## Create Retriever

```python
from langrade import create_retriever

urls = [
    "https://example.com/article1",
    "https://example.com/article2",
]
retriever = create_retriever(urls, api_key)
```

## Retrieving and Grading Documents

```python
question = "What is AI?"
docs = retriever.get_relevant_documents(question)
doc_txt = docs[0].page_content

result = grader.grade_document(doc_txt, question)
print(f"Relevance: {result.binary_score}")
print(f"Reasoning: {result.reasoning}")
```

For more advanced usage, see the Advanced Usage guide.
