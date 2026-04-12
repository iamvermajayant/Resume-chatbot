import logging
import os

# Configure logging FIRST
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    logger.info("Starting application import...")
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
    from fastapi.middleware.cors import CORSMiddleware
    logger.info("FastAPI imports successful")
    
    from config import settings
    logger.info("Config loaded successfully")
    
    app = FastAPI(title="Resume Chatbot API", version="1.0.0")
    logger.info("FastAPI app created successfully")
    
except Exception as e:
    logger.error(f"Failed to initialize app: {str(e)}")
    raise

# CORS
try:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info("CORS middleware added successfully")
except Exception as e:
    logger.error(f"Failed to add CORS middleware: {str(e)}")
    raise

# Request model
class QueryRequest(BaseModel):
    query: str

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Application startup complete")
    logger.info(f"PORT environment variable: {os.environ.get('PORT', 'Not set')}")

# Root route
@app.get("/")
def home():
    logger.info("✅ Root endpoint accessed")
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

# Simple ping route
@app.get("/ping")
def ping():
    return {"message": "pong"}


# Server startup for production
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting server on port {port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port)