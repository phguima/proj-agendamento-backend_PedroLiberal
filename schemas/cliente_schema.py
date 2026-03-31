from typing import Optional
from pydantic import BaseModel, ConfigDict

class ClienteBase(BaseModel):
    cpf: str
    telefone: str

class ClienteCreate(ClienteBase):
    pass

class ClientePublic(ClienteBase):
    id: int
    usuario_id: int
    model_config = ConfigDict(from_attributes=True)
