# 🎓 Guia de Apresentação: HealthScheduler API

## 1. Introdução
O **HealthScheduler** é uma evolução do CRUD básico. Ele simula um ambiente real de agendamentos médicos onde a integridade dos dados e a segurança são fundamentais.

## 2. Pontos Chave para Destacar

### A. Autenticação e Segurança (JWT)
- **O Desafio:** Como impedir que qualquer pessoa manipule os dados?
- **A Solução:** Implementamos Hashing de senhas com `bcrypt` e autenticação via **JWT**.
- **Validação de E-mail**: Utilizamos `EmailStr` para garantir dados de contato válidos desde a entrada.

### B. Relacionamentos Muitos-para-Muitos (N:N)
- **O Desafio:** Gerenciar médicos com múltiplas especialidades.
- **A Solução:** Uso de uma **Tabela de Associação** gerenciada pelo SQLAlchemy.

### C. Regras de Negócio e Integridade
- **Bloqueio de Conflitos**: A API valida a disponibilidade do profissional antes de confirmar o agendamento.
- **Mensagens Amigáveis**: Em vez de códigos genéricos, a API retorna mensagens detalhadas informando exatamente qual o conflito (ex: data e hora ocupada).
- **Sincronização (`db.refresh`)**: Garantimos que a resposta da API contenha os dados atualizados do banco imediatamente após a persistência.

---

## 3. Diferenciais Técnicos
1. **Assincronismo Total**: Uso de `aiosqlite` e `AsyncSession`.
2. **Documentação Automática**: Swagger UI gerado em tempo real.
3. **Internacionalização (UTF-8)**: Scripts de teste e respostas da API configurados para suportar corretamente acentuação da língua portuguesa.

---

## 4. Demonstração Prática
Durante a apresentação, rode o `./testar_agendamento.sh` para mostrar:
1.  Criação dinâmica de usuários e perfis.
2.  Agendamento bem-sucedido.
3.  **O ponto alto:** O bloqueio automático de um agendamento duplicado.

---
**Apresentação por Pedro Liberal - 2026**
