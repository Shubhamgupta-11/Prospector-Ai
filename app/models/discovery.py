from pydantic import BaseModel, Field
from typing import List, Optional


class DiscoveryRequest(BaseModel):
    """Request to discover companies based on ICP"""
    icp_description: str = Field(
        ...,
        description="Natural language description of ideal customer profile",
        min_length=10,
        max_length=2000
    )
    max_results: Optional[int] = Field(
        default=10,
        description="Maximum number of companies to return",
        ge=1,
        le=50
    )


class DiscoveredCompany(BaseModel):
    """A company discovered through ICP matching"""
    name: str = Field(..., description="Company name")
    url: str = Field(..., description="Company website URL")
    description: Optional[str] = Field(
        default=None,
        description="Brief description of the company"
    )


class DiscoveryResponse(BaseModel):
    """Response from discovery endpoint"""
    status: str = Field(default="success", description="Status of discovery")
    icp_description: str = Field(..., description="Original ICP description")
    companies: List[DiscoveredCompany] = Field(
        default_factory=list,
        description="List of discovered companies"
    )
    total_found: int = Field(..., description="Total number of companies found")
    error: Optional[str] = Field(
        default=None,
        description="Error message if discovery failed"
    )
