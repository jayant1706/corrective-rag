def decide_to_generate(state):

    print("\nChecking document quality...\n")

    filtered_docs = state["filtered_documents"]

    if len(filtered_docs) >= 2:

        print("Enough relevant documents.\n")

        return "generate"

    print("Not enough relevant documents.\n")

    return "rewrite"