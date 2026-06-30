from langchain_core.prompts import ChatPromptTemplate

HALLUCINATION_PROMPT = ChatPromptTemplate.from_template("""
You are a factuality evaluator.

Determine whether the generated answer is completely supported by the supplied context.

Context:

{context}

--------------------------

Generated Answer:

{answer}

Respond only with whether the answer is grounded in the context.
""")