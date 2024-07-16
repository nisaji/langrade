# Welcome to Langrade

Langrade is a Python library for grading and retrieving documents based on their relevance to a given question. It supports multiple LLM providers including OpenAI, Anthropic (Claude), and Google (Gemini).

## Quick Start

```python
from langrade import document_grader, create_retriever

provider = "openai"
api_key = "your_api_key_here"
model = "gpt-3.5-turbo-0125"

grader = document_grader(provider, api_key, model)

urls = [
    "https://example.com/article1",
    "https://example.com/article2",
]
retriever = create_retriever(urls, api_key)

question = "What is AI?"
docs = retriever.get_relevant_documents(question)
doc_txt = docs[0].page_content

result = grader.grade_document(doc_txt, question)
print(f"Relevance: {result.binary_score}")
print(f"Reasoning: {result.reasoning}")
```

## Table of Contents

- Installation
- Usage
- API Reference
- Configuration
- Providers
- Advanced Usage
- Troubleshooting
- Contributing
- Changelog
- FAQ
