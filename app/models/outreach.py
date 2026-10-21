from pydantic import BaseModel, Field


class OutreachMessage(BaseModel):
    type: str  # "gap-based" | "timing-based" | "curiosity-based"
    subject: str = ""
    message: str
    word_count: int
    references: list[str] = Field(default_factory=list)
    tone: str = "professional"
