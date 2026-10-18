from langchain_core.prompts import ChatPromptTemplate

REWRITE_PROMPT = ChatPromptTemplate.from_template("""
You are an expert search query optimizer for vector and semantic retrieval.

A user's initial question failed to retrieve sufficiently relevant documents from the knowledge base.
Analyze the user's question and rewrite it to maximize search relevance, precision, and keyword overlap.

Requirements:
- Preserve the exact user intent.
- Expand ambiguous terms, acronyms, or pronouns with specific technical terms.
- Do NOT answer the question.

Original Question:
{question}

Output strictly valid JSON:
{{
  "rewritten_query": "the optimized semantic search query",
  "reason": "1-sentence explanation of what was clarified or expanded"
}}

JSON:
""")