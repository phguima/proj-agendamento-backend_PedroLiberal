from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session
from models.models import UsuarioModel
from security.auth import verificar_senha, criar_token_acesso
from schemas.usuario_schema import TokenSchema

router = APIRouter()

@router.post('/login', response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    # Buscar usuário pelo e-mail (username no padrão OAuth2)
    query = select(UsuarioModel).filter(UsuarioModel.email == form_data.username)
    result = await db.execute(query)
    usuario = result.scalar_one_or_none()
    
    # Validar existência e senha
    if not usuario or not verificar_senha(form_data.password, usuario.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Gerar Token JWT com o ID do usuário (sub)
    token = criar_token_acesso(sub=usuario.id)
    return {"access_token": token, "token_type": "bearer"}
