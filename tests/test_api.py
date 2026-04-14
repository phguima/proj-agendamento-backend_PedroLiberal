import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_fluxo_completo_agendamento(client: AsyncClient):
    # 1. Cadastrar Usuário Profissional
    response = await client.post("/api/v1/usuarios/signup", json={
        "nome": "Dr. Carlos Silva",
        "email": "dr.silva@hospital.com",
        "senha": "senha_segura_123",
        "eh_profissional": True
    })
    assert response.status_code == 201
    id_user_prof = response.json()["id"]

    # 2. Cadastrar Usuário Cliente
    response = await client.post("/api/v1/usuarios/signup", json={
        "nome": "João da Silva",
        "email": "joao@email.com",
        "senha": "outra_senha_456",
        "eh_profissional": False
    })
    assert response.status_code == 201
    id_user_cli = response.json()["id"]

    # 3. Criar Especialidade
    response = await client.post("/api/v1/saude/especialidades", json={
        "nome": "Cardiologia",
        "descricao": "Saúde do coração"
    })
    assert response.status_code == 201
    id_esp = response.json()["id"]

    # 4. Completar Perfil do Profissional
    response = await client.post(f"/api/v1/saude/profissionais/{id_user_prof}", json={
        "crm_ou_registro": "CRM-SP12345",
        "especialidades_ids": [id_esp]
    })
    assert response.status_code == 201
    id_prof = response.json()["id"]

    # 5. Completar Perfil do Cliente
    response = await client.post(f"/api/v1/clientes/{id_user_cli}", json={
        "cpf": "123.456.789-00",
        "telefone": "11999999999"
    })
    assert response.status_code == 201
    id_cli = response.json()["id"]

    # 6. Realizar Agendamento
    data_consulta = "2026-03-30T10:00:00"
    response = await client.post("/api/v1/agendamentos/", json={
        "id_profissional": id_prof,
        "id_cliente": id_cli,
        "data_hora": data_consulta,
        "observacoes": "Primeira consulta de rotina."
    })
    assert response.status_code == 201
    id_agend = response.json()["id"]

    # 7. Testar Conflito de Horário (Mesmo Horário)
    response = await client.post("/api/v1/agendamentos/", json={
        "id_profissional": id_prof,
        "id_cliente": id_cli,
        "data_hora": data_consulta,
        "observacoes": "Tentativa de agendamento duplicado."
    })
    assert response.status_code == 400
    assert "já possui um agendamento" in response.json()["detail"]

    # 8. Listar Agendamentos
    response = await client.get("/api/v1/agendamentos/")
    assert response.status_code == 200
    assert len(response.json()) >= 1

    # 9. Cancelar Agendamento (Soft Delete)
    response = await client.delete(f"/api/v1/agendamentos/{id_agend}")
    assert response.status_code == 204

    # 10. Verificar Status Final após cancelamento
    response = await client.get("/api/v1/agendamentos/")
    agendamentos = response.json()
    cancelado = next(a for a in agendamentos if a["id"] == id_agend)
    assert cancelado["status"] == "Cancelado"

@pytest.mark.asyncio
async def test_login_sucesso(client: AsyncClient):
    # Garantir que o usuário existe para o login
    await client.post("/api/v1/usuarios/signup", json={
        "nome": "Admin",
        "email": "admin@teste.com",
        "senha": "admin_senha",
        "eh_profissional": False
    })

    # Testar Login (OAuth2 espera form-data)
    response = await client.post("/api/v1/auth/login", data={
        "username": "admin@teste.com",
        "password": "admin_senha"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_falha_senha_errada(client: AsyncClient):
    response = await client.post("/api/v1/auth/login", data={
        "username": "admin@teste.com",
        "password": "senha_errada"
    })
    assert response.status_code == 401
