from datetime import datetime, timedelta
from typing import Optional, Any, Union
from jose import jwt
from passlib.context import CryptContext
from core.configs import settings

# Contexto para Hashing de Senhas (bcrypt)
# Explicitamos que queremos usar o esquema bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_senha(senha: str, senha_hash: str) -> bool:
    """Verifica se a senha em texto plano confere com o hash"""
    return pwd_context.verify(senha, senha_hash)

def gerar_hash_senha(senha: str) -> str:
    """Gera um hash seguro da senha do usuário"""
    return pwd_context.hash(senha)

def criar_token_acesso(sub: Any) -> str:
    """Gera um token JWT com tempo de expiração de 7 dias"""
    payload = {
        "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        "sub": str(sub) # Normalmente o ID do usuário
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
