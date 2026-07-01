from prompts.grader import GRADE_PROMPT
from utils.llm import llm
from utils.schema import GradeDocument
from utils.logger import logger

structured_llm = llm.with_structured_output(GradeDocument)


def grade_documents(state):

    print("\nGrading Documents...\n")

    question = state["question"]
    documents = state["documents"]

    filtered_docs = []

    for i, doc in enumerate(documents, start=1):

        prompt = GRADE_PROMPT.invoke(
            {
                "question": question,
                "document": doc.page_content,
            }
        )

        result = structured_llm.invoke(prompt)

        score = result.score

        print(f"Document {i}: Score = {score}")

        if score >= 7:
            filtered_docs.append(doc)

    logger.info(
    f"GRADE | Relevant documents: {len(filtered_docs)}"
    )
    trace = state.get("execution_trace", [])

    trace.append("Grade")

    return {

        "filtered_documents": filtered_docs,

        "execution_trace": trace

    }