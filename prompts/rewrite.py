from langchain_core.prompts import ChatPromptTemplate

REWRITE_PROMPT = ChatPromptTemplate.from_template("""
You are an expert search query optimizer.

Rewrite the user's question to improve document retrieval.

Requirements:

- Preserve the original meaning.
- Make the query more specific.
- Add important keywords if necessary.
- Do not answer the question.

Original Question:

{question}

Improved Question:
""")