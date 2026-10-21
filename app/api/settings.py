from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database.research_history import Settings
import os
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["settings"])


class SettingsUpdate(BaseModel):
    research_depth: str = None
    discovery_limit: int = None
    email: str = None


class APIKeyTest(BaseModel):
    provider: str


@router.get("/settings")
async def get_settings():
    """Get current settings"""
    try:
        settings = Settings.get()
        
        # Add API key status (masked)
        api_status = {
            "gemini": {
                "configured": bool(os.getenv("GOOGLE_API_KEY")),
                "key_preview": _mask_key(os.getenv("GOOGLE_API_KEY", ""))
            },
            "tavily": {
                "configured": bool(os.getenv("TAVILY_API_KEY")),
                "key_preview": _mask_key(os.getenv("TAVILY_API_KEY", ""))
            },
            "serpapi": {
                "configured": bool(os.getenv("SERPAPI_API_KEY")),
                "key_preview": _mask_key(os.getenv("SERPAPI_API_KEY", ""))
            },
            "brave": {
                "configured": bool(os.getenv("BRAVE_API_KEY")),
                "key_preview": _mask_key(os.getenv("BRAVE_API_KEY", ""))
            }
        }
        
        return {
            "status": "success",
            "settings": settings,
            "api_keys": api_status
        }
    
    except Exception as e:
        logger.error(f"Failed to get settings: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/settings")
async def update_settings(update: SettingsUpdate):
    """Update settings"""
    try:
        # Build update dict
        updates = {}
        if update.research_depth:
            updates['research_depth'] = update.research_depth
        if update.discovery_limit:
            updates['discovery_limit'] = update.discovery_limit
        if update.email:
            updates['email'] = update.email
        
        Settings.update(updates)
        
        return {
            "status": "success",
            "message": "Settings updated successfully"
        }
    
    except Exception as e:
        logger.error(f"Failed to update settings: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/settings/test-api")
async def test_api_key(test: APIKeyTest):
    """Test if an API key is working"""
    provider = test.provider.lower()
    
    try:
        if provider == "gemini":
            from app.utils.gemini_client import GeminiClient
            client = GeminiClient()
            response = client.generate_content("Say 'connected' if you can read this")
            return {
                "status": "success",
                "provider": provider,
                "message": "Connected successfully"
            }
        
        elif provider == "tavily":
            from app.scrapers.tavily_search import TavilySearch
            searcher = TavilySearch()
            results = await searcher.search("test", limit=1)
            return {
                "status": "success",
                "provider": provider,
                "message": f"Connected successfully - {len(results)} results"
            }
        
        else:
            return {
                "status": "error",
                "message": f"Unknown provider: {provider}"
            }
    
    except Exception as e:
        logger.error(f"API test failed for {provider}: {str(e)}")
        return {
            "status": "error",
            "provider": provider,
            "message": str(e)
        }


def _mask_key(key: str) -> str:
    """Mask API key for display"""
    if not key or len(key) < 8:
        return ""
    
    # Show first few chars
    if key.startswith("AQ."):
        return f"AQ.{'•' * 32}"
    elif key.startswith("tvly-"):
        return f"tvly-{'•' * 28}"
    elif key.startswith("sk-"):
        return f"sk-{'•' * 32}"
    else:
        return f"{key[:4]}{'•' * 28}"
