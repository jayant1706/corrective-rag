from typing import TypedDict, List
from langchain_core.documents import Document


class GraphState(TypedDict):
    # User input
    question: str
    rewritten_question: str

    # Retrieval
    documents: List[Document]
    filtered_documents: List[Document]
    web_context: str

    # Generation
    generation: str
    generation_context: str

    # Verification
    grounded: bool
    grounding_reason: str

    # Retry counters
    rewrite_count: int
    generation_attempts: int

    # Execution trace
    execution_trace: list