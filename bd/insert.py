import sqlite3
from pathlib import Path

# Define o caminho do banco de dados
DB_PATH = Path(__file__).parent / "sql" / "servidor.db"
SQL_PATH = Path(__file__).parent / "sql" / "insert.sql"

def insert_data():
    """Insere dados de exemplo no banco de dados"""
    
    # Verifica se o banco existe
    if not DB_PATH.exists():
        print(f"❌ Erro: Banco de dados {DB_PATH} não encontrado!")
        print("Execute primeiro o create_db.py")
        return False
    
    # Verifica se o arquivo SQL existe
    if not SQL_PATH.exists():
        print(f"❌ Erro: Arquivo {SQL_PATH} não encontrado!")
        return False
    
    # Lê o SQL do arquivo
    with open(SQL_PATH, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    # Conecta ao banco
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Executa o script SQL completo
        cursor.executescript(sql_script)
        conn.commit()
        print("✅ Dados inseridos com sucesso!")
        
        # Mostra quantidade de registros inseridos
        tabelas = ['estado', 'cidade', 'jogo', 'usuario', 'lanHouse', 'campeonato', 'agendamento']
        print("\n📊 Resumo dos dados inseridos:")
        for tabela in tabelas:
            cursor.execute(f"SELECT COUNT(*) FROM {tabela};")
            count = cursor.fetchone()[0]
            print(f"  - {tabela}: {count} registros")
        
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Erro ao inserir dados: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()

def verificar_dados():
    """Verifica alguns dados inseridos"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("\n🔍 Amostra dos dados inseridos:")
    
    # Mostra alguns usuários
    print("\n  Usuários:")
    cursor.execute("SELECT id, nome, email FROM usuario LIMIT 5;")
    for row in cursor.fetchall():
        print(f"    - {row[0]}: {row[1]} ({row[2]})")
    
    # Mostra algumas lan houses
    print("\n  Lan Houses:")
    cursor.execute("SELECT id, titulo, preco, vagas FROM lanHouse LIMIT 5;")
    for row in cursor.fetchall():
        print(f"    - {row[0]}: {row[1]} - R$ {row[2]:.2f} ({row[3]} vagas)")
    
    # Mostra alguns campeonatos
    print("\n  Campeonatos:")
    cursor.execute("""
        SELECT c.id, j.nome, c.vagas, c.categoria 
        FROM campeonato c 
        JOIN jogo j ON c.jogo = j.id 
        LIMIT 5;
    """)
    for row in cursor.fetchall():
        categoria = ['Amador', 'Semi-Pro', 'Profissional'][row[3]]
        print(f"    - {row[0]}: {row[1]} - {row[2]} vagas ({categoria})")
    
    conn.close()

if __name__ == "__main__":
    print("🚀 Iniciando inserção de dados no banco...")
    print("=" * 50)
    
    resposta = input("⚠️  Isso vai adicionar dados de exemplo. Continuar? (s/N): ")
    if resposta.lower() == 's':
        if insert_data():
            verificar_dados()
            print("\n✨ Dados de exemplo inseridos com sucesso!")
        else:
            print("\n❌ Falha ao inserir dados.")
    else:
        print("❌ Operação cancelada.")