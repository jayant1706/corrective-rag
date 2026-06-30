MAX_REWRITES = 2


def decide_next(state):

    relevant = len(state["filtered_documents"])

    rewrites = state["rewrite_count"]

    print(f"\nRelevant Docs : {relevant}")
    print(f"Rewrite Count : {rewrites}")

    if relevant >= 2:
        return "generate"

    if rewrites >= MAX_REWRITES:
        return "generate"

    return "rewrite"