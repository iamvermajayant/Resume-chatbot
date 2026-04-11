from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from rag import generate_answer
from config import settings

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def home():
    return {"message": "🚀 Resume Chatbot API running"}


@app.post("/chat")
def chat(req: QueryRequest):
    answer, sources = generate_answer(req.query)

    return {
        "answer": answer,
        "sources": sources
    }
    
@app.get("/debug")
def debug():
    from db import debug_count
    return {"count": debug_count()}    