import datetime
import psycopg2

from requete import *

def insererCompteCourant(curseur):
    """Fonction qui insère un compte courant dans la BDD"""
    #Création de la date de création
    date_creation = input("Date de création du compte (YYYY-MM-DD) : ")
    date_creation = date_creation.split('-')
    date_creation_check = datetime.datetime(int(date_creation[0]), int(date_creation[1]), int(date_creation[2]))
    #Decouvert max autorisé
    decouvert_max = int(input("Découvert maximal autorisé : "))
    if decouvert_max > 0 :
        #Conversion en nombre négatif
        decouvert_max = - decouvert_max
    #Solde
    solde = int(input("Solde du compte : "))
    while solde < decouvert_max:
        solde = int(input("Le solde ne peut pas être inférieur au découvert maximal.\nSolde du compte : "))
    #Statut du compte
    statut = {"1":"ouvert", "2":"bloqué","3":"fermé"}
    s = int(input("Statut du compte (1 : ouvert, 2 : bloqué, 3 : fermé) : "))
    while s not in [1, 2, 3]:
        s = input("Statut incorrect.\nStatut du compte (1 : ouvert, 2 : bloqué, 3 : fermé) : ")
    #Gestion du découvert
    if solde < 0:
        date_decouvert = input("\nVotre solde est négatif. Date de découvert (YYYY-MM-DD) : ")
        date_decouvert = date_decouvert.split("-")
        date_decouvert_check = datetime.datetime(int(date_decouvert[0]), int(date_decouvert[1]), int(date_decouvert[2]))
        while date_creation_check > date_decouvert_check:
            date_decouvert = input("La date de découvert ne peut pas être antérieure à la date de création du compte.\nDate de découvert (YYYY-MM-DD) : ")
            date_decouvert = date_decouvert.split("-")
            date_decouvert_check = datetime.datetime(int(date_decouvert[0]), int(date_decouvert[1]), int(date_decouvert[2]))
    #Requête SQL
    sql1 = f"""INSERT INTO Compte VALUES('{date_creation}', '{statut[s]}', '{solde}');"""
    sql2 = f"""INSERT INTO comptecourant VALUES(TO_DATE({date_creation}, "YYYY-MM-DD"), TO_DATE({date_decouvert}, "YYYY-MM-DD"), {decouvert_max});"""
    #Ajout dans la BDD
    try:
        curseur.execute(sql1)
        curseur.execute(sql2)
        curseur.commit()
    except:
        print("La création du compte a échoué.")
        curseur.rollback()
    else:
        print("Création du compte réalisé avec succès.")

def insererCompteRevolving(curseur):
    """Fonction qui insère un compte courant dans la BDD"""
    #Création de la date de création
    date_creation = input("Date de création du compte (YYYY-MM-DD) : ")
    date_creation = date_creation.split('-')
    date_creation_check = datetime.datetime(int(date_creation[0]), int(date_creation[1]), int(date_creation[2]))
    #Decouvert max autorisé
    montant_min = int(input("Montant minimal négocié : "))
    if montant_min > 0 :
        #Conversion en nombre négatif
        montant_min = - montant_min
    #Solde
    solde = int(input("Solde du compte : "))
    #Statut du compte
    statut = {"1":"ouvert", "2":"bloqué","3":"fermé"}
    s = int(input("Statut du compte (1 : ouvert, 2 : bloqué, 3 : fermé) : "))
    while s not in ["1", "2", "3"]:
        s = input("Statut incorrect.\nStatut du compte (1 : ouvert, 2 : bloqué, 3 : fermé) : ")
    #Gestion du taux d'interet
    taux = int(input("Taux d'interet journalier : "))
    while taux < 0:
        taux = int(input("Le taux d'intérêt ne peut pas être négatif.\nTaux d'intérêt journalier : "))
    #Requête SQL
    sql1 = f"""INSERT INTO Compte VALUES(TO_DATE({date_creation}, 'YYYY-MM-DD'), '{statut[s]}', '{solde}');"""
    sql2 = f"""INSERT INTO CompteRevolving VALUES(TO_DATE({date_creation}, 'YYYY-MM-DD'), '{montant_min}', '{taux}');"""
    #Ajout dans la BDD
    try:
        curseur.execute(sql1)
        curseur.execute(sql2)
        curseur.commit()
    except:
        print("La création du compte a échoué.")
        curseur.rollback()
    else:
        print("Création du compte réalisé avec succès.")

def insererOperation(curseur):
    """Fonction qui permet d'insérer une opération dans la BDD"""
    clients = getClients(curseur)
    #Test du nombre de clients
    if len(clients) == 0:
        print("Aucun client dans la base de données\n")
    else:
        #Affichage de la liste des clients
        print("Liste des clients (ID, nom) : ")
        for client in clients:
            print(f"{client[0]}\t{client[1]}")
        #Demande de l'id du client
        id = int(input("ID de l'utilisateur : "))
        if id in [client[0] for client in clients]:
            comptesUtilisateur = getComptesUtilisateur(curseur, id)
            #Affichage de la liste des comptes
            print("Liste des comptes de l'utilisateur choisi (date de création, statut, solde) : ")
            for compte in comptesUtilisateur:
                print(f"{compte[0]}\t{compte[1]}\t{compte[2]}")
            #Demande du compte
            date_creation = input("Date de création du compte où effectuer l'opération : ")
            if date_creation in [compte[0] for compte in comptesUtilisateur]:
                #Vérification du statut du compte
                statut = getInfosCompte(curseur, date_creation)[1]
                #Si compte fermé, aucune opération possible
                if statut == "fermé":
                    print("Le compte est fermé. Aucune opération possible.")
                    exit()
                #Si statut bloqué, uniquement opération guichet et chèque avec montant > 0 (crédit)
                elif statut == "bloqué":
                    typeOpe = {"1" : "Guichet", "2" : "Chèque"}
                    type = input("Type d'opération effectuée : ")
                    while type not in ["1", "2"]:
                        type = input("Ce type d'opération n'existe pas.\nType d'opération effectuée : ")
                #Si le compte est ouvert, tous types d'opération possible
                else:
                    typeOpe = {"1" : "Guichet", "2" : "Chèque", "3" : "Virement"}
                    type = input("Type d'opération effectuée : ")
                    while type not in ["1", "2", "3"]:
                        type = input("Ce type d'opération n'existe pas.\nType d'opération effectuée : ")
                #Demande du montant
                montant = int(input("Montant de l'opération (positif pour crédit, négatif pour débit) : "))
                #Traitement des cas particuliers si le compte est bloqué
                if montant < 0 and statut == "bloqué":
                    print("Seules les opérations de crédit sont possibles. Annulation de l'opération.")
                elif statut == "bloqué":
                    etat = "traité"
                    if type == "2":
                        #Ajout de l'opération
                        sql1 = f"INSERT INTO Operation VALUES('{id}', '{date_creation}', '{montant}', CURRENT_DATE(), '{etat}', 'Chèque', 'depot')"
                        #Modification du solde
                        sql2 = f"UPDATE Compte SET solde = '{getSoldeCompte(curseur, date_creation) + montant}' WHERE date_creation = '{date_creation}')"

                    else:
                        #Ajout de l'opération
                        sql1 = f"INSERT INTO Operation VALUES('{id}', '{date_creation}', '{montant}', CURRENT_DATE(), '{etat}', '{typeOpe[{type}]}', NULL)"
                        #Modification du solde
                        sql2 = f"UPDATE Compte SET solde = '{getSoldeCompte(curseur, date_creation) + montant}' WHERE date_creation = '{date_creation}')"
                    #Ajout des reqûetes à la BDD
                    try:
                        curseur.execute(sql1)
                        curseur.execute(sql2)
                        curseur.commit()
                    except:
                        print("L'ajout de l'opération a échoué.")
                        curseur.rollback()
                    else:
                        print("Ajout de l'opération réalisé avec succès.")
                #Si le compte est ouvert, aucun souci
                else:
                    etat = "traité"
                    #Si le montant est négatif, c'est un débit
                    if type == "2" and montant < 0:
                        sql1 = f"INSERT INTO Operation VALUES('{id}', '{date_creation}', '{montant}', CURRENT_DATE(), '{etat}', '{typeOpe[{type}]}', 'depot')"
                    elif type == "2":
                        sql1 = f"INSERT INTO Operation VALUES('{id}', '{date_creation}', '{montant}', CURRENT_DATE(), '{etat}', '{typeOpe[{type}]}', 'emission')"
                    else:
                        sql1 = f"INSERT INTO Operation VALUES('{id}', '{date_creation}', '{montant}', CURRENT_DATE(), '{etat}', '{typeOpe[{type}]}', NULL)"
                    #Modification du solde du compte
                    sql2 = f"UPDATE Compte SET solde = '{getSoldeCompte(curseur, date_creation) + montant}' WHERE date_creation = '{date_creation}')"
                    # Ajout dans la BDD
                    try:
                        curseur.execute(sql1)
                        curseur.execute(sql2)
                        curseur.commit()
                    except:
                        print("L'ajout de l'opération a échoué.")
                        curseur.rollback()
                    else:
                        print("Ajout de l'opération réalisé avec succès.")
            #Message d'erreur, le compte n'existe pas
            else:
                print("Ce compte n'existe pas. Abandon de l'opération.")
        #Message d'erreur, client inconnu
        else:
            print("Cet utilisateur n'est pas un client. Abandon de l'opération.")
