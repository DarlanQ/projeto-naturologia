import psycopg2
import wikipedia

# Configura a Wikipedia para buscar conteúdo em Português
wikipedia.set_lang("pt")

# Substitua a lista 'plantas' antiga por esta:
plantas = [
    # As que você sentiu falta e plantas do SUS (RENISUS)
    "Cordia verbenacea", "Uncaria tomentosa", "Schinus terebinthifolia",
    "Ananas comosus", "Apium graveolens", "Artemisia absinthium", 
    "Baccharis trimera", "Bauhinia forficata", "Bidens pilosa", 
    "Calendula officinalis", "Camellia sinensis", "Casearia sylvestris", 
    "Cynara scolymus", "Equisetum arvense", "Glycine max", 
    "Harpagophytum procumbens", "Ilex paraguariensis", "Justicia pectoralis", 
    "Lippia alba", "Matricaria chamomilla", "Mentha x piperita", 
    "Mikania glomerata", "Ocimum gratissimum", "Passiflora incarnata", 
    "Peumus boldus", "Plantago major", "Plectranthus barbatus", 
    "Polygonum punctatum", "Psidium guajava", "Punica granatum", 
    "Rhamnus purshiana", "Ricinus communis", "Salix alba", 
    "Solanum paniculatum", "Solidago chilensis", "Stryphnodendron adstringens", 
    "Tagetes minuta", "Trifolium pratense", "Zingiber officinale",
    "Acanthospermum australe", "Achillea millefolium", "Allium sativum",
    "Alpinia zerumbet", "Anethum graveolens", "Arctium lappa",
    "Bryophyllum pinnatum", "Chenopodium ambrosioides", "Copaifera",
    "Crataegus", "Cucurbita pepo", "Cuphea carthagenensis",
    "Dalbergia ecastaphyllum", "Eleutherococcus senticosus", "Euphorbia tirucalli",
    "Foeniculum vulgare", "Hamamelis virginiana", "Lamium album",
    "Leonurus cardiaca", "Linum usitatissimum", "Melissa officinalis",
    "Morus nigra", "Nasturtium officinale", "Origanum vulgare",
    "Panax ginseng", "Persea americana", "Petroselinum crispum",
    "Phyllanthus niruri", "Physalis angulata", "Pimpinella anisum",
    "Rosmarinus officinalis", "Ruta graveolens", "Sambucus nigra",
    "Silybum marianum", "Stachytarpheta cayennensis", "Symphytum officinale",
    "Syzygium cumini", "Tabebuia impetiginosa", "Taraxacum officinale",
    "Thymus vulgaris", "Tilia cordata", "Tribulus terrestris",
    "Trigonella foenum-graecum", "Valeriana officinalis", "Vernonia condensata"
]


def iniciar_garimpo():
    try:
        # Conexão com o seu banco de dados PostgreSQL
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="2366"
        )
        cur = conn.cursor()

        print(f"--- Iniciando garimpo de {len(plantas)} plantas ---\n")

        for nome in plantas:
            try:
                # Busca os dados na Wikipedia
                page = wikipedia.page(nome)
                titulo_cientifico = page.title
                resumo = page.summary[:1500] # Pegamos um bom resumo do texto

                # A "Blindagem": Se o nome científico já existir, o ON CONFLICT ignora
                sql = """
                    INSERT INTO plantas_medicinais (nome_popular, nome_cientifico, propriedades)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (nome_cientifico) DO NOTHING;
                """
                cur.execute(sql, (nome, titulo_cientifico, resumo))
                conn.commit()
                print(f"[OK] {titulo_cientifico} processada.")

            except wikipedia.exceptions.PageError:
                print(f"[Aviso] Página não encontrada para: {nome}")
            except wikipedia.exceptions.DisambiguationError:
                print(f"[Aviso] Muitos resultados para: {nome}. Tente ser mais específico.")
            except Exception as e:
                print(f"[Erro] Falha ao processar {nome}: {e}")

        print("\n--- Garimpo finalizado com sucesso! ---")

    except Exception as e:
        print(f"Erro fatal de conexão: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    iniciar_garimpo()
