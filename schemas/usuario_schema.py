from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict

class UsuarioSchemaBase(BaseModel):
    nome: str
    email: EmailStr
    eh_profissional: bool = False

    model_config = ConfigDict(from_attributes=True)

class UsuarioSchemaCreate(UsuarioSchemaBase):
    senha: str

class UsuarioSchemaPublic(UsuarioSchemaBase):
    id: Optional[int] = None

class TokenSchema(BaseModel):
    access_token: str
    token_type: str
