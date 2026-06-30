from pydantic import BaseModel, Field


class GradeDocument(BaseModel):
    score: int = Field(
        description="Relevance score from 1 to 10."
    )


class HallucinationCheck(BaseModel):
    grounded: bool = Field(
        description="True if the answer is completely supported by the provided context."
    )