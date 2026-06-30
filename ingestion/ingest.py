from ingestion.loader import load_documents
from ingestion.splitter import split_documents
from ingestion.embedder import get_embedding_model
from ingestion.vectorstore import create_vectorstore


def ingest():

    print("Loading documents...")

    documents = load_documents()

    print("Splitting documents...")

    chunks = split_documents(documents)

    print("Loading embedding model...")

    embeddings = get_embedding_model()

    print("Creating Chroma vector database...")

    create_vectorstore(chunks, embeddings)

    print("\nVector database created successfully!")


if __name__ == "__main__":
    ingest()