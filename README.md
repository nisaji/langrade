# langrade

langrade is a Python library for grading and retrieving documents based on their relevance to a given question. It supports multiple LLM providers including OpenAI, Anthropic (Claude), and Google (Gemini).

## Installation

You can install Langrade using pip:

```
pip install langrade
```

## Usage

Here's a quick example of how to use Langrade:

```python
from langrade import document_grader, create_retriever

# Initialize the grader
api_key = "your_openai_api_key_here"
grader = document_grader(api_key)

# Prepare the retriever
urls = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]
retriever = create_retriever(urls, api_key)

# Retrieve and grade a document
question = "What is AI?"
docs = retriever.get_relevant_documents(question)
doc_txt = docs[0].page_content

result = grader.grade_document(doc_txt, question)
print(f"Relevance: {result.binary_score}")
print(f"Reasoning: {result.reasoning}")
```

## Features

- Document retrieval from web URLs
- Document grading based on relevance to a question
- Support for multiple LLM providers (OpenAI, Anthropic, Google, Groq)

## Requirements

Python 3.9+

OpenAI API key

## Running Tests

To run all tests:

```

poetry run test

```

## Security

- Always use environment variables for sensitive information like API keys.
- Never commit `.env` files to version control.
- Regularly update dependencies to their latest secure versions.
- Use HTTPS for all external communications.
- Sanitize all user inputs before processing.

For local development:

1. Copy `.env.example` to `.env`
2. Fill in your actual API keys and other sensitive information in `.env`
3. Ensure `.env` is in your `.gitignore` file

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

```

```
