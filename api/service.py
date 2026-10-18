import time
from typing import Optional, Dict, Any
from graph.graph import graph
from ingestion.embedder import get_embedding_model
from ingestion.vectorstore import get_vectorstore_stats, add_documents_to_vectorstore
from ingestion.splitter import split_documents
from ingestion.loader import SUPPORTED_EXTENSIONS
from pathlib import Path
from utils.logger import logger


def ask_question(
    question: str,
    model: Optional[str] = None,
    top_k: int = 5,
    relevance_threshold: int = 7,
    enable_web_search: bool = True
) -> Dict[str, Any]:
    """Execute the full Corrective RAG pipeline and return rich telemetry."""
    state = {
        "question": question,
        "rewritten_question": "",
        "rewritten_queries": [],
        "documents": [],
        "filtered_documents": [],
        "graded_documents_info": [],
        "web_context": "",
        "web_sources": [],
        "generation": "",
        "generation_context": "",
        "rewrite_count": 0,
        "generation_attempts": 0,
        "grounded": False,
        "grounding_reason": "",
        "confidence": 1.0,
        "unsupported_claims": [],
        "active_route": "vector_direct",
        "execution_trace": [],
        "step_history": [],
        "llm_model": model,
        "top_k": top_k,
        "relevance_threshold": relevance_threshold,
        "enable_web_search": enable_web_search,
    }

    start = time.perf_counter()
    result = graph.invoke(state)
    end = time.perf_counter()

    # Determine unique sources
    local_sources = list({
        doc.metadata.get("filename", "Unknown Document")
        for doc in result.get("filtered_documents", [])
    })

    web_source_titles = [
        f"Web: {src.get('title', 'Web Result')}"
        for src in result.get("web_sources", [])
    ]

    all_sources = local_sources + web_source_titles
    if not all_sources:
        all_sources = ["No sources used"]

    return {
        "answer": result.get("generation", "No answer could be generated."),
        "grounded": result.get("grounded", False),
        "grounding_reason": result.get("grounding_reason", ""),
        "confidence": round(result.get("confidence", 1.0), 2),
        "rewrite_count": result.get("rewrite_count", 0),
        "generation_attempts": result.get("generation_attempts", 1),
        "latency": round(end - start, 2),
        "sources": all_sources,
        "step_history": result.get("step_history", []),
        "execution_trace": result.get("execution_trace", []),
        "graded_documents_info": result.get("graded_documents_info", []),
        "web_sources": result.get("web_sources", []),
        "rewritten_queries": result.get("rewritten_queries", []),
        "active_route": result.get("active_route", "vector_direct")
    }


def get_documents_stats() -> Dict[str, Any]:
    """Retrieve indexed document file list and chunk statistics from ChromaDB."""
    return get_vectorstore_stats()


def ingest_file(file_path: str) -> Dict[str, Any]:
    """Load, split, and index a single document file into ChromaDB."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = path.suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file format '{ext}'. Supported: {list(SUPPORTED_EXTENSIONS.keys())}")

    loader = SUPPORTED_EXTENSIONS[ext](str(path.resolve()))
    docs = loader.load()

    for doc in docs:
        doc.metadata["filename"] = path.name
        doc.metadata["extension"] = ext
        doc.metadata["source_path"] = str(path.resolve())

    chunks = split_documents(docs)
    embeddings = get_embedding_model()
    chunks_added = add_documents_to_vectorstore(chunks, embeddings)
    stats = get_vectorstore_stats(embeddings)

    return {
        "success": True,
        "message": f"Successfully indexed {path.name}",
        "filename": path.name,
        "chunks_created": chunks_added,
        "total_chunks": stats["total_chunks"]
    }