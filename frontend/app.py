import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

import streamlit as st
import time

from graph.graph import graph

st.set_page_config(
    page_title="Corrective RAG",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Corrective RAG Assistant")
question = st.text_input(
    "Ask a question"
)

submit = st.button("Ask")
if submit:
    state = {
        "question": question,
        "rewritten_question": "",
        "documents": [],
        "filtered_documents": [],
        "web_context": "",
        "generation": "",
        "generation_context": "",
        "rewrite_count": 0,
        "generation_attempts": 0,
        "grounded": False,
        "grounding_reason": "",
        "execution_trace": [],
    }

    start = time.perf_counter()

    with st.spinner("Thinking..."):
        result = graph.invoke(state)

    end = time.perf_counter()

    # ---------------- Answer ----------------
    st.subheader("💬 Answer")
    st.markdown(result["generation"])

    st.divider()

    # ---------------- Sources ----------------
    st.subheader("📚 Sources")

    for doc in result["filtered_documents"]:
        with st.expander(
            f"📄 {doc.metadata.get('filename')} "
            f"(Page {doc.metadata.get('page', 'N/A')})"
        ):
            st.write(doc.page_content)

    st.divider()

    # ---------------- Metrics ----------------
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Response Time",
        f"{end-start:.2f}s"
    )

    col2.metric(
        "Relevant Docs",
        len(result["filtered_documents"])
    )

    col3.metric(
        "Grounded",
        "✅" if result["grounded"] else "❌"
    )

    st.divider()

    # ---------------- Execution Trace ----------------
    st.subheader("⚡ Execution Trace")

    for step in result["execution_trace"]:
        st.success(step)

    if not result["grounded"]:
        st.warning(result["grounding_reason"])
with st.sidebar:

    st.header("⚙️ Corrective RAG")

    st.markdown("### Tech Stack")

    st.success("LangGraph")
    st.success("ChromaDB")
    st.success("HuggingFace Embeddings")
    st.success("Groq")
    st.success("Tavily")

    st.divider()

    st.markdown("### Features")

    st.write("✅ Query Rewriting")
    st.write("✅ Document Grading")
    st.write("✅ Web Search Fallback")
    st.write("✅ Hallucination Detection")