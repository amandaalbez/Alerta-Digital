import json
import re
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from app.core.config import settings

RULES = [
    ("urgência exagerada", [r"\bagora\b", r"\bimediatamente\b", r"\bhoje\b", r"\búltima chance\b", r"\burgente\b"], "A pressão para agir rapidamente pode impedir que você confira a informação com calma."),
    ("ameaça de bloqueio ou cancelamento", [r"\bbloquead[oa]\b", r"\bcancelad[oa]\b", r"\bsuspens[oa]\b", r"\bserá encerrad[oa]\b"], "Golpistas podem usar ameaças para provocar medo e induzir uma ação precipitada."),
    ("pedido de pagamento", [r"\bpague\b", r"\btaxa\b", r"\bpix\b", r"\btransfer[êe]ncia\b", r"\b boleto\b", r"\b pagamento\b"], "Cobranças inesperadas devem ser verificadas diretamente no canal oficial."),
    ("promessa de prêmio ou vantagem", [r"\bganhou\b", r"\bprêmio\b", r"\bsorteio\b", r"\bgrátis\b", r"\bdesconto de \d{2,}%"], "Prêmios inesperados e vantagens muito grandes podem ser usados como isca."),
    ("pedido de senha ou código", [r"\bsenha\b", r"\bcódigo\b", r"\btoken\b", r"\bautenticação\b", r"\bconfirme seus dados\b"], "Senhas e códigos de autenticação não devem ser compartilhados por mensagem."),
    ("link ou endereço eletrônico", [r"https?://", r"\bwww\.", r"\bbit\.ly\b", r"\btinyurl\b"], "Links recebidos podem levar a páginas falsas. Não abra; confira o endereço por um canal oficial."),
    ("solicitação de dados pessoais", [r"\bcpf\b", r"\bdados pessoais\b", r"\bnúmero do cartão\b", r"\bdocumento\b"], "Evite fornecer dados pessoais em links ou conversas não verificadas."),
    ("pedido incomum de dinheiro", [r"\bnovo número\b", r"\bme empresta\b", r"\bmanda um pix\b", r"\bpreciso de dinheiro\b"], "Confirme pedidos de dinheiro com a pessoa por uma ligação ou canal que você já conhece."),
]
def local_analysis(message: str) -> dict:
    text = message.lower()
    found = []
    for title, patterns, explanation in RULES:
        if any(re.search(p, text, re.IGNORECASE) for p in patterns):
            found.append({"title": title.capitalize(), "explanation": explanation})
    score = min(100, len(found) * 18)
    if score >= 54:
        classification = "alto_risco"
        summary = "A mensagem reúne vários sinais de alerta. Não realize pagamentos nem informe dados antes de verificar."
    elif score >= 18:
        classification = "atencao"
        summary = "Há elementos que merecem atenção. Confira a informação diretamente com a instituição ou pessoa envolvida."
    else:
        classification = "poucos_sinais"
        summary = "Foram identificados poucos indicadores nesta análise. Isso não garante que a mensagem seja legítima."
    advice = "Não clique em links nem faça pagamentos. Abra o aplicativo ou site oficial digitando o endereço, ou confirme por outro canal conhecido."
    if not found:
        found = [{"title": "Nenhum indicador evidente encontrado", "explanation": "A análise automática não identificou os padrões avaliados. Golpes também podem usar mensagens bem escritas e personalizadas."}]
    return {"classification": classification, "score": score, "summary": summary, "signals": found, "advice": advice,
            "source": "regras locais", "disclaimer": "Indicador educativo, não é probabilidade estatística nem confirmação de fraude."}

def ai_analysis(message: str) -> dict:
    prompt = (
        "Analise somente os sinais presentes no texto fornecido. Não invente fatos e não declare fraude confirmada "
        "sem evidências. Use linguagem simples. Retorne somente JSON com classification (alto_risco, atencao ou poucos_sinais), "
        "score (0 a 100 como indicador educativo), summary, signals (array de title e explanation) e advice. "
        "Poucos sinais nunca significa segurança garantida."
    )
    payload = {"model": settings.AI_MODEL, "temperature": 0.1, "messages": [
        {"role": "system", "content": prompt},
        {"role": "user", "content": message}
    ], "response_format": {"type": "json_object"}}
    req = Request(settings.AI_BASE_URL + "/chat/completions", data=json.dumps(payload).encode(),
                  headers={"Content-Type": "application/json", "Authorization": f"Bearer {settings.AI_API_KEY}"}, method="POST")
    with urlopen(req, timeout=18) as response:
        result = json.loads(response.read().decode())
    content = result["choices"][0]["message"]["content"]
    data = json.loads(content)
    if data.get("classification") not in {"alto_risco", "atencao", "poucos_sinais"}:
        raise ValueError("Classificação inválida")
    data["score"] = max(0, min(100, int(data.get("score", 0))))
    data["source"] = "modelo de IA externo"
    data["disclaimer"] = "Análise automatizada educativa. Pode cometer erros e não confirma fraude."
    data["signals"] = data.get("signals", [])[:10]
    return data

def analyze(message: str) -> dict:
    if settings.AI_PROVIDER == "openai_compatible" and settings.AI_API_KEY:
        try:
            return ai_analysis(message)
        except (URLError, HTTPError, TimeoutError, ValueError, KeyError, json.JSONDecodeError):
            result = local_analysis(message)
            result["source"] = "regras locais (IA externa indisponível)"
            return result
    return local_analysis(message)
