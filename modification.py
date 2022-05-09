from affichage import *
from requete import *

def UpdateClient(conn, curseur):
    print("*** Mise à jour des informations d'un client ***")
    #Affichage de la table
    afficherTable(curseur, 'Client', 1000000)
    client = int(input("id du client à modifier : "))
    #Demande des informations
    if client in [c[0] for c in getClients(curseur)]:
        nom = input("Entrez le nom du client : ")
        telephone = input("Entrez le numéro de téléphone : ")
        adresse = input("Adresse : ")
        sql = f"UPDATE Client SET nom = '{nom}', telephone = '{telephone}', adresse = '{adresse}' WHERE id = {client}"
        #Mise à jour de la BDD
        try:
            curseur.execute(sql)
            conn.commit()
        except:
            conn.rollback()
        else:
            print("Mise à jour des informations du client.")
    else:
        print("Ce client n'existe pas.")

def UpdateCompte(conn, curseur):
    print("*** Mise à jour des informations d'un compte ***")
    #Affichage de la table
    afficherTable(curseur, 'Compte', 1000000)
    compte = input("Date création du compte à modifier (YYYY-MM-DD) : ")
    #Demande des informations
    if compte in [f"{c[0]}" for c in getAllComptes(curseur)]:
        # Statut du compte
        statut = {"1": "ouvert", "2": "bloque", "3": "ferme"}
        s = input("Statut du compte (1 : ouvert, 2 : bloqué, 3 : fermé) : ")
        while s not in ["1", "2", "3"]:
            s = input("Statut incorrect.\nStatut du compte (1 : ouvert, 2 : bloqué, 3 : fermé) : ")
        sql = f"UPDATE Compte SET statut = '{statut[s]}' WHERE date_creation = '{compte}'"
        #Mise à jour de la BDD
        try:
            curseur.execute(sql)
            conn.commit()
        except:
            conn.rollback()
        else:
            print("Mise à jour des informations du compte.")
    else:
        print("Ce compte n'existe pas.")

def UpdateMinMaxMois(conn, curseur, date_creation):
    """Fonction qui met à jour le min/max du mois d'un compte, et qui cree une nouvelle isntance si on a change de mois"""
    sql = f"SELECT * FROM MinMaxMois WHERE compte = '{date_creation}' AND annee = {date.today().year} AND mois = {date.today().month}"
    MinMax = curseur.execute(sql)

    # Pas d'instance pour ce mois ci, on la cree
    if (len(MinMax) == 0):
        sql = f"INSERT INTO MinMaxMois (annee, min, max, mois, compte) VALUES ({date.today().year}, {getSoldeCompte(curseur, date_creation)}, {getSoldeCompte(curseur, date_creation)}, {date.today().month}, '{date_creation}')"
        try:
            curseur.execute(sql)
            conn.commit()
        except:
            conn.rollback()
            print("Erreur dans la mise à jour de MinMaxMois.")

    # Dejà une instance pour ce mois ci, on la met à jour si necessaire
    else:
        if (getSoldeCompte(curseur, date_creation) > MinMax[2]):
            sql = f"UPDATE MinMaxMois SET max = {getSoldeCompte(curseur, date_creation)} WHERE compte = '{date_creation}' AND annee = {date.today().year} AND mois = {date.today().month}"
            try:
                curseur.execute(sql)
                conn.commit()
                print("Erreur dans la mise à jour de MinMaxMois.")
            except:
                conn.rollback()

        if (getSoldeCompte(curseur, date_creation) < MinMax[1]):
            sql = f"UPDATE MinMaxMois SET min = {getSoldeCompte(curseur, date_creation)} WHERE compte = '{date_creation}' AND annee = {date.today().year} AND mois = {date.today().month}"
            try:
                curseur.execute(sql)
                conn.commit()
                print("Erreur dans la mise à jour de MinMaxMois.")
            except:
                conn.rollback()
