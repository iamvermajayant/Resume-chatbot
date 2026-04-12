from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from config import settings
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class QueryRequest(BaseModel):
    query: str

# Root route
@app.get("/")
def home():
    logger.info("✅ Server started successfully")
    port = os.environ.get("PORT", "Not set")
    return {
        "message": "🚀 Resume Chatbot API running",
        "port": port,
        "status": "healthy"
    }


# 🔥 LAZY LOAD EVERYTHING HERE
loaded = False

@app.post("/chat")
def chat(req: QueryRequest):
    global loaded

    try:
        # Import inside (VERY IMPORTANT for Render)
        from ingest import run_ingestion
        from rag import generate_answer

        # Load data only once
        if not loaded:
            logger.info("📄 Running ingestion...")
            run_ingestion()
            loaded = True
            logger.info("✅ Ingestion completed!")

        answer, sources = generate_answer(req.query)

        return {
            "answer": answer,
            "sources": sources
        }
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Debug route
@app.get("/debug")
def debug():
    try:
        from store import documents
        return {"count": len(documents)}
    except Exception as e:
        logger.error(f"Error in debug endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Debug error: {str(e)}")


# Health check route
@app.get("/health")
def health():
    return {"status": "healthy", "port": os.environ.get("PORT", "Not set")}


# Server startup for production
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting server on port {port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port)