from pydantic_settings import BaseSettings
from sqlalchemy.orm import declarative_base
from passlib.context import CryptContext

DBBaseModel = declarative_base()

class Settings(BaseSettings):
    """
    Configurações de Agendamento (HealthScheduler)
    """
    API_V1_STR: str = '/api/v1'
    DB_URL: str = "sqlite+aiosqlite:///./agendamentos.db"
    
    # Segurança: JWT Token (Expira em 7 dias)
    JWT_SECRET: str = "7d446b3f7f45c7f8f8b89d8f8a8f8d8f" # Em prod, use variável de ambiente
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 

    class Config:
        case_sensitive = True

settings = Settings()
