import time

from chains.rag_chain import RAGPipeline

rag = RAGPipeline()

while True:

    question = input("\nAsk: ")

    if question.lower() == "exit":
        break

    start = time.perf_counter()

    answer, docs = rag.ask(question)

    end = time.perf_counter()

    print("\nAnswer\n")
    print(answer)

    print("\nSources\n")

    for doc in docs:
        print(
            f"{doc.metadata.get('filename')} "
            f"(page {doc.metadata.get('page', 'N/A')})"
        )

    print(f"\nResponse Time: {(end - start):.2f} seconds")