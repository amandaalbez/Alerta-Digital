from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routes.analysis import router

app = FastAPI(title="Alerta Digital API", version="1.0.0", description="API educativa para análise de mensagens suspeitas.")
app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS, allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["*"])
app.include_router(router)

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "Alerta Digital"}
