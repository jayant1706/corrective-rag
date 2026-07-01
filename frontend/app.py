import os
import sys

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000/chat"
)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

import streamlit as st
import time

import requests

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
    start = time.perf_counter()

    with st.spinner("Thinking..."):

        try:
            response = requests.post(
                API_URL,
                json={"question": question},
                timeout=120,
            )

            response.raise_for_status()

            result = response.json()

        except requests.exceptions.ConnectionError:

            st.error("FastAPI backend is not running.")

            st.info("Run the backend using:")

            st.code("uvicorn api.main:app --reload")

            st.stop()

        except Exception as e:

            st.error(f"Error: {e}")

            st.stop()

    end = time.perf_counter()

    # ---------------- Answer ----------------
    st.subheader("💬 Answer")
    st.markdown(result["answer"])

    st.divider()

    # ---------------- Sources ----------------
    st.subheader("📚 Sources")

    for source in result["sources"]:
        st.write(f"📄 {source}")

    st.divider()

    # ---------------- Metrics ----------------
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Latency",
        f'{result["latency"]:.2f}s'
    )

    col2.metric(
        "Grounded",
        "Yes" if result["grounded"] else "No"
    )

    col3.metric(
        "Rewrites",
        result["rewrite_count"]
    )

    st.divider()

    # ---------------- Execution Trace ----------------
    st.subheader("⚡ Execution Trace")

    for step in result["execution_trace"]:

        st.success(step)
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