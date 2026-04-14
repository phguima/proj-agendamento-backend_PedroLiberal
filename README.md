# 🏥 HealthScheduler API - Sistema de Agendamentos

Uma API profissional para gestão de agendamentos de saúde, desenvolvida com **FastAPI**. O sistema permite o cadastro de profissionais, clientes e especialidades, gerenciando conflitos de horários e garantindo a segurança dos dados.

## 🌟 Destaques Técnicos

- **Async Stack:** Performance superior utilizando **SQLAlchemy 2.0 (Assíncrono)** e `aiosqlite`.
- **Relacionamentos Complexos:** Implementação de relacionamento **Muitos-para-Muitos (N:N)** entre Profissionais e Especialidades com carregamento eficiente (`selectinload`).
- **Segurança Avançada:** Hashing de senhas com `bcrypt` (via `passlib`) e autenticação via **JWT (JSON Web Tokens)** seguindo o padrão OAuth2.
- **Lógica de Negócio (Conflict Check):** Validação automática para impedir agendamentos duplicados para o mesmo profissional no mesmo horário.
- **Professional Testing Suite:** Testes unitários e de integração assíncronos com **Pytest** e **HTTPX**, utilizando banco de dados em memória para isolamento total.

## 🛠️ Tecnologias Utilizadas

*   **FastAPI:** Framework moderno de alta performance.
*   **SQLAlchemy 2.0:** ORM robusto com suporte total a `async/await`.
*   **Pytest & HTTPX:** Suite de testes assíncronos.
*   **Pydantic v2:** Validação rigorosa de dados e tipagem.
*   **Passlib & Jose:** Criptografia e segurança de tokens.
*   **SQLite (aiosqlite):** Banco de dados relacional leve e assíncrono.

## 📂 Estrutura do Projeto

```text
proj-agendamento-backend_PedroLiberal/
├── api/
│   └── v1/
│       ├── api.py            # Agregador central de rotas da v1
│       └── endpoints/        # Lógica de rotas (Agendamento, Auth, Cliente, Profissional, Usuário)
├── core/
│   ├── configs.py            # Configurações globais e JWT
│   ├── database.py           # Configuração da Engine e Session assíncrona
│   └── deps.py               # Injeção de dependências (Sessão do DB)
├── models/
│   └── models.py             # Entidades do Banco e Tabela de Associação (N:N)
├── schemas/
│   └── ..._schema.py         # Modelos Pydantic para Validação e DTOs
├── security/
│   └── auth.py               # Funções de Hashing e lógica de Token
├── tests/                    # 🧪 Suite de Testes Profissional (Pytest)
│   ├── conftest.py           # Configuração de fixtures e DB em memória
│   └── test_api.py           # Testes de Integração (Fluxo completo, Auth, Conflitos)
├── main.py                   # Ponto de entrada da aplicação (Uvicorn)
├── criar_tabelas.py          # Inicializador do esquema do banco de dados
└── testar_agendamento.sh     # Script legatário de testes rápidos (Bash)
```

## 🚀 Como Executar

1. **Configurar Ambiente:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Inicializar Banco:**
   ```bash
   python criar_tabelas.py
   ```

3. **Rodar Servidor:**
   ```bash
   python main.py
   ```
   O servidor iniciará em `http://127.0.0.1:8001`.

## 📖 Documentação

Acesse o **Swagger UI** interativo em: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

## 🧪 Validação e Testes

### Testes Unitários e de Integração (Recomendado)
A suite de testes utiliza `pytest-asyncio` e um banco SQLite em memória para garantir que os testes não afetem seu banco de dados local.

Para rodar os testes:
```bash
export PYTHONPATH=$PYTHONPATH:.
pytest -v tests/test_api.py
```

### Testes de Fluxo Rápido (Bash)
O script `testar_agendamento.sh` pode ser usado para uma validação rápida contra o servidor rodando em tempo real:
```bash
./testar_agendamento.sh
```

---
Desenvolvido por **Pedro Liberal**
