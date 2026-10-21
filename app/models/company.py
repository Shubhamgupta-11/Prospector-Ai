from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Company(BaseModel):
    id: str
    name: str
    url: str
    industry: Optional[str] = None
    location: Optional[str] = None
    size: Optional[str] = None
    description: Optional[str] = None
    founded: Optional[str] = None
    funding: Optional[str] = None
    logo_url: Optional[str] = None
    tech_stack: list[str] = Field(default_factory=list)
    competitors: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CompanyProfile(BaseModel):
    """Raw company profile data"""
    name: str
    url: str
    industry: Optional[str] = None
    location: Optional[str] = None
    size: Optional[str] = None
    description: Optional[str] = None
    founded: Optional[str] = None
    funding: Optional[str] = None
    logo_url: Optional[str] = None
    products: list[str] = Field(default_factory=list)
    value_propositions: list[str] = Field(default_factory=list)
    target_customers: Optional[str] = None
