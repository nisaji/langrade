from langchain_core.pydantic_v1 import BaseModel, Field
from ..constants import GRADE_REASONING_DESCRIPTION, BINARY_SCORE_DESCRIPTION


class GradeDocumentsWithReasoning(BaseModel):
    """Binary score and reasoning for relevance check on retrieved documents."""  # noqa: E501

    reasoning: str = Field(description=GRADE_REASONING_DESCRIPTION)
    binary_score: str = Field(description=BINARY_SCORE_DESCRIPTION)


class GradeDocumentsWithoutReasoning(BaseModel):
    """Binary score for relevance check on retrieved documents."""

    binary_score: str = Field(description=BINARY_SCORE_DESCRIPTION)
