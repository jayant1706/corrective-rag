from ingestion.embedder import get_embedding_model
from ingestion.vectorstore import load_vectorstore

from config import TOP_K


def main():

    embeddings = get_embedding_model()

    db = load_vectorstore(embeddings)

    retriever = db.as_retriever(
        search_kwargs={
            "k": TOP_K
        }
    )

    while True:

        query = input("\nAsk a question (type exit to quit): ")

        if query.lower() == "exit":
            break

        docs = retriever.invoke(query)

        print("\nRetrieved Documents\n")

        for i, doc in enumerate(docs, 1):

            print("=" * 80)

            print(f"Chunk {i}")

            print(f"Source : {doc.metadata.get('filename')}")

            print(f"Page   : {doc.metadata.get('page','N/A')}")

            print()

            print(doc.page_content[:500])

            print()


if __name__ == "__main__":
    main()