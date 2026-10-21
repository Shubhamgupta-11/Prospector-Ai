from fastapi import APIRouter, HTTPException, status
import logging

from app.models.discovery import DiscoveryRequest, DiscoveryResponse, DiscoveredCompany
from app.agents.discovery_agent import DiscoveryAgent

router = APIRouter(prefix="/api/v1", tags=["discovery"])
logger = logging.getLogger(__name__)


@router.post("/discover", response_model=DiscoveryResponse)
async def discover_companies(request: DiscoveryRequest):
    """
    Discover companies matching an Ideal Customer Profile (ICP)
    
    This endpoint takes a natural language description of your ideal customer
    and uses AI to find companies matching those criteria.
    """
    logger.info(f"Discovery request received: {request.icp_description[:100]}...")
    
    try:
        agent = DiscoveryAgent()
        
        # Execute discovery
        companies = await agent.discover_companies(
            icp_description=request.icp_description,
            max_results=request.max_results
        )
        
        # Convert to response model
        discovered = [
            DiscoveredCompany(
                name=company['name'],
                url=company['url'],
                description=company.get('description')
            )
            for company in companies
        ]
        
        return DiscoveryResponse(
            status="success",
            icp_description=request.icp_description,
            companies=discovered,
            total_found=len(discovered)
        )
    
    except Exception as e:
        logger.error(f"Discovery failed: {str(e)}")
        return DiscoveryResponse(
            status="failed",
            icp_description=request.icp_description,
            companies=[],
            total_found=0,
            error=str(e)
        )
