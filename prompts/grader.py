from langchain_core.prompts import ChatPromptTemplate

GRADE_PROMPT = ChatPromptTemplate.from_template("""
You are an expert retrieval evaluator.

Evaluate whether the retrieved document is relevant for answering the user's question.

Question:
{question}

Document:
{document}

Give a relevance score from 1 to 10.

Scoring Guide:

10 -> Directly answers the question.

8-9 -> Highly relevant.

6-7 -> Somewhat relevant.

3-5 -> Weakly relevant.

1-2 -> Completely irrelevant.
""")