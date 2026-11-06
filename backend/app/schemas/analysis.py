from pydantic import BaseModel, Field, field_validator
from app.core.config import settings

class AnalysisRequest(BaseModel):
    message: str = Field(min_length=1, max_length=settings.MAX_MESSAGE_LENGTH)

    @field_validator("message")
    @classmethod
    def not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Digite uma mensagem para analisar.")
        return value.strip()

class Signal(BaseModel):
    title: str
    explanation: str

class AnalysisResponse(BaseModel):
    classification: str
    score: int
    summary: str
    signals: list[Signal]
    advice: str
    source: str
    disclaimer: str
