from fastapi import APIRouter, HTTPException
from app.models.research import ResearchRequest, ResearchResult
from app.agents.research_agent import ResearchAgent
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["research"])

# Initialize agent
research_agent = ResearchAgent()


@router.post("/research", response_model=ResearchResult)
async def research_company(request: ResearchRequest):
    """
    Research a company and return comprehensive intelligence
    
    - **company_url**: Company website URL (required)
    - **company_name**: Company name (optional, auto-detected)
    - **research_depth**: standard (default) | quick | deep
    - **seller_context**: Optional context about your product/service
    """
    try:
        logger.info(f"Research request for: {request.company_url}")
        
        result = await research_agent.research_company(
            company_url=request.company_url,
            company_name=request.company_name,
            research_depth=request.research_depth
        )
        
        # Save to history
        from app.database.research_history import ResearchHistory
        try:
            ResearchHistory.add_research(result.dict())
        except Exception as e:
            logger.error(f"Failed to save research history: {str(e)}")
        
        return result
    
    except Exception as e:
        logger.error(f"Research failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "research_api"}
