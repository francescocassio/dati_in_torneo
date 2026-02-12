import csv


# 1. GESTIONE DEI NOMI COMPOSTI
def estrai_nome_cognome(testo):
    parti = testo.strip().split()
    nome = parti[0]
    # Se ci sono più parole, consideriamo la prima come nome e TUTTE le altre
    # come cognome (es: "Gian Maria" -> nome="Gian", cognome="Maria")
    # Se c'è una sola parola, il cognome rimane una stringa vuota.
    cognome = " ".join(parti[1:]) if len(parti) > 1 else ""
    return nome, cognome


# 2. ENCODING 'utf-8-sig'
# L'encoding sig rimuove l'eventuale "BOM" (un carattere invisibile all'inizio del file)
# tipico dei file CSV salvati con Excel, evitando errori di lettura sulla prima colonna.
with open("ladybidon.csv", mode='r', encoding='utf-8-sig') as f:
    reader = csv.reader(f, delimiter=',')
    headers = next(reader)  # Salta la riga delle intestazioni

    # Inizializziamo la query con la sintassi per un inserimento multiplo (bulk insert)
    q = """INSERT INTO tournament_player (id, first_name, last_name) VALUES \n"""

    id = 2000

    for riga in reader:
        # Pulizia spazi bianchi superflui all'inizio/fine
        g1 = riga[2].strip()
        g2 = riga[3].strip()

        nome1, cognome1 = estrai_nome_cognome(g1)
        nome2, cognome2 = estrai_nome_cognome(g2)

        # 3. GESTIONE DEGLI APOSITOFI (Escaping)
        # In SQL l'apostrofo è un carattere speciale. Se un nome è "D'Amico",
        # scriverlo come 'D'Amico' romperebbe la query.
        # Raddoppiandolo ('D''Amico') SQL capisce che è un carattere di testo.
        nome1 = nome1.replace("'", "''")
        cognome1 = cognome1.replace("'", "''")
        nome2 = nome2.replace("'", "''")
        cognome2 = cognome2.replace("'", "''")

        # Composizione della stringa con i valori
        q += f"({id}, '{nome1}', '{cognome1}'),\n"
        id += 1
        q += f"({id}, '{nome2}', '{cognome2}'),\n"
        id += 1

    # 4. PULIZIA FINALE
    # q[:-2] rimuove l'ultima virgola e l'ultimo "a capo" aggiunti nel ciclo for,
    # chiudendo poi la query correttamente con un punto e virgola.
    q = q[:-2] + ";"

with open("inserimento_giocatori.sql", mode='w', encoding='utf-8-sig') as f:
    f.write(q)