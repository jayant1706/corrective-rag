import time
from prompts.grader import GRADE_PROMPT
from utils.llm import get_llm, invoke_structured
from utils.schema import GradeDocument
from utils.logger import logger
from config import RELEVANCE_THRESHOLD


def grade_documents(state):
    start_time = time.perf_counter()
    logger.info("GRADE | Grading retrieved documents")

    question = state.get("question", "")
    documents = state.get("documents", [])
    threshold = state.get("relevance_threshold") or RELEVANCE_THRESHOLD
    model_name = state.get("llm_model")

    llm_instance = get_llm(model=model_name, temperature=0.0)

    filtered_docs = []
    graded_info = []

    for i, doc in enumerate(documents, start=1):
        prompt = GRADE_PROMPT.invoke(
            {
                "question": question,
                "document": doc.page_content,
            }
        )
        try:
            result = invoke_structured(llm_instance, prompt, GradeDocument)
            score = result.score
            # Document is relevant only if score is at or above threshold AND is_relevant is true
            is_rel = (score >= threshold) and result.is_relevant
            reason = result.reason or ("Document is relevant." if is_rel else "Document lacks direct relevance.")
        except Exception as e:
            logger.warning(f"GRADE | Grading error on chunk {i}: {e}")
            score = 5
            reason = "Automated fallback evaluation"
            is_rel = score >= threshold

        graded_info.append({
            "index": i,
            "filename": doc.metadata.get("filename", "Unknown Document"),
            "page": doc.metadata.get("page", "N/A"),
            "score": score,
            "is_relevant": is_rel,
            "reason": reason,
            "snippet": doc.page_content[:250].strip() + ("..." if len(doc.page_content) > 250 else ""),
            "full_content": doc.page_content
        })

        if is_rel:
            filtered_docs.append(doc)

    duration = round(time.perf_counter() - start_time, 3)
    logger.info(f"GRADE | Kept {len(filtered_docs)}/{len(documents)} relevant documents in {duration}s")

    trace = list(state.get("execution_trace", []))
    step_history = list(state.get("step_history", []))

    trace.append({
        "step": "Grade",
        "status": "success",
        "duration_sec": duration,
        "message": f"Evaluated {len(documents)} chunks: {len(filtered_docs)} relevant (threshold >={threshold}/10)",
        "relevant_count": len(filtered_docs),
        "total_count": len(documents),
        "threshold": threshold
    })
    step_history.append(f"Grade ({len(filtered_docs)}/{len(documents)} kept)")

    return {
        "filtered_documents": filtered_docs,
        "graded_documents_info": graded_info,
        "execution_trace": trace,
        "step_history": step_history,
    }