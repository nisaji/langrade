# flake8: noqa
GRADE_REASONING_DESCRIPTION = (
    "Thinking process to give a correct binary score shortly."  # noqa: E501
)
BINARY_SCORE_DESCRIPTION = (
    "Documents are relevant to the question, 'yes' or 'no'"  # noqa: E501
)

SYSTEM_PROMPT = """
You are a grader assessing the relevance of a retrieved document to a user question.
    Your goal is to filter out erroneous retrievals without being overly strict.
    If the document contains keywords or semantic meanings related to the user question, grade it as relevant.
    Give a binary score ('yes' or 'no') to indicate whether the document is relevant to the question.
"""
