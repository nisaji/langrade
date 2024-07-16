# Configuration

# Provider-Specific Configuration

## OpenAI

```python
from langrade import document_grader

grader = document_grader("openai", "your_openai_api_key", "gpt-3.5-turbo-0125")
```

## Anthropic

```python
from langrade import document_grader

grader = document_grader("anthropic", "your_anthropic_api_key", "claude-3-opus-20240229")
```

## Google

```python
from langrade import document_grader

grader = document_grader("google", "your_google_api_key", "gemini-1.5-pro-latest")
```
