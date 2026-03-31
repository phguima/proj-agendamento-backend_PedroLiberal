from typing import List, Optional
from pydantic import BaseModel, ConfigDict

# Esquemas para Especialidade
class EspecialidadeBase(BaseModel):
    nome: str
    descricao: Optional[str] = None

class EspecialidadeCreate(EspecialidadeBase):
    pass

class EspecialidadePublic(EspecialidadeBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# Esquemas para Profissional
class ProfissionalBase(BaseModel):
    crm_ou_registro: str

class ProfissionalCreate(ProfissionalBase):
    especialidades_ids: List[int] # Lista de IDs das especialidades que ele possui

class ProfissionalPublic(ProfissionalBase):
    id: int
    usuario_id: int
    especialidades: List[EspecialidadePublic] # Retorna os objetos completos
    model_config = ConfigDict(from_attributes=True)
