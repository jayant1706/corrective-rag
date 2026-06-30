from nodes.retrieve_node import retrieve
from nodes.grader_node import grade_documents

state = {
    "question": "What is LangGraph?"
}

state.update(retrieve(state))

state.update(grade_documents(state))

print("\nRelevant Documents:\n")

for doc in state["filtered_documents"]:

    print("-" * 80)

    print(doc.metadata.get("filename"))

    print(doc.page_content[:300])