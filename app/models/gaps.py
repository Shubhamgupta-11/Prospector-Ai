from pydantic import BaseModel, Field


class Gap(BaseModel):
    title: str
    description: str
    evidence: list[str] = Field(default_factory=list)
    severity: str  # "HIGH" | "MEDIUM" | "LOW"
    actionable_insight: str = ""


class GapAnalysis(BaseModel):
    primary: Gap
    secondary: list[Gap] = Field(default_factory=list)
