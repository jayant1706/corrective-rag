from ingestion.embedder import get_embedding_model
from ingestion.vectorstore import load_vectorstore

from config import TOP_K

embeddings = get_embedding_model()

db = load_vectorstore(embeddings)

retriever = db.as_retriever(
    search_kwargs={
        "k": TOP_K
    }
)


def retrieve(state):

    print("\nRetrieving Documents...\n")

    question = (
        state["rewritten_question"]
        if state["rewritten_question"]
        else state["question"]
    )

    documents = retriever.invoke(question)

    trace = state.get("execution_trace", [])

    trace.append("Retrieve")

    return {

        "documents": documents,

        "execution_trace": trace

    }