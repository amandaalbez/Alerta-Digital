import pytest
from app.services.analyzer import local_analysis
from app.schemas.analysis import AnalysisRequest

def test_urgency_link_and_password_are_flagged():
    result = local_analysis("Sua conta será bloqueada hoje! Clique https://exemplo.invalid e confirme sua senha imediatamente.")
    assert result["classification"] == "alto_risco"
    assert len(result["signals"]) >= 3

def test_clean_text_never_claims_safe():
    result = local_analysis("Olá, tudo bem? Nos vemos amanhã.")
    assert result["classification"] == "poucos_sinais"
    assert "não garante" in result["summary"]

def test_empty_message_rejected():
    with pytest.raises(Exception):
        AnalysisRequest(message="   ")

def test_long_message_rejected():
    with pytest.raises(Exception):
        AnalysisRequest(message="x" * 5001)
