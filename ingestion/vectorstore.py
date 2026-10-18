from typing import List, Dict, Any
from langchain_chroma import Chroma
from langchain_core.documents import Document
from config import CHROMA_DB
from utils.logger import logger


def create_vectorstore(documents: List[Document], embeddings) -> Chroma:
    """Create or overwrite the Chroma vectorstore with documents."""
    db = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=CHROMA_DB,
    )
    return db


def load_vectorstore(embeddings) -> Chroma:
    """Load an existing Chroma vectorstore."""
    return Chroma(
        persist_directory=CHROMA_DB,
        embedding_function=embeddings,
    )


def add_documents_to_vectorstore(documents: List[Document], embeddings) -> int:
    """Incrementally add documents to existing vectorstore and return added count."""
    db = load_vectorstore(embeddings)
    if documents:
        db.add_documents(documents)
        logger.info(f"VECTORSTORE | Added {len(documents)} chunks to ChromaDB")
    return len(documents)


def get_vectorstore_stats(embeddings=None) -> Dict[str, Any]:
    """Retrieve indexed document file list and chunk statistics from ChromaDB instantly."""
    try:
        import chromadb
        client = chromadb.PersistentClient(path=CHROMA_DB)
        collections = client.list_collections()
        if not collections:
            return {"total_chunks": 0, "documents": [], "collection_name": "none"}

        # Use the first or default 'langchain' collection
        target_name = "langchain" if any(c.name == "langchain" for c in collections) else collections[0].name
        collection = client.get_collection(target_name)
        total_chunks = collection.count()

        # Fetch metadatas to extract filenames and counts
        doc_data = collection.get(include=["metadatas"])
        metadatas = doc_data.get("metadatas", []) or []

        file_counts: Dict[str, int] = {}
        for meta in metadatas:
            if meta and "filename" in meta:
                fn = meta["filename"]
                file_counts[fn] = file_counts.get(fn, 0) + 1

        docs_list = [
            {
                "filename": fn,
                "chunk_count": count,
                "extension": ("." + fn.split(".")[-1].lower()) if "." in fn else ""
            }
            for fn, count in file_counts.items()
        ]

        return {
            "total_chunks": total_chunks,
            "documents": sorted(docs_list, key=lambda x: x["chunk_count"], reverse=True),
            "collection_name": target_name
        }
    except Exception as e:
        logger.error(f"Error fetching vectorstore stats: {e}")
        return {
            "total_chunks": 0,
            "documents": [],
            "collection_name": "chroma"
        }