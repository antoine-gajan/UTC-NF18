from requete import *

def supprimerClient(conn, cur):
    """Fonction qui supprime un client de la BDD"""
    numero = input("Numero de telephone du client : ")
    sql = f"DELETE FROM Client WHERE telephone = {numero}"
    try:
        cur.execute(sql)
        conn.commit()
    except:
        conn.rollback()
        print("Erreur rencontree. Impossible de supprimer ce client.")

def supprimerCompte(conn, cur):
    """Fonction qui supprime un compte de la BDD"""
    date_creation = input("Date de creation du compte : ")
    sql = f"DELETE FROM Client WHERE date_creation = '{date_creation}'"
    try:
        cur.execute(sql)
        conn.commit()
    except:
        conn.rollback()
        print("Erreur rencontree. Impossible de supprimer ce compte.")

def supprimeAppartenance(conn, cur):
    clients = getClients(cur)
    # Test du nombre de clients
    if len(clients) == 0:
        print("Aucun client dans la base de donnees.\nAucune suppression de relation d'appartenance possible.")
    else:
        # Affichage de la liste des clients
        print("Liste des clients (ID, nom) : ")
        for client in clients:
            print(f"{client[0]}\t{client[1]}")
        # Demande de l'id du client
        id = int(input("Choix de l'ID de l'utilisateur : "))
        if id in [client[0] for client in clients]:
            comptesUtilisateur = getComptesUtilisateur(cur, id)
            # Affichage de la liste des comptes
            print("Liste des comptes de l'utilisateur choisi (date de creation, statut, solde) : ")
            for compte in comptesUtilisateur:
                print(f"{compte[0]}\t{compte[1]}\t{compte[2]}")
            # Demande du compte
            date_creation = input("Date de creation du compte où il faut supprimer la relation d'appartenance : ")
            if date_creation in [compte[0] for compte in comptesUtilisateur]:
                sql = f"DELETE FROM Appartenir WHERE compte = {date_creation} AND client = {id};"
                try:
                    cur.execute(sql)
                    conn.commit()
                except:
                    conn.rollback()
                    print("Erreur rencontree. Impossible de supprimer la relation d'appartenance.")
            else:
                print("Ce compte n'existe pas.")
        else:
            print("Ce client n'existe pas.")