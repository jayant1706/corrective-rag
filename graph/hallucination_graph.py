MAX_GENERATION_ATTEMPTS = 2


def decide_grounding(state):

    if state["grounded"]:

        return "end"

    return "generate"