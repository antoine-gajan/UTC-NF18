import psycopg2


def connexion():
    """Fonction permettant de se connecter à la BDD"""
    #Identifiant de connexion
    HOST = "localhost"
    USER = "postgres"
    PASSWORD = "Esvfjfpk060303"
    DATABASE = "banque"

    #Ouverture de la connexion
    conn = psycopg2.connect(f"host={HOST} dbname={DATABASE} user={USER} password={PASSWORD}")

    #Creation d'un curseur
    cur = conn.cursor()
    return conn, cur

def close(connexion):
    """Fonction qui ferme la connexion avec la BDD"""
    connexion.close()