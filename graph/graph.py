from langgraph.graph import StateGraph, END

from graph.state import GraphState

from graph.decision import decide_next

from nodes.retrieve_node import retrieve
from nodes.grader_node import grade_documents
from nodes.rewrite_node import rewrite_query
from nodes.generate_node import generate_answer


workflow = StateGraph(GraphState)

workflow.add_node("retrieve", retrieve)
workflow.add_node("grade", grade_documents)
workflow.add_node("rewrite", rewrite_query)
from nodes.web_search_node import web_search

workflow.add_node("web", web_search)
workflow.add_node("generate", generate_answer)
workflow.add_edge("web", "generate")

workflow.set_entry_point("retrieve")

workflow.add_edge("retrieve", "grade")

workflow.add_conditional_edges(
    "grade",
    decide_next,
    {
        "generate": "generate",
        "rewrite": "rewrite",
        "web": "web",
    },
)

workflow.add_edge("rewrite", "retrieve")
workflow.add_edge("generate", END)

graph = workflow.compile()