# api.py
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from pathlib import Path
from typing import Optional
from contextlib import contextmanager

app = FastAPI(title="Lan House System API", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Caminho do banco de dados
DB_PATH = Path(__file__).parent / "sql" / "servidor.db"

@contextmanager
def get_db():
    """Gerenciador de conexão com o banco de dados"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
    try:
        yield conn
    finally:
        conn.close()

# ==================== ENDPOINTS ====================

@app.post("/login")
def login(email: str, senha: str):
    """
    Login do usuário
    Retorna o id do usuário se email e senha estiverem corretos
    """
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Busca o usuário pelo email
        cursor.execute(
            "SELECT id, senha FROM usuario WHERE email = ? AND apagado = 0",
            (email,)
        )
        user = cursor.fetchone()
        
        if not user:
            raise HTTPException(status_code=401, detail="Email não encontrado")
        
        # Em produção, use bcrypt para comparar a senha
        # Por enquanto, comparando texto puro (para teste)
        if senha != user["senha"]:
            raise HTTPException(status_code=401, detail="Senha incorreta")
        
        return {"id": user["id"], "message": "Login realizado com sucesso"}

@app.post("/getContaInfo/{user_id}")
def get_conta_info(user_id: int):
    """
    Retorna todas as informações do usuário, incluindo:
    - Dados pessoais
    - Lan houses do usuário
    - Campeonatos do usuário
    - Agendamentos do usuário
    """
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Busca dados do usuário
        cursor.execute("""
            SELECT u.*, e.nome as estado_nome, c.nome as cidade_nome
            FROM usuario u
            LEFT JOIN estado e ON u.localidadeEstado = e.id
            LEFT JOIN cidade c ON u.localidadeCidade = c.id
            WHERE u.id = ? AND u.apagado = 0
        """, (user_id,))
        
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        # Converte o usuário para dicionário
        user_data = dict(user)
        
        # Busca lan houses do usuário
        cursor.execute("""
            SELECT * FROM lanHouse
            WHERE usuario = ?
        """, (user_id,))
        
        lan_houses = [dict(row) for row in cursor.fetchall()]
        user_data["lan_houses"] = lan_houses
        
        # Busca campeonatos do usuário
        cursor.execute("""
            SELECT c.*, j.nome as jogo_nome
            FROM campeonato c
            JOIN jogo j ON c.jogo = j.id
            WHERE c.usuario = ?
        """, (user_id,))
        
        campeonatos = [dict(row) for row in cursor.fetchall()]
        user_data["campeonatos"] = campeonatos
        
        # Busca agendamentos do usuário
        cursor.execute("""
            SELECT a.*, c.titulo as campeonato_titulo, j.nome as jogo_nome
            FROM agendamento a
            JOIN campeonato c ON a.campeonato = c.id
            JOIN jogo j ON c.jogo = j.id
            WHERE a.usuario = ?
            ORDER BY a.dataCriacao DESC
        """, (user_id,))
        
        agendamentos = [dict(row) for row in cursor.fetchall()]
        user_data["agendamentos"] = agendamentos
        
        # Remove a senha por segurança
        if "senha" in user_data:
            del user_data["senha"]
        
        return user_data

# Atualizar perfil do usuário
@app.put("/usuarios/{user_id}")
def atualizar_usuario(user_id: int, nome: str, localidadeEstado: int, localidadeCidade: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE usuario 
            SET nome = ?, localidadeEstado = ?, localidadeCidade = ?
            WHERE id = ?
        """, (nome, localidadeEstado, localidadeCidade, user_id))
        conn.commit()
        return {"message": "Usuário atualizado com sucesso"}

# Criar lan house
@app.post("/lanhouses")
def criar_lan_house(nome: str, descricao: str, preco: float, tipoPublico: int, usuario: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO lanHouse (nome, descricao, preco, tipoPublico, usuario)
            VALUES (?, ?, ?, ?, ?)
        """, (nome, descricao, preco, tipoPublico, usuario))
        conn.commit()
        return {"id": cursor.lastrowid, "message": "Lan house criada com sucesso"}

# Deletar lan house
@app.delete("/lanhouses/{lanhouse_id}")
def deletar_lan_house(lanhouse_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM lanHouse WHERE id = ?", (lanhouse_id,))
        conn.commit()
        return {"message": "Lan house deletada com sucesso"}

# Deletar usuário (soft delete)
@app.delete("/usuarios/{user_id}")
def deletar_usuario(user_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE usuario SET apagado = 1 WHERE id = ?", (user_id,))
        conn.commit()
        return {"message": "Usuário deletado com sucesso"}

@app.get("/estados")
def get_estados():
    """
    Retorna todos os estados
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM estado ORDER BY nome")
        estados = [dict(row) for row in cursor.fetchall()]
        return {"estados": estados}

@app.get("/cidades")
def get_cidades(estado_id: Optional[int] = Query(None, description="Filtrar por estado")):
    """
    Retorna todas as cidades
    Se estado_id for informado, filtra por estado
    """
    with get_db() as conn:
        cursor = conn.cursor()
        
        if estado_id:
            cursor.execute("""
                SELECT c.id, c.nome, e.nome as estado_nome
                FROM cidade c
                LEFT JOIN estado e ON c.estado_id = e.id
                WHERE c.estado_id = ?
                ORDER BY c.nome
            """, (estado_id,))
        else:
            cursor.execute("""
                SELECT c.id, c.nome, e.nome as estado_nome
                FROM cidade c
                LEFT JOIN estado e ON c.estado_id = e.id
                ORDER BY c.nome
            """)
        
        cidades = [dict(row) for row in cursor.fetchall()]
        return {"cidades": cidades}

@app.get("/jogos")
def get_jogos():
    """
    Retorna todos os jogos com seus IDs
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM jogo ORDER BY nome")
        jogos = [dict(row) for row in cursor.fetchall()]
        return {"jogos": jogos}

@app.get("/lanhouses")
def get_lan_houses(
    tipo: Optional[int] = Query(None, description="Tipo de público (0-4)"),
    precoMinimo: Optional[float] = Query(None, description="Preço mínimo"),
    precoMaximo: Optional[float] = Query(None, description="Preço máximo")
):
    """
    Retorna lan houses filtradas por:
    - tipo: tipo de público (0 a 4)
    - precoMinimo: preço mínimo
    - precoMaximo: preço máximo
    Se não informar o parâmetro, busca todos
    """
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Monta a query dinamicamente
        query = """
            SELECT l.*, u.nome as usuario_nome
            FROM lanHouse l
            JOIN usuario u ON l.usuario = u.id
            WHERE 1=1
        """
        params = []
        
        if tipo is not None:
            query += " AND l.tipoPublico = ?"
            params.append(tipo)
        
        if precoMinimo is not None:
            query += " AND l.preco >= ?"
            params.append(precoMinimo)
        
        if precoMaximo is not None:
            query += " AND l.preco <= ?"
            params.append(precoMaximo)
        
        query += " ORDER BY l.preco ASC"
        
        cursor.execute(query, params)
        lan_houses = [dict(row) for row in cursor.fetchall()]
        
        return {"lan_houses": lan_houses, "total": len(lan_houses)}

@app.get("/comps")
def get_campeonatos(
    tipo: Optional[int] = Query(None, description="Tipo de categoria (0-2)"),
    jogo: Optional[int] = Query(None, description="ID do jogo")
):
    """
    Retorna campeonatos filtrados por:
    - tipo: categoria (0=Amador, 1=Semi-Pro, 2=Profissional)
    - jogo: ID do jogo
    Se não informar o parâmetro, busca todos
    """
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Monta a query dinamicamente
        query = """
            SELECT c.*, 
                   u.nome as usuario_nome,
                   j.nome as jogo_nome,
                   (SELECT COUNT(*) FROM agendamento WHERE campeonato = c.id) as inscritos
            FROM campeonato c
            JOIN usuario u ON c.usuario = u.id
            JOIN jogo j ON c.jogo = j.id
            WHERE 1=1
        """
        params = []
        
        if tipo is not None:
            query += " AND c.categoria = ?"
            params.append(tipo)
        
        if jogo is not None:
            query += " AND c.jogo = ?"
            params.append(jogo)
        
        query += " ORDER BY c.id DESC"
        
        cursor.execute(query, params)
        campeonatos = [dict(row) for row in cursor.fetchall()]
        
        # Adiciona texto descritivo para categoria
        for comp in campeonatos:
            categoria_texto = {0: "Amador", 1: "Semi-Pro", 2: "Profissional"}.get(comp["categoria"], "Desconhecido")
            comp["categoria_texto"] = categoria_texto
            comp["vagas_disponiveis"] = comp["vagas"] - comp["inscritos"]
        
        return {"campeonatos": campeonatos, "total": len(campeonatos)}

@app.get("/lanhouses/{lanhouse_id}")
def get_lan_house_details(lanhouse_id: int):
    """
    Retorna detalhes de uma lan house específica
    """
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT l.*, u.nome as usuario_nome, u.email as usuario_email
            FROM lanHouse l
            JOIN usuario u ON l.usuario = u.id
            WHERE l.id = ?
        """, (lanhouse_id,))
        
        lan_house = cursor.fetchone()
        if not lan_house:
            raise HTTPException(status_code=404, detail="Lan house não encontrada")
        
        return dict(lan_house)

@app.get("/comps/{comp_id}")
def get_comp_details(comp_id: int):
    """
    Retorna detalhes de um campeonato específico
    """
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT c.*, 
                   u.nome as usuario_nome,
                   u.email as usuario_email,
                   j.nome as jogo_nome,
                   (SELECT COUNT(*) FROM agendamento WHERE campeonato = c.id) as inscritos
            FROM campeonato c
            JOIN usuario u ON c.usuario = u.id
            JOIN jogo j ON c.jogo = j.id
            WHERE c.id = ?
        """, (comp_id,))
        
        comp = cursor.fetchone()
        if not comp:
            raise HTTPException(status_code=404, detail="Campeonato não encontrado")
        
        comp_dict = dict(comp)
        categoria_texto = {0: "Amador", 1: "Semi-Pro", 2: "Profissional"}.get(comp_dict["categoria"], "Desconhecido")
        comp_dict["categoria_texto"] = categoria_texto
        comp_dict["vagas_disponiveis"] = comp_dict["vagas"] - comp_dict["inscritos"]
        
        # Busca participantes do campeonato
        cursor.execute("""
            SELECT u.id, u.nome, u.email, a.dataCriacao
            FROM agendamento a
            JOIN usuario u ON a.usuario = u.id
            WHERE a.campeonato = ?
            ORDER BY a.dataCriacao ASC
        """, (comp_id,))
        
        participantes = [dict(row) for row in cursor.fetchall()]
        comp_dict["participantes"] = participantes
        
        return comp_dict

@app.post("/usuarios")
def criar_usuario(nome: str, email: str, senha: str, localidadeEstado: int, localidadeCidade: int):
    with get_db() as conn:
        cursor = conn.cursor()
        # Verificar se email já existe
        cursor.execute("SELECT id FROM usuario WHERE email = ?", (email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Email já cadastrado")
        
        # Inserir novo usuário
        cursor.execute("""
            INSERT INTO usuario (nome, email, senha, localidadeEstado, localidadeCidade, apagado)
            VALUES (?, ?, ?, ?, ?, 0)
        """, (nome, email, senha, localidadeEstado, localidadeCidade))
        conn.commit()
        
        return {"id": cursor.lastrowid, "message": "Usuário criado com sucesso"}

@app.get("/health")
def health_check():
    """Verifica se a API está funcionando"""
    return {"status": "online", "database": DB_PATH.exists()}

# ==================== INICIALIZAÇÃO ====================
if __name__ == "__main__":
    import uvicorn
    # Executar sem reload para evitar o warning
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)