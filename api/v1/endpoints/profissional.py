from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from core.deps import get_session
from models.models import EspecialidadeModel, ProfissionalModel, UsuarioModel
from schemas.profissional_schema import (
    EspecialidadeCreate, EspecialidadePublic,
    ProfissionalCreate, ProfissionalPublic
)

router = APIRouter()

# --- ESPECIALIDADES ---

@router.post('/especialidades', status_code=status.HTTP_201_CREATED, response_model=EspecialidadePublic)
async def post_especialidade(especialidade: EspecialidadeCreate, db: AsyncSession = Depends(get_session)):
    nova_especialidade = EspecialidadeModel(**especialidade.model_dump())
    db.add(nova_especialidade)
    await db.commit()
    await db.refresh(nova_especialidade)
    return nova_especialidade

@router.get('/especialidades', response_model=List[EspecialidadePublic])
async def get_especialidades(db: AsyncSession = Depends(get_session)):
    query = select(EspecialidadeModel)
    result = await db.execute(query)
    return result.scalars().all()

# --- PROFISSIONAIS ---

@router.post('/profissionais/{usuario_id}', status_code=status.HTTP_201_CREATED, response_model=ProfissionalPublic)
async def post_profissional(usuario_id: int, profissional: ProfissionalCreate, db: AsyncSession = Depends(get_session)):
    # 1. Verificar se o usuário existe e se marcou 'eh_profissional' no cadastro
    query_user = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
    result_user = await db.execute(query_user)
    usuario = result_user.scalar_one_or_none()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    if not usuario.eh_profissional:
        raise HTTPException(status_code=400, detail="Este usuário não está marcado como profissional.")

    # 2. Buscar as especialidades selecionadas
    query_esp = select(EspecialidadeModel).filter(EspecialidadeModel.id.in_(profissional.especialidades_ids))
    result_esp = await db.execute(query_esp)
    especialidades_db = result_esp.scalars().all()

    if not especialidades_db:
        raise HTTPException(status_code=400, detail="Selecione ao menos uma especialidade válida.")

    # 3. Criar o perfil do profissional e associar as especialidades (N:N)
    novo_profissional = ProfissionalModel(
        usuario_id=usuario_id,
        crm_ou_registro=profissional.crm_ou_registro,
        especialidades=especialidades_db # SQLAlchemy cuida da tabela de associação!
    )
    
    db.add(novo_profissional)
    await db.commit()
    
    # Recarregar para trazer os dados completos (selectinload)
    query_final = select(ProfissionalModel).filter(ProfissionalModel.id == novo_profissional.id).options(selectinload(ProfissionalModel.especialidades))
    result_final = await db.execute(query_final)
    return result_final.scalar_one()

@router.get('/profissionais', response_model=List[ProfissionalPublic])
async def get_profissionais(db: AsyncSession = Depends(get_session)):
    # Usamos selectinload para carregar as especialidades relacionadas de forma eficiente
    query = select(ProfissionalModel).options(selectinload(ProfissionalModel.especialidades))
    result = await db.execute(query)
    return result.scalars().all()
