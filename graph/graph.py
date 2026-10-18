from langgraph.graph import StateGraph, END
from graph.state import GraphState
from graph.decision import decide_after_grade, decide_after_hallucination
from nodes.retrieve_node import retrieve
from nodes.grader_node import grade_documents
from nodes.rewrite_node import rewrite_query
from nodes.web_search_node import web_search
from nodes.generate_node import generate_answer
from nodes.hallucination_node import check_hallucination


def build_crag_graph():
    """Build and compile the complete Corrective RAG LangGraph workflow."""
    workflow = StateGraph(GraphState)

    # Add core nodes
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("grade", grade_documents)
    workflow.add_node("rewrite", rewrite_query)
    workflow.add_node("web", web_search)
    workflow.add_node("generate", generate_answer)
    workflow.add_node("hallucination", check_hallucination)

    # Set Entry Point
    workflow.set_entry_point("retrieve")

    # Retrieve -> Grade
    workflow.add_edge("retrieve", "grade")

    # Grade -> [Generate, Rewrite, Web]
    workflow.add_conditional_edges(
        "grade",
        decide_after_grade,
        {
            "generate": "generate",
            "rewrite": "rewrite",
            "web": "web",
        },
    )

    # Query Rewrite loop back to retrieval
    workflow.add_edge("rewrite", "retrieve")

    # Web search leads to generation
    workflow.add_edge("web", "generate")

    # Generation leads to factual grounding / hallucination audit
    workflow.add_edge("generate", "hallucination")

    # Hallucination audit conditional edges:
    # If grounded -> END
    # If ungrounded -> Web Search (if not yet run) or Regenerate with critique
    workflow.add_conditional_edges(
        "hallucination",
        decide_after_hallucination,
        {
            "end": END,
            "web": "web",
            "regenerate": "generate",
        },
    )

    return workflow.compile()


# Default compiled graph instance
graph = build_crag_graph()