from fastapi import APIRouter
from app.database.research_history import ResearchHistory, UsageTracking
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["analytics"])


@router.get("/analytics")
async def get_analytics():
    """Get research analytics and statistics"""
    try:
        analytics = ResearchHistory.get_analytics()
        usage = UsageTracking.get_usage()
        recent = ResearchHistory.get_recent(limit=5)
        
        return {
            "status": "success",
            "analytics": analytics,
            "usage": usage,
            "recent_researches": recent
        }
    
    except Exception as e:
        logger.error(f"Failed to get analytics: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }


@router.get("/history")
async def get_history(limit: int = 50):
    """Get research history"""
    try:
        history = ResearchHistory.get_recent(limit=limit)
        return {
            "status": "success",
            "history": history,
            "total": len(history)
        }
    
    except Exception as e:
        logger.error(f"Failed to get history: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }
