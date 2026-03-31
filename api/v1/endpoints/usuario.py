from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.models import UsuarioModel
from schemas.usuario_schema import UsuarioSchemaCreate, UsuarioSchemaPublic
from core.deps import get_session
from security.auth import gerar_hash_senha

router = APIRouter()

@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaPublic)
async def post_usuario(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)):
    # Verificar se o e-mail já existe
    query = select(UsuarioModel).filter(UsuarioModel.email == usuario.email)
    result = await db.execute(query)
    usuario_existente = result.scalar_one_or_none()
    
    if usuario_existente:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="E-mail já cadastrado.")

    novo_usuario = UsuarioModel(
        nome=usuario.nome,
        email=usuario.email,
        senha=gerar_hash_senha(usuario.senha), # Criptografia!
        eh_profissional=usuario.eh_profissional
    )
    
    db.add(novo_usuario)
    await db.commit()
    await db.refresh(novo_usuario)
    return novo_usuario
