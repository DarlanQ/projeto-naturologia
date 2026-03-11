import psycopg2
from datetime import datetime

def conectar():
    return psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="2366"
    )

def gerar_relatorio():
    print("\n" + "="*50)
    print("      SISTEMA DE CONSULTA FITOTERÁPICA       ")
    print("="*50)
    
    termo = input("Digite o nome da planta para busca: ")

    try:
        conn = conectar()
        cur = conn.cursor()

        # Usamos o ILIKE para a busca ignorar maiúsculas/minúsculas
        # O % permite que você digite apenas "Espinheira" e ele ache "Espinheira-santa"
        sql = """
            SELECT nome_popular, nome_cientifico, propriedades 
            FROM plantas_medicinais 
            WHERE nome_popular ILIKE %s OR nome_cientifico ILIKE %s;
        """
        cur.execute(sql, (f'%{termo}%', f'%{termo}%'))
        resultados = cur.fetchall()

        if not resultados:
            print(f"\n[!] Nenhuma planta encontrada com o termo '{termo}'.")
        else:
            for r in resultados:
                print("\n" + "-"*50)
                print(f"🌿 PLANTA: {r[0].upper()}")
                print(f"🧬 NOME CIENTÍFICO: {r[1]}")
                print(f"📖 DESCRIÇÃO/PROPRIEDADES:")
                # Formata o texto para não ficar uma linha gigante
                print(f"   {r[2][:500]}...") 
                print("-"*50)
                print(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    except Exception as e:
        print(f"\n[ERRO] Falha na consulta: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    while True:
        gerar_relatorio()
        if input("\nNova busca? (S/N): ").upper() != 'S':
            print("\nEncerrando consulta. Boa prática terapêutica, Darlan!")
            break



