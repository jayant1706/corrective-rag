import os
import shutil
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from api.models import (
    ChatRequest,
    ChatResponse,
    DocumentStatsResponse,
    UploadResponse
)
from api.service import ask_question, get_documents_stats, ingest_file
from config import AVAILABLE_MODELS, DATA_DIR

app = FastAPI(
    title="🤖 Corrective RAG API",
    description="Production-grade Corrective Retrieval-Augmented Generation API with self-correcting feedback and grounding verification.",
    version="2.0.0"
)

# Enable CORS for Streamlit or custom frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "status": "online",
        "service": "Corrective RAG API",
        "version": "2.0.0",
        "endpoints": ["/chat", "/documents", "/upload", "/models", "/health"]
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "groq_configured": bool(os.getenv("GROQ_API_KEY")),
        "tavily_configured": bool(os.getenv("TAVILY_API_KEY"))
    }


@app.get("/models")
def list_models():
    return {
        "available_models": AVAILABLE_MODELS,
        "default": AVAILABLE_MODELS[0] if AVAILABLE_MODELS else "openai/gpt-oss-120b"
    }


@app.get("/documents", response_model=DocumentStatsResponse)
def get_documents():
    stats = get_documents_stats()
    return stats


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        result = ask_question(
            question=request.question,
            model=request.model,
            top_k=request.top_k or 5,
            relevance_threshold=request.relevance_threshold or 7,
            enable_web_search=request.enable_web_search if request.enable_web_search is not None else True
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    target_dir = Path(DATA_DIR)
    target_dir.mkdir(parents=True, exist_ok=True)
    file_path = target_dir / file.filename

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = ingest_file(str(file_path))
        return UploadResponse(
            success=True,
            message=result["message"],
            filename=file.filename,
            chunks_created=result["chunks_created"],
            total_chunks=result["total_chunks"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to ingest file: {str(e)}")