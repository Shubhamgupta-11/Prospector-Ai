from pydantic import BaseModel, Field
from typing import Optional


class HiringSignal(BaseModel):
    title: str
    department: str
    signal: str
    url: Optional[str] = None


class NewsSignal(BaseModel):
    title: str
    date: str
    url: str
    relevance: str
    source: Optional[str] = None


class Signals(BaseModel):
    hiring: list[HiringSignal] = Field(default_factory=list)
    news: list[NewsSignal] = Field(default_factory=list)
    tech_stack: list[str] = Field(default_factory=list)
    competitors_detected: list[str] = Field(default_factory=list)
    recent_activities: list[str] = Field(default_factory=list)
