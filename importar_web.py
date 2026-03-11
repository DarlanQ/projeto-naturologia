import mysql.connector
import csv

def carga_inicial():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="caminho6_naturologia",
            password="DQjjkbtkdlle_221279!.",
            database="caminho6_naturologia"
        )
        cur = conn.cursor()

        # Criando a tabela no MySQL (Sintaxe levemente diferente do Postgres)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS plantas_medicinais (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome_popular VARCHAR(255),
                nome_cientifico VARCHAR(255) UNIQUE,
                propriedades TEXT
            )
        """)

        with open('renisus.csv', mode='r', encoding='utf-8') as f:
            leitor = csv.DictReader(f, delimiter=';')
            for linha in leitor:
                sql = "INSERT IGNORE INTO plantas_medicinais (nome_popular, nome_cientifico, propriedades) VALUES (%s, %s, %s)"
                cur.execute(sql, (linha['nome_popular'], linha['nome_cientifico'], linha['propriedades']))
        
        conn.commit()
        print("Carga concluída com sucesso no MySQL!")
    except Exception as e:
        print(f"Erro na carga: {e}")
    finally:
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    carga_inicial()
