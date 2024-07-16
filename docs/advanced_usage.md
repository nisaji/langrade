# Advanced Usage

## Custom Prompts

You can customize the system prompt used by the grader:

```python
from langrade.constants import SYSTEM_PROMPT

# Modify the SYSTEM_PROMPT constant
SYSTEM_PROMPT = """
Your custom prompt here.
"""

# Then create your grader as usual
grader = document_grader(provider, api_key, model)
```

## Batch Processing

For grading multiple documents:

```python
documents = ["doc1 content", "doc2 content", "doc3 content"]
question = "What is AI?"

results = []
for doc in documents:
    result = grader.grade_document(doc, question)
    results.append(result)

for i, result in enumerate(results):
    print(f"Document {i+1}:")
    print(f"Relevance: {result.binary_score}")
    print(f"Reasoning: {result.reasoning}")
    print()
```

## Custom Retriever

You can create a custom retriever by subclassing BaseRetriever:

```python
from langchain.schema import BaseRetriever, Document

class CustomRetriever(BaseRetriever):
    def get_relevant_documents(self, query: str) -> List[Document]:
        # Your custom retrieval logic here
        pass

    async def aget_relevant_documents(self, query: str) -> List[Document]:
        # Your custom async retrieval logic here
        pass

# Use your custom retriever
custom_retriever = CustomRetriever()
docs = custom_retriever.get_relevant_documents("What is AI?")
```

For more advanced usage scenarios, refer to the source code and consider extending the base classes provided by Langrade.
