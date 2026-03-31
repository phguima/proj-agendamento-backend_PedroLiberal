from typing import AsyncGenerator, Optional
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.database import Session
from core.configs import settings

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Sessão assíncrona para o banco de dados"""
    async with Session() as session:
        yield session

# Futuramente: get_current_user para proteger as rotas
# async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_session)) -> Usuario:
#     ...
