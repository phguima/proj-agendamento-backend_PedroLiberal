# 🏥 HealthScheduler API - Sistema de Agendamentos

Uma API profissional para gestão de agendamentos de saúde, desenvolvida com **FastAPI**. O sistema permite o cadastro de profissionais, clientes e especialidades, gerenciando conflitos de horários e garantindo a segurança dos dados.

## 🌟 Destaques deste Projeto

- **Segurança Avançada:** Hashing de senhas com `bcrypt` e autenticação via **JWT (JSON Web Tokens)**.
- **Relacionamentos Complexos:** Implementação de relacionamento **Muitos-para-Muitos** entre Profissionais e Especialidades.
- **Lógica de Negócio (Conflict Check):** Validação automática para impedir agendamentos duplicados para o mesmo profissional.
- **Async Stack:** Performance superior utilizando SQLAlchemy Assíncrono e `aiosqlite`.

## 🛠️ Tecnologias Utilizadas

*   **FastAPI:** Framework principal.
*   **SQLAlchemy 2.0:** ORM assíncrono.
*   **Pydantic v2:** Validação e tipagem (incluindo `email-validator`).
*   **Passlib & Jose:** Criptografia e Tokens JWT.
*   **SQLite:** Banco de dados relacional.

## 📂 Estrutura do Projeto

```text
projeto_agendamento/
├── api/            # Roteamento (Usuários, Auth, Saúde, Agendamentos)
├── core/           # Configurações de Segurança e Banco de Dados
├── models/         # Entidades do Banco (User, Profissional, Cliente, etc)
├── schemas/        # Esquemas de Validação e DTOs
├── security/       # Lógica de Hashing e geração de Tokens
├── main.py         # Start da aplicação (Porta 8001)
├── criar_tabelas.py # Inicializador do banco
└── testar_agendamento.sh # Automação de testes de fluxo completo
```

## 🚀 Como Executar

1. **Configurar Ambiente:**
   ```bash
   cd projeto_agendamento
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

## 📖 Documentação

Acesse o Swagger UI em: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

## 🧪 Testes Automatizados

O projeto inclui um script que testa o fluxo completo (Cadastro -> Login -> Perfil -> Agendamento -> Conflito):
```bash
./testar_agendamento.sh
```

---
Desenvolvido por **Pedro Liberal**
