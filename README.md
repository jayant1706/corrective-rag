# 🤖 Corrective RAG with LangGraph

An advanced **Corrective Retrieval-Augmented Generation (CRAG)** system built using **LangGraph**, **LangChain**, **ChromaDB**, **Groq LLMs**, and **Streamlit**. The application improves retrieval quality by grading retrieved documents, rewriting ambiguous queries, performing web search fallback when necessary, and validating generated answers using a hallucination detection module.

---

## 🚀 Features

- 📄 Multi-format document ingestion
  - PDF
  - Markdown (.md)
  - Text (.txt)

- 🗂️ ChromaDB Vector Store

- 🔍 Semantic Retrieval using HuggingFace Embeddings

- 🤖 LangGraph-based Agentic Workflow

- 📊 Document Relevance Grading using Structured Outputs (Pydantic)

- ✍️ Automatic Query Rewriting

- 🌐 Tavily Web Search Fallback

- 🛡️ Hallucination Detection (Grounding Verification)

- 🔁 Self-Correcting Regeneration

- 💬 Streamlit Frontend

- 📈 Execution Trace and Performance Metrics

---

# 🏗️ Architecture

```
                    User Question
                          │
                          ▼
                   Retrieve Documents
                          │
                          ▼
                  Grade Retrieved Docs
                          │
          ┌───────────────┴───────────────┐
          │                               │
     Relevant                       Not Relevant
          │                               │
          ▼                               ▼
     Generate Answer              Rewrite Query
                                          │
                                          ▼
                                  Retrieve Again
                                          │
                               Max Retry Reached?
                                  │             │
                                 No            Yes
                                  │             ▼
                                  │      Web Search
                                  │             │
                                  └─────────────▼
                                      Generate Answer
                                             │
                                             ▼
                                  Hallucination Checker
                                  │                 │
                             Grounded        Not Grounded
                                  │                 │
                                  ▼                 ▼
                               Return        Regenerate Answer
```

---

# 📂 Project Structure

```text
corrective-rag/
│
├── data/
├── frontend/
│   └── app.py
│
├── graph/
│   ├── graph.py
│   ├── decision.py
│   └── state.py
│
├── ingestion/
│   ├── ingest.py
│   ├── loader.py
│   ├── splitter.py
│   └── vectorstore.py
│
├── nodes/
│   ├── retrieve_node.py
│   ├── grader_node.py
│   ├── rewrite_node.py
│   ├── generate_node.py
│   ├── web_search_node.py
│   └── hallucination_node.py
│
├── prompts/
├── utils/
│
├── app.py
├── config.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Tech Stack

| Component | Technology |
|-----------|------------|
| LLM | Groq (Llama 3.3 70B) |
| Framework | LangGraph |
| LLM Framework | LangChain |
| Embeddings | HuggingFace |
| Vector Database | ChromaDB |
| Web Search | Tavily |
| Frontend | Streamlit |
| Validation | Pydantic |

---

# 🔄 Workflow

1. User asks a question.
2. Retrieve relevant chunks from ChromaDB.
3. Grade each retrieved document using an LLM.
4. If retrieval quality is poor:
   - Rewrite the query.
   - Retrieve again.
5. If retrieval still fails:
   - Perform a Tavily web search.
6. Generate an answer from the available context.
7. Verify that the answer is grounded in the retrieved context.
8. If the answer is not grounded:
   - Regenerate using the grounding feedback.
9. Return the final verified response.

---

# 💻 Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/corrective-rag.git
cd corrective-rag
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file.

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

---

# 📄 Index Your Documents

Place your documents inside the `data/` directory and run:

```bash
python ingestion/ingest.py
```

---

# ▶️ Run the Application

Terminal version:

```bash
python app.py
```

Streamlit version:

```bash
streamlit run frontend/app.py
```

---

# 📊 Example Features

- Query rewriting for ambiguous questions
- Automatic retrieval grading
- Web search fallback
- Hallucination detection
- Execution trace
- Source document display
- Response latency measurement

---

# 🌟 Future Improvements

- FastAPI backend
- Docker support
- Authentication
- Conversation memory
- Multi-user support
- RAGAS evaluation
- Cloud deployment
- CI/CD pipeline

---

# 📸 Screenshots

Add screenshots of:

- Streamlit UI
- Execution trace
- Source documents
- Hallucination detection

---

# 👨‍💻 Author

**Jayant Singh Patel**

B.Tech Computer Science Engineering

Interested in:
- Generative AI
- Retrieval-Augmented Generation (RAG)
- AI Agents
- Machine Learning
- Backend Development

---

# 📜 License

This project is licensed under the MIT License.
