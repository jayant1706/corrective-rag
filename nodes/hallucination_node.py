from utils.llm import llm
from utils.schema import HallucinationCheck
from prompts.hallucination import HALLUCINATION_PROMPT
from utils.logger import logger

checker = llm.with_structured_output(HallucinationCheck)


def check_hallucination(state):

    prompt = HALLUCINATION_PROMPT.invoke(
        {
            "context": state["generation_context"],
            "answer": state["generation"],
        }
    )

    result = checker.invoke(prompt)

    print("\n========== GROUNDING CHECK ==========")
    logger.info(
        f"GROUNDING | Grounded: {result.grounded}"
    )
    print("Reason   :", result.explanation)
    trace = state.get("execution_trace", [])
    trace.append("Grounding Check")
    return {
        "grounded": result.grounded,
        "grounding_reason": result.explanation,
    }