from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session
from models.models import ClienteModel, UsuarioModel
from schemas.cliente_schema import ClienteCreate, ClientePublic

router = APIRouter()

@router.post('/{usuario_id}', status_code=status.HTTP_201_CREATED, response_model=ClientePublic)
async def post_cliente(usuario_id: int, cliente: ClienteCreate, db: AsyncSession = Depends(get_session)):
    """
    Registra um usuário como Cliente, adicionando o CPF e Telefone.
    """
    # 1. Verificar se o usuário existe e não é profissional
    query_user = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
    result_user = await db.execute(query_user)
    usuario = result_user.scalar_one_or_none()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    if usuario.eh_profissional:
        raise HTTPException(status_code=400, detail="Profissionais não podem se registrar como clientes.")

    # 2. Verificar se já existe um cliente com esse CPF
    query_cpf = select(ClienteModel).filter(ClienteModel.cpf == cliente.cpf)
    result_cpf = await db.execute(query_cpf)
    if result_cpf.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Este CPF já está cadastrado no sistema.")

    # 3. Criar o perfil de cliente
    novo_cliente = ClienteModel(
        usuario_id=usuario_id,
        cpf=cliente.cpf,
        telefone=cliente.telefone
    )
    
    db.add(novo_cliente)
    await db.commit()
    await db.refresh(novo_cliente)
    return novo_cliente

@router.get('/', response_model=List[ClientePublic])
async def get_clientes(db: AsyncSession = Depends(get_session)):
    query = select(ClienteModel)
    result = await db.execute(query)
    return result.scalars().all()
