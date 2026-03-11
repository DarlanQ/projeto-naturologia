from flask import Flask, render_template, request
import mysql.connector  # Mudamos de psycopg2 para mysql.connector

app = Flask(__name__)

def get_db_connection():
    # Aqui você usará os dados que criar no painel da SuperDomínios
    # Por enquanto, se quiser testar no Debian, instale o MySQL local
    return mysql.connector.connect(
        host="localhost",
        user="caminho6_naturologia",      # Seu usuário do banco no DirectAdmin
        password="DQjjkbtkdlle_221279!.",    # Sua senha do banco
        database="caminho6_naturologia" # Nome do banco que você criar
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    plantas = []
    termo = ""
    if request.method == 'POST':
        termo = request.form.get('termo', '')
        
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            # No MySQL, a busca LIKE já ignora acentos/maiúsculas 
            # se o banco for criado com o padrão 'utf8mb4_general_ci'
            sql = """
                SELECT nome_popular, nome_cientifico, propriedades 
                FROM plantas_medicinais 
                WHERE nome_popular LIKE %s 
                   OR nome_cientifico LIKE %s 
                   OR propriedades LIKE %s
            """
            
            # O sinal de % permite encontrar a palavra em qualquer lugar do texto
            termo_busca = f"%{termo}%"
            cur.execute(sql, (termo_busca, termo_busca, termo_busca))
            
            plantas = cur.fetchall()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Erro de conexão ou busca: {e}")
            # Em caso de erro, plantas continua como uma lista vazia
            
    return render_template('index.html', plantas=plantas, termo=termo)

if __name__ == '__main__':
    # No servidor da SuperDomínios, essa linha final não será usada,
    # mas deixamos aqui para você testar no seu Debian em Imbé.
#    app.run(debug=True)
