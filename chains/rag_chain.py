from ingestion.embedder import get_embedding_model
from ingestion.vectorstore import load_vectorstore

from utils.llm import llm

from prompts.answer import ANSWER_PROMPT

from config import TOP_K


class RAGPipeline:

    def __init__(self):
        embeddings = get_embedding_model()
        db = load_vectorstore(embeddings)

        self.retriever = db.as_retriever(
            search_kwargs={
                "k": TOP_K
            }
        )

    def ask(self, question):

        docs = self.retriever.invoke(question)

        context = ""

        for i, doc in enumerate(docs, start=1):

            context += f"""
Document {i}

Source:
{doc.metadata.get('filename')}

Page:
{doc.metadata.get('page', 'N/A')}

Content:
{doc.page_content}

--------------------
"""

        prompt = ANSWER_PROMPT.invoke(
            {
                "context": context,
                "question": question
            }
        )

        response = llm.invoke(prompt)

        return response.content, docs