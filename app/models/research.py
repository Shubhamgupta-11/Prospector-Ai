from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .company import Company
from .signals import Signals
from .scoring import IntentScore
from .gaps import GapAnalysis
from .outreach import OutreachMessage


class Source(BaseModel):
    url: str
    scraped_at: datetime
    type: str  # "website" | "search" | "news" | "jobs"
    status: str = "success"


class ResearchMetadata(BaseModel):
    research_time_seconds: float
    tokens_used: int = 0
    cost_usd: float = 0.0
    research_depth: str = "standard"
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ResearchResult(BaseModel):
    id: str
    status: str  # "completed" | "partial" | "failed"
    company: Company
    signals: Signals
    intent_score: IntentScore
    gaps: GapAnalysis
    outreach_messages: list[OutreachMessage] = Field(default_factory=list)
    sources: list[Source] = Field(default_factory=list)
    metadata: ResearchMetadata
    error: Optional[str] = None


class ResearchRequest(BaseModel):
    company_url: str
    company_name: Optional[str] = None
    research_depth: str = "standard"  # "quick" | "standard" | "deep"
    seller_context: Optional[dict] = None
