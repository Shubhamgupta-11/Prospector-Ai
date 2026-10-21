from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import logging
import os

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Import routes
from app.api.research import router as research_router
from app.api.discovery import router as discovery_router
from app.api.analytics import router as analytics_router
from app.api.settings import router as settings_router

# Create FastAPI app
app = FastAPI(
    title="Prospector AI API",
    version="1.0.0",
    description="AI-powered GTM intelligence - Hours of research in 70 secs"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(research_router)
app.include_router(discovery_router)
app.include_router(analytics_router)
app.include_router(settings_router)


@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "status": "online",
        "message": "Prospector AI API is running",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    """Health check"""
    openai_configured = bool(os.getenv("OPENAI_API_KEY"))
    tavily_configured = bool(os.getenv("TAVILY_API_KEY"))
    
    return {
        "status": "healthy",
        "openai_configured": openai_configured,
        "tavily_configured": tavily_configured,
        "ready": openai_configured  # Minimum requirement
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
