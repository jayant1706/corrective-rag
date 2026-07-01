import time

from graph.graph import graph
from utils.logger import logger

logger.info(
    "Corrective RAG started"
)

while True:

    question = input("\nAsk: ")
    logger.info(
        f"QUESTION | {question}"
    )

    if question.lower() == "exit":
        break

    state = {
    "question": question,
    "rewritten_question": "",
    "documents": [],
    "grounded":False,
    "generation_attempts":0,  
    "filtered_documents": [],
    "web_context": "",
    "generation": "",
    "rewrite_count": 0,
    }

    start = time.perf_counter()

    result = graph.invoke(state)
    end = time.perf_counter()
    logger.info(
        f"LATENCY | {end-start:.2f} sec"
    )
    print("\nAnswer\n")
    print(result["generation"])

    print(f"\nResponse Time : {end-start:.2f} sec")

logger.info(
    "REQUEST COMPLETED"
)