from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str
    model: Optional[str] = Field(default=None, description="Groq model name to use")
    top_k: Optional[int] = Field(default=5, ge=1, le=20, description="Number of documents to retrieve")
    relevance_threshold: Optional[int] = Field(default=7, ge=1, le=10, description="Relevance cutoff score (1-10)")
    enable_web_search: Optional[bool] = Field(default=True, description="Enable Tavily fallback if retrieval is weak")


class ChatResponse(BaseModel):
    answer: str
    grounded: bool
    grounding_reason: str
    confidence: float
    rewrite_count: int
    generation_attempts: int
    latency: float
    sources: List[str]
    step_history: List[str]
    execution_trace: List[Dict[str, Any]]
    graded_documents_info: List[Dict[str, Any]]
    web_sources: List[Dict[str, Any]]
    rewritten_queries: List[Dict[str, Any]]
    active_route: str


class DocumentItem(BaseModel):
    filename: str
    chunk_count: int
    extension: str
    file_size_bytes: Optional[int] = None


class DocumentStatsResponse(BaseModel):
    total_chunks: int
    documents: List[DocumentItem]
    collection_name: str


class UploadResponse(BaseModel):
    success: bool
    message: str
    filename: str
    chunks_created: int
    total_chunks: int