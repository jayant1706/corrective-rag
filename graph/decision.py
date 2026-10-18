from config import (
    MAX_REWRITES,
    MIN_RELEVANT_DOCS,
    MAX_GENERATION_ATTEMPTS,
    ENABLE_WEB_SEARCH,
    TAVILY_API_KEY,
)
from utils.logger import logger


def decide_after_grade(state):
    """Route after document grading: generate, rewrite, or web search."""
    relevant_count = len(state.get("filtered_documents", []))
    rewrite_count = state.get("rewrite_count", 0)
    max_rewrites = state.get("max_rewrites", MAX_REWRITES)
    min_docs = state.get("min_relevant_docs", MIN_RELEVANT_DOCS)
    enable_web = state.get("enable_web_search", ENABLE_WEB_SEARCH) and bool(TAVILY_API_KEY)

    logger.info(
        f"DECISION | Relevant docs: {relevant_count}/{min_docs}, Rewrites: {rewrite_count}/{max_rewrites}"
    )

    # If we have enough relevant documents, proceed directly to generation
    if relevant_count >= min_docs:
        return "generate"

    # If retrieval was insufficient and we haven't reached max rewrites, try rewriting
    if rewrite_count < max_rewrites:
        return "rewrite"

    # If max rewrites reached and still insufficient, fall back to web search if enabled
    if enable_web:
        return "web"

    # Otherwise generate best-effort from available information
    return "generate"


def decide_after_hallucination(state):
    """Route after hallucination evaluation: finish, regenerate, or web search."""
    grounded = state.get("grounded", True)
    attempts = state.get("generation_attempts", 1)
    max_attempts = state.get("max_generation_attempts", MAX_GENERATION_ATTEMPTS)
    web_context = state.get("web_context", "")
    enable_web = state.get("enable_web_search", ENABLE_WEB_SEARCH) and bool(TAVILY_API_KEY)

    logger.info(
        f"DECISION | Grounded: {grounded}, Attempts: {attempts}/{max_attempts}, Has Web Context: {bool(web_context)}"
    )

    # If grounded, terminate successfully
    if grounded:
        return "end"

    # If reached max generation attempts, stop and return the output
    if attempts >= max_attempts:
        return "end"

    # If ungrounded and web search hasn't been queried yet, enrich context with live web search
    if not web_context and enable_web:
        return "web"

    # Self-correct by regenerating using grounding critique feedback
    return "regenerate"


# Backwards compatibility alias
decide_next = decide_after_grade