from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class AgendamentoBase(BaseModel):
    id_profissional: int
    id_cliente: int
    data_hora: datetime
    observacoes: Optional[str] = None

class AgendamentoCreate(AgendamentoBase):
    pass

class AgendamentoPublic(AgendamentoBase):
    id: int
    status: str # 'Agendado', 'Cancelado', 'Concluído'
    
    model_config = ConfigDict(from_attributes=True)
