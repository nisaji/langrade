# Frequently Asked Questions

## General

### Q: What is Langrade?

A: Langrade is a Python library for grading and retrieving documents based on their relevance to a given question. It supports multiple LLM providers including OpenAI, Anthropic (Claude), and Google (Gemini).

### Q: Which Python versions are supported?

A: Langrade supports Python 3.9 and above.

## Usage

### Q: How do I choose between different LLM providers?

A: You can specify the provider when creating a `DocumentGrader`:

```python
from langrade import document_grader

# For OpenAI
grader_openai = document_grader("openai", "your_openai_api_key", "gpt-3.5-turbo-0125")

# For Anthropic
grader_anthropic = document_grader("anthropic", "your_anthropic_api_key", "claude-3-opus-20240229")

# For Google
grader_google = document_grader("google", "your_google_api_key", "gemini-1.0-pro")
```

### Q: Can I use my own custom models?

A: Currently, Langrade supports the models provided by OpenAI, Anthropic, and Google. Custom model support may be added in future versions.

## Troubleshooting

### Q: I'm getting an "API key not found" error. What should I do?

A: Ensure that you've set up your .env file correctly with the appropriate API keys. Also, make sure you're loading the environment variables in your code:

```python
from dotenv import load_dotenv
load_dotenv()
```

### Q: How can I report a bug or request a feature?

A: Please open an issue on our GitHub repository. Provide as much detail as possible, including your Python version and any error messages you're seeing.

For more detailed information, please refer to our [documentation](https://langrade.readthedocs.io/).
