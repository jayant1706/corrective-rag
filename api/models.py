from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    grounded: bool
    rewrite_count: int
    latency: float
    sources: list[str]
    execution_trace: list[str]