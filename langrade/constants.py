# flake8: noqa
SYSTEM_PROMPT = """
You are a grader assessing the relevance of a retrieved document to a user question.
Your goal is to filter out erroneous retrievals without being overly strict.
If the document contains keywords or semantic meanings related to the user question, grade it as relevant.
Give a binary score ('yes' or 'no') to indicate whether the document is relevant to the question.
"""

DEFAULT_MODEL = "gpt-3.5-turbo-0125"

REASONING_DESCRIPTION = "Thinking process to give a correct binary score shortly."
BINARY_SCORE_DESCRIPTION = "Documents are relevant to the question, 'yes' or 'no'"

RELEVANCE_PROMPT = """
Assess the relevance of the retrieved document to the user question.
Your goal is to filter out erroneous retrievals without being overly strict.
If the document contains keywords or semantic meanings related to the user question, grade it as relevant.

Retrieved document:
{document}

User question:
{question}

Binary score (yes/no):
Reasoning:
"""

READABILITY_PROMPT = """
Assess the readability of the given document.
Consider factors such as sentence structure, vocabulary, and overall clarity.
If the document is easy to understand for a general audience, grade it as readable.

Document to assess:
{document}

Binary score (yes/no):
Reasoning:
"""

COHERENCE_PROMPT = """
Assess the coherence of the given document.
Consider factors such as logical flow, organization of ideas, and overall structure.
If the document presents ideas in a clear and logical manner, grade it as coherent.

Document to assess:
{document}

Binary score (yes/no):
Reasoning:
"""
