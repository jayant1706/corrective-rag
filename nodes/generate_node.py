import time
from prompts.answer import ANSWER_PROMPT, REGENERATE_ANSWER_PROMPT
from utils.llm import get_llm
from utils.logger import logger


def generate_answer(state):
    start_time = time.perf_counter()
    attempts = state.get("generation_attempts", 0) + 1
    logger.info(f"GENERATE | Generating answer (Attempt #{attempts})")

    docs = state.get("filtered_documents", [])
    question = state.get("question", "")
    web_context = state.get("web_context", "")
    model_name = state.get("llm_model")

    context = ""

    if docs:
        context += "LOCAL DOCUMENT KNOWLEDGE:\n"
        for i, doc in enumerate(docs, start=1):
            filename = doc.metadata.get("filename", "Unknown Document")
            page = doc.metadata.get("page", "N/A")
            context += f"""
[Doc {i}: {filename} (Page {page})]
{doc.page_content}
------------------------
"""

    if web_context:
        context += f"""
EXTERNAL LIVE WEB SEARCH CONTEXT:
{web_context}
------------------------
"""

    if not context.strip():
        context = "No relevant context found in documents or web search."

    llm_instance = get_llm(model=model_name, temperature=0.1)

    # If this is a regeneration attempt following a hallucination audit, incorporate critique
    is_regeneration = (attempts > 1) and (not state.get("grounded", True))
    if is_regeneration:
        critique = state.get("grounding_reason", "Answer contained unsupported claims.")
        if state.get("unsupported_claims"):
            critique += f"\nSpecifically unsupported claims: {', '.join(state['unsupported_claims'])}"
        prompt = REGENERATE_ANSWER_PROMPT.invoke({
            "context": context,
            "question": question,
            "critique": critique
        })
    else:
        prompt = ANSWER_PROMPT.invoke({
            "context": context,
            "question": question,
        })

    try:
        response = llm_instance.invoke(prompt)
        answer = response.content.strip()
    except Exception as e:
        logger.error(f"GENERATE | Error during generation: {e}")
        answer = "An error occurred while generating the response. Please check your connection or model parameters."

    duration = round(time.perf_counter() - start_time, 3)
    logger.info(f"GENERATE | Answer generated successfully in {duration}s")

    trace = list(state.get("execution_trace", []))
    step_history = list(state.get("step_history", []))

    step_label = f"Regenerate (Attempt #{attempts})" if is_regeneration else "Generate Answer"
    trace.append({
        "step": step_label,
        "status": "success",
        "duration_sec": duration,
        "message": f"Generated answer using {len(docs)} local chunks and {'web search' if web_context else 'no web'}",
        "attempt": attempts,
        "is_regeneration": is_regeneration
    })
    step_history.append(f"{step_label}")

    return {
        "generation": answer,
        "generation_context": context,
        "generation_attempts": attempts,
        "execution_trace": trace,
        "step_history": step_history,
    }