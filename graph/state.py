from typing import TypedDict, List

from langchain_core.documents import Document


class GraphState(TypedDict):

    question: str

    documents: List[Document]

    filtered_documents: List[Document]

    generation: str

    rewrite_count: int