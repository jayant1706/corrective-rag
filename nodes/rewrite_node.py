from utils.llm import llm
from prompts.rewrite import REWRITE_PROMPT
from utils.logger import logger

MAX_REWRITES = 2


def rewrite_query(state):

    logger.info(
        "Rewritting query"
    )

    question = state["question"]

    prompt = REWRITE_PROMPT.invoke(
        {
            "question": question
        }
    )

    rewritten = llm.invoke(prompt).content.strip()
    trace = state.get("execution_trace", [])
    trace.append("Rewrite")
    print("Original :", question)
    logger.info(
    f"REWRITE | Query rewritten"
    )

    return {
        "rewritten_question": rewritten,
        "rewrite_count": state["rewrite_count"] + 1,
    }