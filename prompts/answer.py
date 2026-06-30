from langchain_core.prompts import ChatPromptTemplate

ANSWER_PROMPT = ChatPromptTemplate.from_template(
"""
You are an expert assistant.

Use ONLY the supplied documents.

If the answer is not present,

say

"I don't know based on the provided documents."

Do not invent facts.

Cite document numbers whenever possible.

=====================

{context}

=====================

Question

{question}

Answer
"""
)