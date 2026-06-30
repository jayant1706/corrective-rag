from prompts.answer import ANSWER_PROMPT
from utils.llm import llm


def generate_answer(state):

    print("\nGenerating Answer...\n")

    docs = state["filtered_documents"]

    question = state["question"]

    context = ""

    for i, doc in enumerate(docs, start=1):

        context += f"""
Document {i}

Source:
{doc.metadata.get("filename")}

Page:
{doc.metadata.get("page","N/A")}

Content:
{doc.page_content}

------------------------
"""

    prompt = ANSWER_PROMPT.invoke(
        {
            "context": context,
            "question": question,
        }
    )

    response = llm.invoke(prompt)

    return {
        "generation": response.content
    }