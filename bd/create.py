import sqlite3
import os
from pathlib import Path

# Define o caminho do banco de dados
DB_PATH = Path(__file__).parent / "sql" / "servidor.db"
SQL_PATH = Path(__file__).parent / "sql" / "create.sql"

def init_database():
    """Inicializa o banco de dados SQLite com as tabelas e índices"""
    
    # Verifica se o arquivo SQL existe
    if not SQL_PATH.exists():
        print(f"Erro: Arquivo {SQL_PATH} não encontrado!")
        return False
    
    # Lê o SQL do arquivo
    with open(SQL_PATH, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    # Conecta ao banco (cria o arquivo se não existir)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Executa o script SQL completo
        cursor.executescript(sql_script)
        conn.commit()
        print(f"✅ Banco de dados criado com sucesso: {DB_PATH}")
        print("📊 Tabelas: estado, cidade, usuario, jogo, lanHouse, campeonato, agendamento")
        print("🔍 Índices criados com sucesso")
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Erro ao executar SQL: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()

def verificar_tabelas():
    """Verifica se as tabelas foram criadas corretamente"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tabelas = cursor.fetchall()
    
    print("\n📋 Tabelas existentes:")
    for tabela in tabelas:
        # Conta registros em cada tabela
        cursor.execute(f"SELECT COUNT(*) FROM {tabela[0]};")
        count = cursor.fetchone()[0]
        print(f"  - {tabela[0]}: {count} registros")
    
    conn.close()

def mostrar_estrutura():
    """Mostra a estrutura das tabelas principais"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    tabelas_principais = ['usuario', 'lanHouse', 'campeonato', 'jogo']
    
    print("\n🏗️  Estrutura das tabelas principais:")
    for tabela in tabelas_principais:
        cursor.execute(f"PRAGMA table_info({tabela});")
        colunas = cursor.fetchall()
        print(f"\n  Tabela: {tabela}")
        for coluna in colunas:
            print(f"    - {coluna[1]} ({coluna[2]})")
    
    conn.close()

if __name__ == "__main__":
    print("🚀 Iniciando criação do banco de dados Lan House System...")
    print("=" * 50)
    
    # Se o banco já existir, pergunta se quer recriar
    if DB_PATH.exists():
        resposta = input(f"⚠️  Banco {DB_PATH} já existe. Recriar? (s/N): ")
        if resposta.lower() == 's':
            os.remove(DB_PATH)
            print("🗑️  Banco antigo removido.")
            print()
            init_database()
            verificar_tabelas()
            mostrar_estrutura()
        else:
            print("❌ Operação cancelada.")
    else:
        init_database()
        verificar_tabelas()
        mostrar_estrutura()
    
    print("\n✨ Banco de dados pronto para uso!")