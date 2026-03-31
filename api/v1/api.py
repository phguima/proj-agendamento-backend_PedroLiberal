from fastapi import APIRouter
from api.v1.endpoints import usuario, auth, profissional, cliente, agendamento

api_router = APIRouter()
api_router.include_router(usuario.router, prefix='/usuarios', tags=['Usuários'])
api_router.include_router(auth.router, prefix='/auth', tags=['Autenticação'])
api_router.include_router(profissional.router, prefix='/saude', tags=['Profissionais & Especialidades'])
api_router.include_router(cliente.router, prefix='/clientes', tags=['Clientes'])
api_router.include_router(agendamento.router, prefix='/agendamentos', tags=['Agendamentos'])
