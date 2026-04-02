#!/bin/bash

BASE_URL="http://localhost:8000"

# Função para formatar JSON
format_json() {
    python3 -m json.tool 2>/dev/null || jq '.' 2>/dev/null || cat
}

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           TESTES DA API - LAN HOUSE SYSTEM                  ║"
echo "╚══════════════════════════════════════════════════════════════╝"

# Health check
echo
echo "HEALTH CHECK"
echo "═══════════════════════════════════════════════════════════════"
curl -s "$BASE_URL/health" | format_json
echo

# Estados
echo
echo "ESTADOS"
echo "═══════════════════════════════════════════════════════════════"
curl -s "$BASE_URL/estados" | format_json
echo

# Cidades (todas)
echo
echo "CIDADES (Todas)"
echo "═══════════════════════════════════════════════════════════════"
curl -s "$BASE_URL/cidades" | format_json
echo

# Cidades filtradas por estado (SP - id=1)
echo
echo "CIDADES - São Paulo (estado_id=1)"
echo "═══════════════════════════════════════════════════════════════"
curl -s "$BASE_URL/cidades?estado_id=1" | format_json
echo

# Jogos
echo
echo "JOGOS"
echo "═══════════════════════════════════════════════════════════════"
curl -s "$BASE_URL/jogos" | format_json
echo

# Lan Houses - Sem filtros
echo
echo "LAN HOUSES - Todas"
echo "═══════════════════════════════════════════════════════════════"
curl -s "$BASE_URL/lanhouses" | format_json
echo

# Lan Houses - Com filtros (tipo=3, preço entre 10 e 15)
echo
echo "LAN HOUSES - Filtradas (tipo=3, preço R$10-R$15)"
echo "═══════════════════════════════════════════════════════════════"
curl -s "$BASE_URL/lanhouses?tipo=3&precoMinimo=10&precoMaximo=15" | format_json
echo

# Lan Houses - Com filtros (tipo=1)
echo
echo "LAN HOUSES - Tipo 1 (Familiar)"
echo "═══════════════════════════════════════════════════════════════"
curl -s "$BASE_URL/lanhouses?tipo=1" | format_json
echo

# Lan Houses - Com filtros (preço mínimo 12)
echo
echo "LAN HOUSES - Preço mínimo R$12"
echo "═══════════════════════════════════════════════════════════════"
curl -s "$BASE_URL/lanhouses?precoMinimo=12" | format_json
echo

# Campeonatos - Sem filtros
echo
echo "CAMPEONATOS - Todos"
echo "═══════════════════════════════════════════════════════════════"
curl -s "$BASE_URL/comps" | format_json
echo

# Campeonatos - Filtrados (tipo=2 profissional, jogo=1 LoL)
echo
echo "CAMPEONATOS - Profissionais de League of Legends"
echo "═══════════════════════════════════════════════════════════════"
curl -s "$BASE_URL/comps?tipo=2&jogo=1" | format_json
echo

# Campeonatos - Filtrados (jogo=2 CS2)
echo
echo "CAMPEONATOS - Counter-Strike 2"
echo "═══════════════════════════════════════════════════════════════"
curl -s "$BASE_URL/comps?jogo=2" | format_json
echo

# Campeonatos - Filtrados (tipo=0 amador)
echo
echo "CAMPEONATOS - Amadores"
echo "═══════════════════════════════════════════════════════════════"
curl -s "$BASE_URL/comps?tipo=0" | format_json
echo

# Detalhes de Lan House específica (ID 1)
echo
echo "DETALHES - Lan House ID 1"
echo "═══════════════════════════════════════════════════════════════"
curl -s "$BASE_URL/lanhouses/1" | format_json
echo

# Detalhes de Lan House específica (ID 2)
echo
echo "DETALHES - Lan House ID 2"
echo "═══════════════════════════════════════════════════════════════"
curl -s "$BASE_URL/lanhouses/2" | format_json
echo

# Detalhes de Campeonato específico (ID 1)
echo
echo "DETALHES - Campeonato ID 1"
echo "═══════════════════════════════════════════════════════════════"
curl -s "$BASE_URL/comps/1" | format_json
echo

# Detalhes de Campeonato específico (ID 2)
echo
echo "DETALHES - Campeonato ID 2"
echo "═══════════════════════════════════════════════════════════════"
curl -s "$BASE_URL/comps/2" | format_json
echo

# Teste de Login (com usuário de teste)
echo
echo "LOGIN - Usuário Teste"
echo "═══════════════════════════════════════════════════════════════"

# Primeiro, vamos criar um usuário de teste se não existir
python3 << EOF
import sqlite3
from pathlib import Path

DB_PATH = Path("sqlite/servidor.db")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Criar usuário de teste com senha simples
try:
    cursor.execute("""
        INSERT OR REPLACE INTO usuario (id, email, senha, nome, telefone, cpf, bloqueado, apagado)
        VALUES (99, 'teste@email.com', '123456', 'Usuário Teste', '11999999999', '999.999.999-99', 0, 0)
    """)
    conn.commit()
    print("Usuário de teste criado: teste@email.com / 123456")
except Exception as e:
    print(f"Usuário já existe ou erro: {e}")
finally:
    conn.close()
EOF

echo
curl -s -X POST "$BASE_URL/login?email=teste@email.com&senha=123456" | format_json
echo

# Informações completas do usuário de teste
echo
echo "INFORMAÇÕES COMPLETAS - Usuário ID 99"
echo "═══════════════════════════════════════════════════════════════"
curl -s -X POST "$BASE_URL/getContaInfo/99" | format_json
echo

# Informações completas do usuário 1
echo
echo "INFORMAÇÕES COMPLETAS - Usuário ID 1"
echo "═══════════════════════════════════════════════════════════════"
curl -s -X POST "$BASE_URL/getContaInfo/1" | format_json
echo

echo
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    TESTES CONCLUÍDOS!                        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo
echo "Dica: Acesse a documentação interativa: http://localhost:8000/docs"
echo "Para ver o JSON formatado, use | python3 -m json.tool"
echo