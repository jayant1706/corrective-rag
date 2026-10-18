import time
from prompts.rewrite import REWRITE_PROMPT
from utils.llm import get_llm, invoke_structured
from utils.schema import QueryRewrite
from utils.logger import logger


def rewrite_query(state):
    start_time = time.perf_counter()
    logger.info("REWRITE | Rewriting query for improved retrieval")

    question = state.get("question", "")
    current_count = state.get("rewrite_count", 0)
    model_name = state.get("llm_model")

    llm_instance = get_llm(model=model_name, temperature=0.2)

    prompt = REWRITE_PROMPT.invoke({"question": question})

    try:
        result = invoke_structured(llm_instance, prompt, QueryRewrite)
        rewritten = result.rewritten_query.strip() if result.rewritten_query else question
        reason = result.reason or "Query expanded for better semantic matching."
    except Exception as e:
        logger.warning(f"REWRITE | Error during query rewrite: {e}")
        raw = llm_instance.invoke(prompt)
        rewritten = raw.content.strip() if hasattr(raw, "content") else question
        reason = "Direct rewrite fallback"

    duration = round(time.perf_counter() - start_time, 3)
    logger.info(f"REWRITE | Original: '{question}' -> Rewritten: '{rewritten}' in {duration}s")

    rewritten_queries = list(state.get("rewritten_queries", []))
    rewritten_queries.append({
        "iteration": current_count + 1,
        "original": question,
        "rewritten": rewritten,
        "reason": reason
    })

    trace = list(state.get("execution_trace", []))
    step_history = list(state.get("step_history", []))

    trace.append({
        "step": "Rewrite",
        "status": "success",
        "duration_sec": duration,
        "message": f"Rewrote query (attempt {current_count + 1}): '{rewritten}'",
        "rewritten": rewritten,
        "reason": reason
    })
    step_history.append(f"Rewrite #{current_count + 1}")

    return {
        "rewritten_question": rewritten,
        "rewritten_queries": rewritten_queries,
        "rewrite_count": current_count + 1,
        "execution_trace": trace,
        "step_history": step_history,
    }