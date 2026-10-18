import os
import sys
import time
import requests
import streamlit as st

# Configure Root Directory
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from config import (
    AVAILABLE_MODELS,
    LLM_MODEL,
    TOP_K,
    RELEVANCE_THRESHOLD,
    ENABLE_WEB_SEARCH,
    DATA_DIR
)
from api.service import ask_question, get_documents_stats, ingest_file

# Streamlit Page Config
st.set_page_config(
    page_title="Corrective RAG Studio",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
css_path = os.path.join(os.path.dirname(__file__), "styles.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Session State Initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "selected_prompt" not in st.session_state:
    st.session_state.selected_prompt = ""

# Sidebar Configuration
with st.sidebar:
    st.markdown("### ⚙️ CRAG Control Panel")
    
    # Model Selector
    selected_model = st.selectbox(
        "🧠 LLM Engine (Groq)",
        options=AVAILABLE_MODELS,
        index=0 if LLM_MODEL in AVAILABLE_MODELS else 0,
        help="Select the inference model used for retrieval grading, rewriting, and generation."
    )
    
    col_sb1, col_sb2 = st.columns(2)
    with col_sb1:
        top_k_val = st.slider("Top-K Docs", min_value=2, max_value=10, value=TOP_K, step=1)
    with col_sb2:
        threshold_val = st.slider("Relevance Cutoff", min_value=1, max_value=10, value=RELEVANCE_THRESHOLD, step=1)
        
    web_fallback_toggle = st.toggle(
        "🌐 Web Search Fallback",
        value=ENABLE_WEB_SEARCH,
        help="When retrieved documents are insufficient, perform live web search via Tavily."
    )
    
    st.divider()
    
    # Execution Mode
    st.markdown("#### 🔌 Connection Mode")
    api_url = os.getenv("API_URL", "http://localhost:8000")
    
    backend_online = False
    try:
        r = requests.get(f"{api_url}/health", timeout=1.5)
        if r.status_code == 200:
            backend_online = True
    except Exception:
        backend_online = False

    if backend_online:
        st.markdown('<span class="crag-badge badge-emerald">● FastAPI Backend Connected</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="crag-badge badge-cyan">● Direct In-Process Mode</span>', unsafe_allow_html=True)
        st.caption("Backend offline; running pipeline directly in-process.")

    st.divider()
    
    # Knowledge Base Quick Stats
    st.markdown("#### 📊 Knowledge Base Stats")
    try:
        stats = get_documents_stats()
        st.metric("Total Indexed Chunks", stats.get("total_chunks", 0))
        st.caption(f"Indexed Files: {len(stats.get('documents', []))}")
    except Exception as e:
        st.caption("ChromaDB loading...")

# Main Hero Header
st.markdown("""
<div class="crag-hero">
    <div class="crag-badge-row">
        <span class="crag-badge badge-cyan">🛡️ Agentic CRAG</span>
        <span class="crag-badge badge-purple">⚡ LangGraph Workflow</span>
        <span class="crag-badge badge-emerald">🔍 Hybrid Grounding Audit</span>
        <span class="crag-badge badge-amber">🌐 Tavily Web Fallback</span>
    </div>
    <h1 class="crag-title">Corrective RAG Studio</h1>
    <p class="crag-subtitle">
        An intelligent self-correcting retrieval system that grades retrieved document relevance, 
        rewrites ambiguous questions, triggers live web search when local context is insufficient, 
        and actively audits hallucinations before returning verified answers.
    </p>
</div>
""", unsafe_allow_html=True)

# Navigation Tabs
tab_chat, tab_kb, tab_arch = st.tabs([
    "💬 CRAG Research Copilot",
    "🗂️ Knowledge Base & Ingestion",
    "⚡ Architecture & LangGraph Workflow"
])

# =========================================================================
# TAB 1: CRAG Research Copilot
# =========================================================================
with tab_chat:
    # Quick Starter Chips
    st.markdown("##### 💡 Suggested Questions")
    col_c1, col_c2, col_c3 = st.columns(3)
    
    with col_c1:
        if st.button("🤖 What is LangGraph and how does it work?", use_container_width=True):
            st.session_state.selected_prompt = "What is LangGraph and how does it work?"
    with col_c2:
        if st.button("🐍 Explain Python decorators with examples", use_container_width=True):
            st.session_state.selected_prompt = "Explain Python decorators with examples"
    with col_c3:
        if st.button("🌐 What are the latest AI breakthroughs in 2026?", use_container_width=True):
            st.session_state.selected_prompt = "What are the latest AI breakthroughs in 2026?"

    # Input Box Form
    with st.form("query_form", clear_on_submit=False):
        user_question = st.text_input(
            "Ask any question (searches indexed PDFs and falls back to live web if needed):",
            value=st.session_state.selected_prompt,
            placeholder="e.g., Explain the core architecture of LangGraph and its difference from standard chains",
            key="input_question"
        )
        col_btn, col_info = st.columns([1, 4])
        with col_btn:
            submitted = st.form_submit_button("🚀 Run CRAG Agent", use_container_width=True)
        with col_info:
            st.caption(f"Active Model: `{selected_model}` | Top-K: `{top_k_val}` | Cutoff: `{threshold_val}/10`")

    # Processing Logic
    if submitted and user_question.strip():
        with st.status("🤖 Corrective RAG Agent Active...", expanded=True) as status_box:
            st.write("🔍 **Stage 1:** Performing dense semantic retrieval from ChromaDB...")
            time.sleep(0.3)
            
            # Execute Pipeline
            try:
                if backend_online:
                    # Query through FastAPI
                    payload = {
                        "question": user_question,
                        "model": selected_model,
                        "top_k": top_k_val,
                        "relevance_threshold": threshold_val,
                        "enable_web_search": web_fallback_toggle
                    }
                    resp = requests.post(f"{api_url}/chat", json=payload, timeout=120)
                    resp.raise_for_status()
                    result = resp.json()
                else:
                    # In-process execution
                    result = ask_question(
                        question=user_question,
                        model=selected_model,
                        top_k=top_k_val,
                        relevance_threshold=threshold_val,
                        enable_web_search=web_fallback_toggle
                    )

                st.session_state.last_result = result
                status_box.update(label="✅ Corrective RAG Execution Completed!", state="complete", expanded=False)
            except Exception as ex:
                status_box.update(label=f"❌ Execution Error: {ex}", state="error")
                st.error(f"Error during CRAG execution: {ex}")

    # Display Last Result
    res = st.session_state.last_result
    if res:
        st.markdown("---")
        
        # 1. Dynamic Workflow Stepper Pipeline
        st.markdown("##### ⚡ Agent Execution Pathway")
        steps = res.get("step_history", [])
        if steps:
            pills_html = '<div class="workflow-pipeline">'
            for idx, s in enumerate(steps):
                badge_class = "active-cyan"
                if "Grade" in s:
                    badge_class = "active-pass"
                elif "Rewrite" in s or "Web" in s:
                    badge_class = "active-warn"
                elif "Grounding" in s:
                    badge_class = "active-pass" if res.get("grounded") else "active-warn"
                
                pills_html += f'<div class="step-node {badge_class}"><span>{idx + 1}.</span> {s}</div>'
                if idx < len(steps) - 1:
                    pills_html += '<span class="step-arrow">➔</span>'
            pills_html += '</div>'
            st.markdown(pills_html, unsafe_allow_html=True)

        # 2. Key Metrics Row
        kpi_cols = st.columns(4)
        with kpi_cols[0]:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">⚡ Response Time</div>
                <div class="kpi-value">{res.get('latency', 0.0):.2f}s</div>
                <div class="kpi-subtext">Total pipeline duration</div>
            </div>
            """, unsafe_allow_html=True)
            
        with kpi_cols[1]:
            is_grounded = res.get("grounded", False)
            conf = int(res.get("confidence", 1.0) * 100)
            status_text = "Verified Grounded" if is_grounded else "Correction Applied"
            badge_color = "#34d399" if is_grounded else "#fbbf24"
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">🛡️ Fact Grounding</div>
                <div class="kpi-value" style="color: {badge_color};">{status_text}</div>
                <div class="kpi-subtext">Confidence Score: {conf}%</div>
            </div>
            """, unsafe_allow_html=True)

        with kpi_cols[2]:
            graded_info = res.get("graded_documents_info", [])
            rel_count = sum(1 for d in graded_info if d.get("is_relevant"))
            total_retrieved = len(graded_info)
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">📊 Document Precision</div>
                <div class="kpi-value">{rel_count}/{total_retrieved}</div>
                <div class="kpi-subtext">Relevant chunks retained</div>
            </div>
            """, unsafe_allow_html=True)

        with kpi_cols[3]:
            route_label = "Local Vector Direct"
            if res.get("web_sources"):
                route_label = "Web Augmented"
            elif res.get("rewrite_count", 0) > 0:
                route_label = f"Query Rewritten ({res.get('rewrite_count')})"
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">🧭 Execution Route</div>
                <div class="kpi-value" style="font-size: 1.35rem;">{route_label}</div>
                <div class="kpi-subtext">Generation Attempts: {res.get('generation_attempts', 1)}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 3. Grounding Verification Audit Box
        grounded_status = res.get("grounded", False)
        grounding_reason = res.get("grounding_reason", "No audit details available.")
        box_class = "pass" if grounded_status else "fail"
        icon = "🛡️" if grounded_status else "⚠️"
        title = "Faithful & Grounded in Context" if grounded_status else "Grounding Audit / Self-Correction Note"
        
        st.markdown(f"""
        <div class="grounding-box {box_class}">
            <div class="grounding-icon">{icon}</div>
            <div class="grounding-content">
                <h4>{title}</h4>
                <p>{grounding_reason}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 4. Final Answer Box
        st.markdown("### 💬 Verified Response")
        st.markdown(res.get("answer", "No answer."))

        # 5. Expandable Sources Inspector
        with st.expander("📚 Inspect Sources & Retrieval Scoring", expanded=False):
            # Local Documents
            graded_docs = res.get("graded_documents_info", [])
            if graded_docs:
                st.markdown("##### 📄 Local Knowledge Chunks Evaluated")
                for d in graded_docs:
                    is_rel = d.get("is_relevant", False)
                    score = d.get("score", 5)
                    score_cls = "score-high" if is_rel else "score-low"
                    badge_lbl = f"Score {score}/10 (PASSED)" if is_rel else f"Score {score}/10 (FILTERED OUT)"
                    
                    st.markdown(f"""
                    <div class="doc-chunk-card">
                        <div class="doc-chunk-header">
                            <span class="doc-chunk-title">📄 {d.get('filename')} (Page {d.get('page', 'N/A')})</span>
                            <span class="doc-score-pill {score_cls}">{badge_lbl}</span>
                        </div>
                        <div class="doc-snippet">{d.get('snippet')}</div>
                        <div class="doc-reason"><b>Evaluator Rationale:</b> {d.get('reason')}</div>
                    </div>
                    """, unsafe_allow_html=True)

            # Web Sources
            web_srcs = res.get("web_sources", [])
            if web_srcs:
                st.markdown("##### 🌐 Live Web Search Results (Tavily)")
                for w in web_srcs:
                    st.markdown(f"""
                    <div class="doc-chunk-card" style="border-left: 3px solid #00f2fe;">
                        <div class="doc-chunk-header">
                            <span class="doc-chunk-title">🌐 <a href="{w.get('url')}" target="_blank" style="color: #38bdf8; text-decoration: none;">{w.get('title')}</a></span>
                            <span class="crag-badge badge-cyan">Web Result</span>
                        </div>
                        <div class="doc-snippet">{w.get('snippet')}</div>
                    </div>
                    """, unsafe_allow_html=True)

        # 6. Detailed Telemetry Trace
        with st.expander("🔬 Agent Telemetry & Query Rewriting Log", expanded=False):
            rewrites = res.get("rewritten_queries", [])
            if rewrites:
                st.markdown("##### ✍️ Query Transformation Log")
                for rw in rewrites:
                    st.info(f"**Attempt #{rw.get('iteration')}:** `{rw.get('rewritten')}`\n\n*Rationale:* {rw.get('reason')}")
            
            st.markdown("##### ⏱️ Step-by-Step Execution Trace")
            traces = res.get("execution_trace", [])
            for t in traces:
                st.write(f"• **{t.get('step')}** ({t.get('duration_sec', 0)}s) — {t.get('message')}")

# =========================================================================
# TAB 2: Knowledge Base & Ingestion
# =========================================================================
with tab_kb:
    st.markdown("### 🗂️ Knowledge Base Document Management")
    st.markdown("Upload documents (PDF, TXT, MD) to expand your local ChromaDB vector repository in real-time.")
    
    col_upload, col_catalog = st.columns([1, 1], gap="large")
    
    with col_upload:
        st.markdown("#### 📤 Upload Documents")
        uploaded_file = st.file_uploader(
            "Choose a document to index",
            type=["pdf", "txt", "md"],
            help="Supported formats: PDF, TXT, Markdown"
        )
        
        if uploaded_file is not None:
            st.write(f"📄 **Selected:** `{uploaded_file.name}` ({uploaded_file.size / 1024:.1f} KB)")
            if st.button("📥 Process & Ingest to ChromaDB", use_container_width=True):
                with st.spinner("Splitting, embedding, and storing in ChromaDB..."):
                    try:
                        save_path = os.path.join(DATA_DIR, uploaded_file.name)
                        os.makedirs(DATA_DIR, exist_ok=True)
                        with open(save_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        ingest_res = ingest_file(save_path)
                        st.success(f"✅ Indexed {uploaded_file.name}! Added {ingest_res['chunks_created']} chunks. Total collection size: {ingest_res['total_chunks']}.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to ingest: {e}")

    with col_catalog:
        st.markdown("#### 📚 Current Indexed Documents")
        try:
            stats = get_documents_stats()
            docs = stats.get("documents", [])
            st.write(f"**Total Collection Chunks:** `{stats.get('total_chunks', 0)}`")
            
            if docs:
                for d in docs:
                    st.markdown(f"""
                    <div class="doc-chunk-card">
                        <div class="doc-chunk-header">
                            <span class="doc-chunk-title">📄 {d.get('filename')}</span>
                            <span class="crag-badge badge-purple">{d.get('chunk_count')} Chunks</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No documents found in vectorstore. Upload a document to get started!")
        except Exception as e:
            st.error(f"Could not load vector store catalog: {e}")

# =========================================================================
# TAB 3: Architecture & LangGraph Workflow
# =========================================================================
with tab_arch:
    st.markdown("### ⚡ Corrective RAG Agentic Architecture")
    st.markdown("Below is the closed-loop state graph orchestrating document retrieval, quality grading, query rewriting, web search fallback, and hallucination self-correction.")
    
    # Mermaid Diagram of CRAG
    mermaid_code = """
    %%{init: {'theme': 'dark', 'themeVariables': { 'primaryColor': '#1e293b', 'primaryTextColor': '#f8fafc', 'primaryBorderColor': '#38bdf8', 'lineColor': '#00f2fe'}}}%%
    graph TD
        Q([User Question]) --> R[1. Retrieve Documents]
        R --> G[2. Grade Document Relevance]
        
        G -->|Docs >= Threshold| GEN[5. Generate Answer]
        G -->|Docs < Threshold & Retry < Max| RW[3. Rewrite Query]
        RW --> R
        
        G -->|Docs < Threshold & Retry >= Max| WEB[4. Live Web Search]
        WEB --> GEN
        
        GEN --> AUDIT[6. Hallucination Grounding Audit]
        
        AUDIT -->|Grounded / Max Retries| END([Return Verified Response])
        AUDIT -->|Not Grounded & No Web Context| WEB
        AUDIT -->|Not Grounded & Web Present| GEN
    """
    
    st.markdown(f"```mermaid\n{mermaid_code}\n```")
    
    st.markdown("""
    #### 🔄 Stage-by-Stage Architecture Highlights
    1. **Dense Retrieval:** Retrieves semantic chunks from ChromaDB using `sentence-transformers/all-MiniLM-L6-v2`.
    2. **Relevance Grading:** LLM examines each chunk in isolation and assigns a structured 1-10 score with reasoning.
    3. **Query Optimization:** If retrieval precision falls below the threshold, query rewriting clarifies terminology and context.
    4. **Web Search Fallback:** If local vector search remains insufficient, Tavily searches external live internet resources.
    5. **Context Generation:** Synthesizes an answer with inline citations (`[Doc X]`, `[Web X]`).
    6. **Hallucination Audit:** Evaluates factuality against provided context. If ungrounded claims are detected, the system triggers critique-driven self-correction.
    """)