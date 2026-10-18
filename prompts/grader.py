from langchain_core.prompts import ChatPromptTemplate

GRADE_PROMPT = ChatPromptTemplate.from_template("""
You are an expert retrieval evaluator assessing document relevance for answering a user's question.

Question:
{question}

Retrieved Document Content:
{document}

Scoring Criteria:
- 10: Directly and fully answers the question with specific details.
- 7-9: Contains highly relevant facts or context needed to answer the question.
- 4-6: Partially mentions the topic but lacks substantial answering capability.
- 1-3: Completely irrelevant, off-topic, or discusses unrelated concepts (e.g., Python code when asked about quantum computing).

Output strictly valid JSON with the following keys:
- "score": integer from 1 to 10
- "is_relevant": boolean (true ONLY if score >= 7 and document directly helps answer the question; otherwise false)
- "reason": concise 1-sentence reason explaining why it is or is not relevant.

JSON:
""")