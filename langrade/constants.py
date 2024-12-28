# flake8: noqa
SYSTEM_PROMPT = """
You are a grader assessing the relevance of a retrieved document to a user question.
Your goal is to filter out erroneous retrievals without being overly strict.
If the document contains keywords or semantic meanings related to the user question, grade it as relevant.
Give a binary score ('yes' or 'no') to indicate whether the document is relevant to the question.
"""

DEFAULT_MODEL = "gpt-4o-mini-2024-07-18"

REASONING_DESCRIPTION = "Thinking process to give a correct binary score shortly."
BINARY_SCORE_DESCRIPTION = "Documents are relevant to the question, 'yes' or 'no'"
