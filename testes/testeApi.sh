# Válido
curl -X GET "http://localhost:8000/estados" | jq '.'
# Válido
curl -X GET "http://localhost:8000/jogos" | jq '.'
# Inválido
curl -X POST "http://localhost:8000/login?email=joao.silva@email.com&senha=senha_incorreta" | jq '.'
# Inválido
curl -X POST "http://localhost:8000/getContaInfo/9999" | jq '.'