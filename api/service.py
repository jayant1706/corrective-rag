import time

from graph.graph import graph


def ask_question(question: str):

    state = {
        "question": question,
        "rewritten_question": "",
        "documents": [],
        "filtered_documents": [],
        "web_context": "",
        "generation": "",
        "generation_context": "",
        "rewrite_count": 0,
        "generation_attempts": 0,
        "grounded": False,
        "grounding_reason": "",
        "execution_trace": [],
    }

    start = time.perf_counter()

    result = graph.invoke(state)

    end = time.perf_counter()

    return {
        "answer": result["generation"],
        "grounded": result["grounded"],
        "rewrite_count": result["rewrite_count"],
        "latency": round(end - start, 2),
        "sources": list(
            {
                doc.metadata.get("filename", "Unknown Source")
                for doc in result["filtered_documents"]
            }
        ),
    }