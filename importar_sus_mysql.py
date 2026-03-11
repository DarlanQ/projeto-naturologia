import mysql.connector
import csv

def importar_para_mysql():
    try:
        # Troque pelos dados que você criar no seu DirectAdmin
        conn = mysql.connector.connect(
            host="localhost",
            user="caminho6_naturologia",
            password="DQjjkbtkdlle_221279!.",
            database="caminho6_naturologia"
        )
        cur = conn.cursor()

        # No MySQL, usamos 'TEXT' ou 'LONGTEXT' para propriedades
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
                sql = """
                    INSERT INTO plantas_medicinais (nome_popular, nome_cientifico, propriedades)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE 
                    nome_popular = VALUES(nome_popular), 
                    propriedades = VALUES(propriedades)
                """
                cur.execute(sql, (linha['nome_popular'], linha['nome_cientifico'], linha['propriedades']))
        
        conn.commit()
        print("Sucesso! Dados migrados para o MySQL da SuperDomínios.")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    importar_para_mysql()
