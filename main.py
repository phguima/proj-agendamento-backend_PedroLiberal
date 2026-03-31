from fastapi import FastAPI
from core.configs import settings
from api.v1.api import api_router

app = FastAPI(title='HealthScheduler API - Sistema de Agendamentos')

# Registrando as rotas da versão 1
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get('/')
async def root():
    return {"mensagem": "HealthScheduler Online! Acesse /api/v1/auth/login para autenticar."}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, log_level="info", reload=True)
