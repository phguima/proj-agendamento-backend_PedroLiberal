from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime

from core.deps import get_session
from models.models import AgendamentoModel, ProfissionalModel, ClienteModel
from schemas.agendamento_schema import AgendamentoCreate, AgendamentoPublic

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=AgendamentoPublic)
async def post_agendamento(agendamento: AgendamentoCreate, db: AsyncSession = Depends(get_session)):
    """
    Realiza um novo agendamento, validando se o Profissional está disponível.
    """
    # 1. Verificar se o Profissional e o Cliente existem
    query_prof = select(ProfissionalModel).filter(ProfissionalModel.id == agendamento.id_profissional)
    result_prof = await db.execute(query_prof)
    if not result_prof.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Profissional não encontrado.")

    query_cli = select(ClienteModel).filter(ClienteModel.id == agendamento.id_cliente)
    result_cli = await db.execute(query_cli)
    if not result_cli.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")

    # 2. REGRA DE NEGÓCIO: Verificar conflito de horário para o Profissional
    query_conflito = select(AgendamentoModel).filter(
        AgendamentoModel.id_profissional == agendamento.id_profissional,
        AgendamentoModel.data_hora == agendamento.data_hora,
        AgendamentoModel.status == "Agendado"
    )
    result_conflito = await db.execute(query_conflito)
    if result_conflito.scalar_one_or_none():
        horario_formatado = agendamento.data_hora.strftime('%d/%m/%Y às %H:%M')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"O profissional já possui um agendamento confirmado para o dia {horario_formatado}."
        )

    # 3. Criar o agendamento
    novo_agendamento = AgendamentoModel(
        id_profissional=agendamento.id_profissional,
        id_cliente=agendamento.id_cliente,
        data_hora=agendamento.data_hora,
        observacoes=agendamento.observacoes
    )
    
    db.add(novo_agendamento)
    await db.commit()
    return novo_agendamento

@router.get('/', response_model=List[AgendamentoPublic])
async def get_agendamentos(db: AsyncSession = Depends(get_session)):
    """Lista todos os agendamentos registrados"""
    query = select(AgendamentoModel)
    result = await db.execute(query)
    return result.scalars().all()

@router.delete('/{agendamento_id}', status_code=status.HTTP_204_NO_CONTENT)
async def cancelar_agendamento(agendamento_id: int, db: AsyncSession = Depends(get_session)):
    """Altera o status do agendamento para Cancelado em vez de deletar fisicamente (Soft Delete parcial)"""
    query = select(AgendamentoModel).filter(AgendamentoModel.id == agendamento_id)
    result = await db.execute(query)
    agendamento = result.scalar_one_or_none()
    
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado.")
    
    agendamento.status = "Cancelado"
    await db.commit()
    return status.HTTP_204_NO_CONTENT
