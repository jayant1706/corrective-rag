from langchain_core.prompts import ChatPromptTemplate

HALLUCINATION_PROMPT = ChatPromptTemplate.from_template("""
You are a rigorous factuality and hallucination auditor for an AI system.

Evaluate whether the generated answer is completely and faithfully grounded in the supplied context.

Context:
{context}

--------------------------

Generated Answer:
{answer}

--------------------------

Task:
Determine if all claims, facts, and statements in the answer are supported by the provided context. If any fact is invented, exaggerated, or contradictory to the context, marked grounded as false.

Output strictly valid JSON with the following structure:
{{
  "grounded": true or false,
  "confidence": float between 0.0 and 1.0,
  "explanation": "concise explanation of why the answer is or is not fully supported by context",
  "unsupported_claims": ["claim 1", "claim 2"]
}}

JSON:
""")