from langchain_chroma import Chroma

from config import CHROMA_DB


def create_vectorstore(documents, embeddings):

    db = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=CHROMA_DB,
    )

    return db


def load_vectorstore(embeddings):

    return Chroma(
        persist_directory=CHROMA_DB,
        embedding_function=embeddings,
    )