from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from core.configs import DBBaseModel

# Tabela de Associação: Muitos-para-Muitos (Profissional <-> Especialidade)
profissional_especialidade = Table(
    "profissional_especialidade",
    DBBaseModel.metadata,
    Column("id_profissional", Integer, ForeignKey("profissionais.id"), primary_key=True),
    Column("id_especialidade", Integer, ForeignKey("especialidades.id"), primary_key=True)
)

class UsuarioModel(DBBaseModel):
    __tablename__ = 'usuarios'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(100), nullable=False)
    email: str = Column(String(100), unique=True, index=True, nullable=False)
    senha: str = Column(String(100), nullable=False)
    eh_profissional: bool = Column(Boolean, default=False)

class EspecialidadeModel(DBBaseModel):
    __tablename__ = 'especialidades'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(100), unique=True, nullable=False)
    descricao: str = Column(String(255))

class ProfissionalModel(DBBaseModel):
    __tablename__ = 'profissionais'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id: int = Column(Integer, ForeignKey('usuarios.id'))
    crm_ou_registro: str = Column(String(50), unique=True, nullable=False)
    
    # Relacionamento N:N
    especialidades = relationship("EspecialidadeModel", secondary=profissional_especialidade)

class ClienteModel(DBBaseModel):
    __tablename__ = 'clientes'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id: int = Column(Integer, ForeignKey('usuarios.id'))
    cpf: str = Column(String(14), unique=True, nullable=False)
    telefone: str = Column(String(20))

class AgendamentoModel(DBBaseModel):
    __tablename__ = 'agendamentos'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    id_profissional: int = Column(Integer, ForeignKey('profissionais.id'), nullable=False)
    id_cliente: int = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    data_hora: datetime = Column(DateTime, nullable=False)
    status: str = Column(String(20), default="Agendado") # Agendado, Cancelado, Concluído
    observacoes: str = Column(String(255))
