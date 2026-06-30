from langchain_core.prompts import ChatPromptTemplate

GRADE_PROMPT = ChatPromptTemplate.from_template(
"""
You are a document relevance grader.

Question:

{question}

Document:

{document}

Is this document relevant?

Answer ONLY:

yes

or

no
"""
)