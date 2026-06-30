from utils.llm import llm
from prompts.rewrite import REWRITE_PROMPT


MAX_REWRITES = 2


def rewrite_query(state):

    print("\nRewriting Query...\n")

    question = state["question"]

    prompt = REWRITE_PROMPT.invoke(
        {
            "question": question
        }
    )

    rewritten = llm.invoke(prompt).content.strip()

    print("Original :", question)
    print("Rewritten:", rewritten)

    return {
        "rewritten_question": rewritten,
        "rewrite_count": state["rewrite_count"] + 1,
    }