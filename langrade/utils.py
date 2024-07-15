from langrade import DocumentGraderFactory

api_key = "your_openai_api_key_here"
grader = DocumentGraderFactory.create(api_key, reasoning=True)

document = "This is a test document about AI."
question = "What is AI?"
result = grader.grade_document(document, question)
print(f"Relevance: {result.binary_score}")
print(f"Reasoning: {result.reasoning}")
