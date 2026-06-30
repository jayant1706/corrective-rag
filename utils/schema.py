from pydantic import BaseModel, Field


class GradeDocument(BaseModel):
    score: int = Field(
        description="Relevance score from 1 to 10."
    )