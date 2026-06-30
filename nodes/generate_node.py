from prompts.answer import ANSWER_PROMPT
from utils.llm import llm


def generate_answer(state):

    print("\nGenerating Answer...\n")

    docs = state["filtered_documents"]
    question = state["question"]

    context = ""

    if docs:
        for i, doc in enumerate(docs, start=1):
            context += f"""
Document {i}

Source:
{doc.metadata.get("filename")}

Page:
{doc.metadata.get("page", "N/A")}

Content:
{doc.page_content}

------------------------
"""

    if state["web_context"]:
        context += """

====================

WEB SEARCH RESULTS

====================

"""

        context += state["web_context"]

    prompt = ANSWER_PROMPT.invoke(
        {
            "context": context,
            "question": question,
        }
    )

    response = llm.invoke(prompt)
    trace = state.get("execution_trace", [])
    trace.append("Generate")
    return {
        "generation": response.content,
        "generation_attempts":
        state["generation_attempts"]+1
    }