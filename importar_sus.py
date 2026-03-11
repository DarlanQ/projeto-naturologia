import csv
import psycopg2

def importar_dados_oficiais():
    conn = None
    try:
        # 1. Conexão com o banco (ajuste a senha se necessário)
        conn = psycopg2.connect(
            host="localhost", 
            database="postgres", 
            user="postgres", 
            password="2366"
        )
        cur = conn.cursor()

        print("--- Iniciando Importação RENISUS ---")

        # 2. Abrindo o arquivo CSV
        with open('renisus.csv', mode='r', encoding='utf-8') as f:
            # Usamos o delimitador ';' para evitar erro com as vírgulas dos nomes
            leitor = csv.DictReader(f, delimiter=';')
            
            contador = 0
            for linha in leitor:
                sql = """
                    INSERT INTO plantas_medicinais (nome_popular, nome_cientifico, propriedades)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (nome_cientifico) DO UPDATE 
                    SET propriedades = EXCLUDED.propriedades, 
                        nome_popular = EXCLUDED.nome_popular;
                """
                cur.execute(sql, (linha['nome_popular'], linha['nome_cientifico'], linha['propriedades']))
                contador += 1
        
        conn.commit()
        print(f"--- Sucesso! {contador} plantas importadas para o banco. ---")

    except Exception as e:
        print(f"Erro na importação: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    importar_dados_oficiais()
