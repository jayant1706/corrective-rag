import time

from graph.graph import graph


while True:

    question = input("\nAsk: ")

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

    print("\nAnswer\n")
    print(result["generation"])

    print(f"\nResponse Time : {end-start:.2f} sec")