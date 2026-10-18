import time
from typing import Optional
from ingestion.embedder import get_embedding_model
from ingestion.vectorstore import load_vectorstore
from config import TOP_K
from utils.logger import logger

_db_instance = None
_retriever_instance = None


def get_retriever(k: int = TOP_K):
    global _db_instance, _retriever_instance
    if _retriever_instance is None:
        try:
            embeddings = get_embedding_model()
            _db_instance = load_vectorstore(embeddings)
            _retriever_instance = _db_instance.as_retriever(search_kwargs={"k": k})
        except Exception as e:
            logger.error(f"Error initializing vectorstore retriever: {e}")
            return None
    return _retriever_instance


def retrieve(state):
    start_time = time.perf_counter()
    logger.info("RETRIEVE | Starting document retrieval")

    question = state.get("rewritten_question") or state.get("question", "")
    k = state.get("top_k") or TOP_K

    retriever = get_retriever(k=k)
    documents = []

    if retriever is not None:
        try:
            documents = retriever.invoke(question)
        except Exception as e:
            logger.error(f"RETRIEVE | Error querying vectorstore: {e}")
            documents = []
    else:
        logger.warning("RETRIEVE | Vectorstore retriever is unavailable")

    duration = round(time.perf_counter() - start_time, 3)
    logger.info(f"RETRIEVE | Retrieved {len(documents)} documents in {duration}s")

    trace = list(state.get("execution_trace", []))
    step_history = list(state.get("step_history", []))

    trace.append({
        "step": "Retrieve",
        "status": "success",
        "duration_sec": duration,
        "message": f"Retrieved {len(documents)} chunks from ChromaDB for query: '{question}'",
        "query": question,
        "count": len(documents)
    })
    step_history.append(f"Retrieve ({len(documents)} docs)")

    return {
        "documents": documents,
        "execution_trace": trace,
        "step_history": step_history,
    }