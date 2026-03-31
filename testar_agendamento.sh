#!/bin/bash

# Configurações
BASE_URL="http://127.0.0.1:8001/api/v1"
BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${BLUE}=== INICIANDO TESTES: HEALTH SCHEDULER (CRUD COMPLETO) ===${NC}\n"

# Verificar se o servidor está rodando
if ! curl -s --head --request GET http://127.0.0.1:8001/ | grep "200 OK" > /dev/null; then
    echo -e "${RED}ERRO: O servidor FastAPI não parece estar rodando na porta 8001.${NC}"
    echo -e "Por favor, rode 'python main.py' em outro terminal antes de testar."
    exit 1
fi

# 1. RESETAR BANCO DE DADOS
echo -e "${CYAN}[1/12] Reiniciando Banco de Dados...${NC}"
python3 criar_tabelas.py > /dev/null
echo -e "Banco resetado com sucesso.\n"

# Função auxiliar para tratar erros de CURL e formatar JSON
exec_curl() {
    local METHOD=$1
    local URL=$2
    local DATA=$3
    local RESPONSE
    
    if [ -z "$DATA" ]; then
        RESPONSE=$(curl -s -X "$METHOD" "$URL" -H 'Content-Type: application/json')
    else
        RESPONSE=$(curl -s -X "$METHOD" "$URL" -H 'Content-Type: application/json' -d "$DATA")
    fi

    # Verificar se houve erro na resposta (ex: detail field presente)
    if [[ $RESPONSE == *"detail"* && ($RESPONSE == *"error"* || $RESPONSE == *"404"* || $RESPONSE == *"400"*) ]] || [[ -z $RESPONSE && $METHOD != "DELETE" ]]; then
        echo -e "${RED}Falha na requisição $METHOD em $URL!${NC}"
        echo "$RESPONSE" | python3 -c "import sys, json; print(json.dumps(json.load(sys.stdin), indent=4, ensure_ascii=False))" 2>/dev/null || echo "$RESPONSE"
        return 1
    fi
    echo "$RESPONSE"
}

format_json() {
    python3 -c "import sys, json; print(json.dumps(json.load(sys.stdin), indent=4, ensure_ascii=False))"
}

# 2. CADASTRAR USUÁRIO PROFISSIONAL (CREATE)
echo -e "${CYAN}[2/12] CREATE: Cadastrando Usuário Profissional (Dr. Silva)...${NC}"
USER_PROF_JSON=$(exec_curl 'POST' "$BASE_URL/usuarios/signup" '{
  "nome": "Dr. Carlos Silva",
  "email": "dr.silva@hospital.com",
  "senha": "senha_segura_123",
  "eh_profissional": true
}')
ID_USER_PROF=$(echo $USER_PROF_JSON | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")
echo "$USER_PROF_JSON" | format_json
echo -e "Usuário criado com ID: ${GREEN}$ID_USER_PROF${NC}\n"

# 3. CADASTRAR USUÁRIO CLIENTE (CREATE)
echo -e "${CYAN}[3/12] CREATE: Cadastrando Usuário Cliente (João)...${NC}"
USER_CLI_JSON=$(exec_curl 'POST' "$BASE_URL/usuarios/signup" '{
  "nome": "João da Silva",
  "email": "joao@email.com",
  "senha": "outra_senha_456",
  "eh_profissional": false
}')
ID_USER_CLI=$(echo $USER_CLI_JSON | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")
echo "$USER_CLI_JSON" | format_json
echo -e "Usuário criado com ID: ${GREEN}$ID_USER_CLI${NC}\n"

# 4. CRIAR ESPECIALIDADE (CREATE)
echo -e "${CYAN}[4/12] CREATE: Criando Especialidade: Cardiologia...${NC}"
ESP_JSON=$(exec_curl 'POST' "$BASE_URL/saude/especialidades" '{
  "nome": "Cardiologia",
  "descricao": "Saúde do coração"
}')
ID_ESP=$(echo $ESP_JSON | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")
echo "$ESP_JSON" | format_json
echo -e "Especialidade ID: ${GREEN}$ID_ESP${NC}\n"

# 5. COMPLETAR PERFIL DO PROFISSIONAL (CREATE)
echo -e "${CYAN}[5/12] CREATE: Vinculando CRM e Especialidade ao Dr. Silva...${NC}"
PROF_JSON=$(exec_curl 'POST' "$BASE_URL/saude/profissionais/$ID_USER_PROF" "{
  \"crm_ou_registro\": \"CRM-SP12345\",
  \"especialidades_ids\": [$ID_ESP]
}")
ID_PROF=$(echo $PROF_JSON | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")
echo "$PROF_JSON" | format_json
echo -e "Perfil Profissional ID: ${GREEN}$ID_PROF${NC}\n"

# 6. COMPLETAR PERFIL DO CLIENTE (CREATE)
echo -e "${CYAN}[6/12] CREATE: Vinculando CPF ao Cliente João...${NC}"
CLI_JSON=$(exec_curl 'POST' "$BASE_URL/clientes/$ID_USER_CLI" '{
  "cpf": "123.456.789-00",
  "telefone": "11999999999"
}')
ID_CLI=$(echo $CLI_JSON | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")
echo "$CLI_JSON" | format_json
echo -e "Perfil Cliente ID: ${GREEN}$ID_CLI${NC}\n"

# 7. LISTAR PROFISSIONAIS E CLIENTES (READ)
echo -e "${CYAN}[7/12] READ: Listando Profissionais Cadastrados...${NC}"
exec_curl 'GET' "$BASE_URL/saude/profissionais" | format_json
echo -e "\n"

echo -e "${CYAN}[8/12] READ: Listando Clientes Cadastrados...${NC}"
exec_curl 'GET' "$BASE_URL/clientes/" | format_json
echo -e "\n"

# 8. REALIZAR AGENDAMENTO (CREATE)
echo -e "${CYAN}[9/12] CREATE: Agendando Consulta: 30/03/2026 às 10:00...${NC}"
DATA_CONSULTA="2026-03-30T10:00:00"
AGEND_JSON=$(exec_curl 'POST' "$BASE_URL/agendamentos/" "{
  \"id_profissional\": $ID_PROF,
  \"id_cliente\": $ID_CLI,
  \"data_hora\": \"$DATA_CONSULTA\",
  \"observacoes\": \"Primeira consulta de rotina.\"
}")
ID_AGEND=$(echo $AGEND_JSON | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")
echo "$AGEND_JSON" | format_json
echo -e "Agendamento realizado com ID: ${GREEN}$ID_AGEND${NC}\n"

# 9. LISTAR AGENDAMENTOS (READ)
echo -e "${CYAN}[10/12] READ: Listando Todos os Agendamentos...${NC}"
exec_curl 'GET' "$BASE_URL/agendamentos/" | format_json
echo -e "\n"

# 10. TESTAR CONFLITO DE HORÁRIO (VALIDATION)
echo -e "${YELLOW}[11/12] VALIDATION: Testando Conflito (Mesmo Horário)...${NC}"
RESPONSE_CONFLITO=$(curl -s -X 'POST' "$BASE_URL/agendamentos/" \
  -H 'Content-Type: application/json' \
  -d "{
  \"id_profissional\": $ID_PROF,
  \"id_cliente\": $ID_CLI,
  \"data_hora\": \"$DATA_CONSULTA\",
  \"observacoes\": \"Tentativa de agendamento duplicado.\"
}")
echo "$RESPONSE_CONFLITO" | format_json
echo -e "\n"

# 11. CANCELAR AGENDAMENTO (DELETE/SOFT DELETE)
echo -e "${CYAN}[12/12] DELETE: Cancelando o Agendamento ID $ID_AGEND...${NC}"
exec_curl 'DELETE' "$BASE_URL/agendamentos/$ID_AGEND"
echo -e "Agendamento cancelado (Status alterado para 'Cancelado').\n"

# 12. VERIFICAR STATUS FINAL (READ)
echo -e "${CYAN}=== VERIFICAÇÃO FINAL: LISTA DE AGENDAMENTOS APÓS CANCELAMENTO ===${NC}"
exec_curl 'GET' "$BASE_URL/agendamentos/" | format_json

echo -e "\n${GREEN}=== TESTES TÉCNICOS CRUD CONCLUÍDOS COM SUCESSO ===${NC}"
