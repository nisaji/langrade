# Langrade

Langrade is a Python library for grading and retrieving documents based on their relevance to a given question.

## Installation

You can install Langrade using pip:

```
pip install langrade
```

## Usage

Here's a quick example of how to use Langrade:

```python
from langrade import document_grader

api_key = "user_api_key_here"
grader = document_grader(api_key, reasoning=True)

document = "This is a test document about AI."
question = "What is AI?"
result = grader.grade_document(document, question)
print(f"Relevance: {result.binary_score}")
print(f"Reasoning: {result.reasoning}")
```

## Running Tests

To run all tests:

```
poetry run test
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
