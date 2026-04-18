import sqlite3
from prettytable import PrettyTable  # Você precisa instalar: pip install prettytable

def select_all_tables():
    try:
        # Conectar ao banco
        conn = sqlite3.connect('sql/servidor.db')
        cursor = conn.cursor()
        
        # Obter todas as tabelas do banco
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        # Para cada tabela, fazer SELECT *
        for table in tables:
            table_name = table[0]
            
            # Pegar dados da tabela
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            # Pegar nomes das colunas
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in cursor.fetchall()]
            
            # Criar tabela formatada
            print(f"\n📊 Tabela: {table_name}")
            print("-" * 80)
            
            if rows:
                # Criar PrettyTable para melhor formatação
                pt = PrettyTable()
                pt.field_names = columns
                
                for row in rows:
                    pt.add_row(row)
                
                print(pt)
                print(f"Total: {len(rows)} registros")
            else:
                print("Nenhum registro encontrado.")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"Erro no banco de dados: {e}")
    except Exception as e:
        print(f"Erro geral: {e}")

# Executar
if __name__ == "__main__":
    select_all_tables()