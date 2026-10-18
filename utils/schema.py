from typing import List, Union
from pydantic import BaseModel, Field, field_validator


class GradeDocument(BaseModel):
    score: int = Field(
        default=5,
        description="Relevance score integer from 1 to 10."
    )
    is_relevant: bool = Field(
        default=False,
        description="True if the document contains relevant information to answer the question, False otherwise."
    )
    reason: str = Field(
        default="",
        description="Brief 1-sentence justification for the assigned relevance score."
    )

    @field_validator("score", mode="before")
    @classmethod
    def parse_score(cls, v):
        if v is None:
            return 5
        try:
            val = float(v)
            if 0.0 <= val <= 1.0 and val > 0:
                val = val * 10.0
            return max(1, min(10, int(round(val))))
        except Exception:
            return 5

    @field_validator("is_relevant", mode="before")
    @classmethod
    def parse_is_relevant(cls, v, values):
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            return v.lower().strip() in ("true", "yes", "1", "relevant")
        return bool(v)


class HallucinationCheck(BaseModel):
    grounded: bool = Field(
        default=True,
        description="True if the answer is completely supported by the provided context; False if it introduces hallucinated facts."
    )
    confidence: float = Field(
        default=1.0,
        description="Confidence score between 0.0 and 1.0 that the assessment is accurate."
    )
    explanation: str = Field(
        default="",
        description="Concise explanation citing supported or unsupported claims."
    )
    unsupported_claims: List[str] = Field(
        default_factory=list,
        description="List of claims in the generated answer not found in the context, if any."
    )

    @field_validator("grounded", mode="before")
    @classmethod
    def parse_grounded(cls, v):
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            return v.lower().strip() in ("true", "yes", "grounded", "1")
        return bool(v)

    @field_validator("confidence", mode="before")
    @classmethod
    def parse_confidence(cls, v):
        if v is None:
            return 1.0
        try:
            val = float(v)
            if val > 1.0 and val <= 100.0:
                val = val / 100.0
            return max(0.0, min(1.0, val))
        except Exception:
            return 1.0


class QueryRewrite(BaseModel):
    rewritten_query: str = Field(
        description="The optimized, specific search query."
    )
    reason: str = Field(
        default="",
        description="Brief explanation of why this rewritten query improves retrieval."
    )