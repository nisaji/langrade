# langrade

langrade is a Python library for grading and retrieving documents based on their relevance to a given question. It supports multiple LLM providers including OpenAI, Anthropic (Claude), and VertexAI (Gemini).

📚 [Documentation](https://nisaji.github.io/langrade/)

## Installation

You can install Langrade using pip

```bash
pip install langrade
```

## Usage

Here's a quick example of how to use Langrade with different providers

```python
from langrade import document_grader, create_retriever

# Initialize the grader with OpenAI
provider = "openai"
api_key = "your_openai_api_key_here"
model = "gpt-4o-mini-2024-07-18"  # optional
grader = document_grader(provider, api_key, model)

# Or with Anthropic (Claude)
provider = "anthropic"
api_key = "your_anthropic_api_key_here"
model = "claude-3-5-haiku-20241022"  # optional
grader = document_grader(provider, api_key, model)

# Or with Google (Gemini)
provider = "vertexai"
credentials = {
    "project_id": "your_project_id",
    "location": "your_location",  # optional, defaults to asia-northeast1
    # ... other service account credentials
}
model = "gemini-1.5-flash"  # optional
grader = document_grader(provider, credentials, model)

# Prepare the retriever (uses OpenAI embeddings)
urls = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]
retriever = create_retriever(urls, openai_api_key)

# Retrieve and grade a document
question = "What is AI?"
docs = retriever.get_relevant_documents(question)
doc_txt = docs[0].page_content

result = grader.grade_document(doc_txt, question)
print(f"Relevance: {result.binary_score}")  # 'yes' or 'no'
print(f"Reasoning: {result.reasoning}")
```

## Features

- Document grading based on relevance to a question

- Support for multiple LLM providers

  - OpenAI (GPT models)
  - Anthropic (Claude models)
  - Google (Gemini models)

- Document retrieval from web URLs

- Flexible configuration options for each provider

## Requirements

- Python 3.9+
- API key for chosen provider

  - OpenAI API key for OpenAI
  - Anthropic API key for Claude
  - Google Cloud service account credentials for Gemini

## Environment Setup

- For local development:

  1. Copy .env.example to .env
  2. Fill in your API keys and configuration

```
# OpenAI Configuration
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-3.5-turbo-0125

# Google Cloud Platform Configuration
GCP_PROJECT_ID=your-project-id
GCP_LOCATION=asia-northeast1
GOOGLE_APPLICATION_CREDENTIALS=path-to-credentials.json
GEMINI_MODEL=gemini-2.0-flash-exp

# Anthropic (Claude) Configuration
ANTHROPIC_API_KEY=your-api-key-here
CLAUDE_MODEL=claude-3-5-haiku-20241022

# Default Engine Configuration
DEFAULT_ENGINE_TYPE=openai
```

## Running Tests

To run all tests

```bash
poetry run test
```
