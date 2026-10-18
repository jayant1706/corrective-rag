from typing import TypedDict, List, Dict, Any, Optional
from langchain_core.documents import Document


class GraphState(TypedDict, total=False):
    # User input
    question: str
    rewritten_question: str
    rewritten_queries: List[Dict[str, str]]

    # Retrieval
    documents: List[Document]
    filtered_documents: List[Document]
    graded_documents_info: List[Dict[str, Any]]
    web_context: str
    web_sources: List[Dict[str, str]]

    # Generation
    generation: str
    generation_context: str

    # Verification & Hallucination
    grounded: bool
    grounding_reason: str
    confidence: float
    unsupported_claims: List[str]

    # Retry counters & Route
    rewrite_count: int
    generation_attempts: int
    active_route: str

    # Configuration overrides
    llm_model: Optional[str]
    top_k: Optional[int]
    relevance_threshold: Optional[int]
    enable_web_search: Optional[bool]

    # Execution trace & telemetry
    execution_trace: List[Dict[str, Any]]
    step_history: List[str]