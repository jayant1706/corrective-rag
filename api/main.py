from fastapi import FastAPI

from api.models import ChatRequest
from api.service import ask_question

app = FastAPI(
    title="Corrective RAG API",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Corrective RAG API Running"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    return ask_question(request.question)