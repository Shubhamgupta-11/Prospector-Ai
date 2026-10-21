from pydantic import BaseModel, Field


class ScoreBreakdown(BaseModel):
    category: str
    score: int
    max_score: int
    evidence: list[str] = Field(default_factory=list)
    reasoning: str = ""


class IntentScore(BaseModel):
    overall: int  # 0-100
    breakdown: dict[str, ScoreBreakdown]
    recommendation: str  # "HIGH PRIORITY" | "MEDIUM" | "LOW"
    summary: str = ""
