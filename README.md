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
from langrade import document_grader, create_retriever

# Initialize the grader
api_key = "your_openai_api_key_here"
grader = document_grader(api_key, reasoning=True)

# Prepare the retriever
urls = [
    "https://example.com/article1",
    "https://example.com/article2",
    "https://example.com/article3",
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

Document retrieval from web URLs

Document grading based on relevance to a question

Optional reasoning for grading decisions

## Requirements

Python 3.8+

OpenAI API key

## Running Tests

To run all tests:

```

poetry run test

```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

```

```
