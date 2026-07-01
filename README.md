# 🤖 Corrective RAG Assistant

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.138-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B.svg)](https://streamlit.io/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agentic%20Workflow-purple.svg)](https://www.langchain.com/langgraph)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED.svg)](https://www.docker.com/)
[![Render](https://img.shields.io/badge/Backend-Render-46E3B7.svg)](https://render.com/)

An intelligent **Corrective Retrieval-Augmented Generation (CRAG)** system that enhances traditional RAG pipelines by evaluating retrieved documents, rewriting ambiguous queries, searching the web when necessary, and verifying generated responses before returning them to the user.

The project is built using **LangGraph**, **FastAPI**, **Streamlit**, **ChromaDB**, **Groq LLM**, and **Tavily Search**.

---

# 🌐 Live Demo

## 🖥️ Frontend

https://corrective-rag-hzkxrqzsxzmkbntenmk3ai.streamlit.app/

## 🚀 Backend API

https://corrective-rag-5x8d.onrender.com

## 📖 Swagger Documentation

https://corrective-rag-5x8d.onrender.com/docs

---

# ✨ Features

- 🔍 Retrieval-Augmented Generation (RAG)
- 🔄 Intelligent Query Rewriting
- 📄 LLM-based Document Relevance Grading
- 🌐 Automatic Web Search Fallback using Tavily
- 🧠 Hallucination Detection
- 🔁 Answer Regeneration when responses are not grounded
- ⚡ Agentic Workflow using LangGraph
- 📚 ChromaDB Vector Database
- 🚀 FastAPI REST Backend
- 🖥️ Streamlit Frontend
- 🐳 Dockerized Deployment
- ☁️ Cloud Deployment on Render & Streamlit Community Cloud

---

# 🏗️ System Architecture

```text
                    User
                      │
                      ▼
            Streamlit Frontend
                      │
            POST Request (/chat)
                      │
                      ▼
             FastAPI Backend
                      │
                      ▼
             LangGraph Workflow
                      │
     ┌────────────────┼────────────────┐
     │                │                │
     ▼                ▼                ▼
Retrieve Docs   Rewrite Query   Tavily Search
     │                │
     └──────────┬─────┘
                ▼
      Document Relevance Grading
                │
         Relevant Documents
                │
                ▼
        Answer Generation (Groq)
                │
                ▼
     Hallucination Detection
         │              │
         │              │
     Grounded      Not Grounded
         │              │
         ▼              ▼
 Return Response   Regenerate Answer
```

---

# 🛠️ Tech Stack

### Backend

- FastAPI
- LangGraph
- LangChain
- Groq API

### Frontend

- Streamlit

### Vector Database

- ChromaDB

### Embeddings

- HuggingFace Sentence Transformers

### Web Search

- Tavily Search API

### Deployment

- Docker
- Render
- Streamlit Community Cloud

---

# 📂 Project Structure

```
corrective-rag/
│
├── api/
│   └── main.py
│
├── frontend/
│   └── app.py
│
├── graph/
│   └── graph.py
│
├── nodes/
│
├── services/
│
├── utils/
│
├── evaluation/
│
├── Dockerfile
├── requirements.txt
├── requirements-docker.txt
├── README.md
└── .env.example
```

---

# ⚙️ Workflow

The Corrective RAG pipeline follows these stages:

1. User submits a question.
2. The query is rewritten if necessary.
3. Relevant documents are retrieved from ChromaDB.
4. Retrieved documents are graded for relevance.
5. If insufficient information is found, the system performs a Tavily web search.
6. The LLM generates an answer using the retrieved context.
7. A hallucination detector verifies whether the answer is grounded.
8. If the answer is not grounded, it is regenerated.
9. The final verified response is returned.

---

# 📡 API Endpoints

## Home

```
GET /
```

Response

```json
{
    "message": "Corrective RAG API Running"
}
```

---

## Chat

```
POST /chat
```

Request

```json
{
    "question": "What is LangGraph?"
}
```

Example Response

```json
{
    "answer": "...",
    "grounded": true,
    "latency": 1.84,
    "sources": [
        "LangGraph.pdf"
    ]
}
```

---

# 🚀 Running Locally

## Clone Repository

```bash
git clone https://github.com/jayant1706/corrective-rag.git
cd corrective-rag
```

---

## Create Virtual Environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file.

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

---

## Run Backend

```bash
uvicorn api.main:app --reload
```

Open:

```
http://localhost:8000
```

Swagger UI:

```
http://localhost:8000/docs
```

---

## Run Frontend

```bash
streamlit run frontend/app.py
```

---

# 🐳 Docker

## Build

```bash
docker build -t corrective-rag-api .
```

## Run

```bash
docker run -p 8000:8000 --env-file .env corrective-rag-api
```

---

# 📸 Screenshots

## Streamlit Frontend

<img width="1917" height="866" alt="image" src="https://github.com/user-attachments/assets/d6116479-b94c-4b11-9639-f2b5fca317b9" />


## Swagger API

<img width="1917" height="867" alt="image" src="https://github.com/user-attachments/assets/8acf903a-295c-4b13-8a1c-e89bc353dd15" />


## LangGraph Workflow

                 User Question
                       │
                       ▼
                 Retrieve Node
                       │
                       ▼
              Document Grader
                       │
         ┌─────────────┴─────────────┐
         │                           │
         ▼                           ▼
   Documents Relevant?            No Relevant Docs
         │                           │
         ▼                           ▼
    Generate Answer            Rewrite Query
         │                           │
         │                           ▼
         │                    Tavily Web Search
         │                           │
         └───────────────┬───────────┘
                         ▼
                Hallucination Check
                  │             │
                  │             │
            Grounded       Not Grounded
                  │             │
                  ▼             ▼
           Return Answer   Regenerate Answer

# 🔮 Future Improvements

- Multi-PDF Support
- Hybrid Retrieval
- RAGAS Evaluation Dashboard
- Conversation Memory
- User Authentication
- Streaming Responses
- Source Highlighting
- Kubernetes Deployment
- CI/CD Pipeline
- Monitoring & Logging

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new feature branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

---

# 👨‍💻 Author

**Jayant Singh Patel**

GitHub

https://github.com/jayant1706

LinkedIn

www.linkedin.com/in/jayant-singh-patel

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub. It helps others discover the project and supports future development.

---

# 📄 License

This project is licensed under the MIT License.
