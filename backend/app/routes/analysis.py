from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from app.schemas.analysis import AnalysisRequest, AnalysisResponse
from app.services.analyzer import analyze

router = APIRouter(prefix="/api", tags=["análise"])

@router.post("/analyze", response_model=AnalysisResponse)
def analyze_message(payload: AnalysisRequest):
    try:
        result = analyze(payload.message)
        return AnalysisResponse(**result)
    except Exception:
        raise HTTPException(status_code=500, detail="Não foi possível concluir a análise. Tente novamente.")
