import datetime
import psycopg2
from psycopg2 import errors

from modification import *

def insererClient(connexion, curseur):
    print("*** Ajout d'un client ***")
    nom = input("Nom du client : ")
    telephone = input("Telephone : ")
    adresse = input("Adresse : ")
    sql = f"INSERT INTO Client (nom, telephone, adresse) VALUES('{nom}', '{telephone}', '{adresse}')"
    try:
        curseur.execute(sql)
        connexion.commit()
    except psycopg2.IntegrityError:
        print("Impossible de créer le compte client : problème sur la clé primaire.")
        connexion.rollback()
    except psycopg2.errors.UniqueViolation:
        print("Violation d'une contrainte d'unicité. Annulation de la création du compte client.")
        connexion.rollback()
    except:
        print("Erreur rencontrée. Impossible de créer le compte client.")
        connexion.rollback()
    else:
        print("Création du compte client realise avec succès.")


def insererCompteCourant(connexion, curseur):
    """Fonction qui insere un compte courant dans la BDD"""
    print("*** Ajout d'un compte courant ***")
    #Creation de la date de creation
    date_creation = input("Date de création du compte (YYYY-MM-DD) : ")
    date_creation_check = date_creation.split('-')
    date_creation_check = datetime.datetime(int(date_creation_check[0]), int(date_creation_check[1]), int(date_creation_check[2]))
    #Decouvert max autorise
    decouvert_max = int(input("Découvert maximal autorise : "))
    if decouvert_max < 0 :
        #Conversion en nombre positif pour la BDD
        decouvert_max = - decouvert_max
    #Solde
    solde = int(input("Solde du compte : "))
    while solde < (-decouvert_max):
        solde = int(input("Le solde ne peut pas être inférieur au découvert maximal.\nSolde du compte : "))
    #Statut du compte
    statut = {"1":"ouvert", "2":"bloque","3":"ferme"}
    s = input("Statut du compte (1 : ouvert, 2 : bloqué, 3 : fermé) : ")
    while s not in ["1", "2", "3"]:
        s = input("Statut incorrect.\nStatut du compte (1 : ouvert, 2 : bloqué, 3 : fermé) : ")
    #Gestion du decouvert
    if solde < 0:
        date_decouvert = input("\nVotre solde est négatif. Date de découvert (YYYY-MM-DD) : ")
        date_decouvert_check = date_decouvert.split("-")
        date_decouvert_check = datetime.datetime(int(date_decouvert_check[0]), int(date_decouvert_check[1]), int(date_decouvert_check[2]))
        while date_creation_check > date_decouvert_check:
            date_decouvert = input("La date de découvert ne peut pas être antérieure à la date de creation du compte.\nDate de decouvert (YYYY-MM-DD) : ")
            date_decouvert_check = date_decouvert.split("-")
            date_decouvert_check = datetime.datetime(int(date_decouvert_check[0]), int(date_decouvert_check[1]), int(date_decouvert_check[2]))
        sql2 = f"""INSERT INTO comptecourant VALUES('{date_creation}','{date_decouvert}',{decouvert_max});"""
    else:
        sql2 = f"""INSERT INTO comptecourant VALUES('{date_creation}', NULL,{decouvert_max});"""
    #Requête SQL
    sql1 = f"""INSERT INTO Compte VALUES('{date_creation}', '{statut[s]}', {solde});"""
    #Ajout dans la BDD
    try:
        curseur.execute(sql1)
        curseur.execute(sql2)
        connexion.commit()
    except psycopg2.IntegrityError:
        print("Impossible de créer le compte : problème sur la cle primaire.")
        connexion.rollback()
    except psycopg2.errors.UniqueViolation:
        print("Violation d'une contrainte d'unicité. Annulation de la création du compte.")
        connexion.rollback()
    except:
        print("La création du compte a échoué.")
        connexion.rollback()
    else:
        print("Création du compte réalisée avec succès.")

def insererCompteRevolving(connexion, curseur):
    """Fonction qui insere un compte courant dans la BDD"""
    print("*** Ajout d'un compte revolving ***")
    #Creation de la date de creation
    date_creation = input("Date de création du compte (YYYY-MM-DD) : ")
    #Decouvert max autorise
    montant_min = int(input("Montant minimal négocié : "))
    if montant_min > 0 :
        #Conversion en nombre negatif
        montant_min = - montant_min
    #Solde
    solde = int(input("Solde du compte : "))
    #Statut du compte
    statut = {"1":"ouvert", "2":"bloque","3":"ferme"}
    s = input("Statut du compte (1 : ouvert, 2 : bloqué, 3 : fermé) : ")
    while s not in ["1", "2", "3"]:
        s = input("Statut incorrect.\nStatut du compte (1 : ouvert, 2 : bloqué, 3 : fermé) : ")
    #Gestion du taux d'interet
    taux = int(input("Taux d'intérêt journalier : "))
    while taux < 0:
        taux = int(input("Le taux d'intérêt ne peut pas être négatif.\nTaux d'intérêt journalier : "))
    #Requête SQL
    sql1 = f"""INSERT INTO Compte VALUES('{date_creation}', '{statut[s]}', {solde});"""
    sql2 = f"""INSERT INTO CompteRevolving VALUES('{date_creation}'), {montant_min}, {taux});"""
    #Ajout dans la BDD
    try:
        curseur.execute(sql1)
        curseur.execute(sql2)
        connexion.commit()
    except psycopg2.IntegrityError:
        print("Impossible de créer le compte : problème sur la cle primaire.")
        connexion.rollback()
    except psycopg2.errors.UniqueViolation:
        print("Violation d'une contrainte d'unicité. Annulation de la creation du compte.")
        connexion.rollback()
    except:
        print("Erreur rencontrée. La création du compte a échoué.")
        connexion.rollback()
    else:
        print("Création du compte réalisée avec succès.")

def insererCompteEpargne(connexion, curseur):
    """Fonction qui insère un compte d'epargne dans la BDD"""
    print("*** Ajout d'un compte d'epargne ***")
    #Creation de la date de creation
    date_creation = input("Date de création du compte (YYYY-MM-DD) : ")
    #Solde du compte
    solde = int(input("Solde du compte : "))
    if solde < 300 :
        #Impossible
        solde = int(input("Le solde doit être supérieur à 300€.\nSolde du compte : "))
    #Statut du compte
    statut = {"1":"ouvert", "2":"bloque", "3":"ferme"}
    s = input("Statut du compte (1 : ouvert, 2 : bloqué, 3 : fermé) : ")
    while s not in ["1", "2", "3"]:
        s = input("Statut incorrect.\nStatut du compte (1 : ouvert, 2 : bloqué, 3 : fermé) : ")
    #Requête SQL
    sql1 = f"""INSERT INTO Compte VALUES('{date_creation}', '{statut[s]}', '{solde}');"""
    sql2 = f"""INSERT INTO CompteEpargne VALUES('{date_creation}');"""
    #Ajout dans la BDD
    try:
        curseur.execute(sql1)
        curseur.execute(sql2)
        connexion.commit()
    except psycopg2.IntegrityError:
        print("Impossible de créer le compte : problème sur la clé primaire.")
        connexion.rollback()
    except psycopg2.errors.UniqueViolation:
        print("Violation d'une contrainte d'unicité. Annulation de la création du compte.")
        connexion.rollback()
    except:
        print("La création du compte a échoué.")
        connexion.rollback()
    else:
        print("Création du compte réalisée avec succès.")

def insererOperation(connexion, curseur):
    """Fonction qui permet d'inserer une operation dans la BDD"""
    print("*** Effectuer une operation ***")
    aujourdhui = f"{date.today().year}-{date.today().month:02}-{date.today().day:02}"
    clients = getClients(curseur)
    #Test du nombre de clients
    if len(clients) == 0:
        print("Aucun client dans la base de données.\n")
    else:
        #Affichage de la liste des clients
        print("Liste des clients (ID, nom) : ")
        for client in clients:
            print(f"{client[0]:8d}\t{client[1]}")
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
            if date_creation in [f"{compte[0]}" for compte in comptesUtilisateur]:
                #Verification du statut du compte
                statut = getInfosCompte(curseur, date_creation)[0][1]
                #Si compte ferme, aucune operation possible
                if statut == "ferme":
                    print("Le compte est fermé. Aucune opération possible.")
                    return
                #Si statut bloque, uniquement operation guichet et cheque avec montant > 0 (credit)
                elif statut == "bloque":
                    typeOpe = {"1" : "Guichet", "2" : "Cheque"}
                    type = input("Type d'operation effectuee (1 : Guichet, 2 : Cheque)\n  ->")
                    while type not in ["1", "2"]:
                        type = input("Ce type d'operation n'existe pas.\nType d'opération effectuée : ")
                #Si le compte est ouvert, tous types d'operation possible
                else:
                    typeOpe = {"1" : "Guichet", "2" : "Cheque", "3" : "Virement", "4" : "CB"}
                    type = input("Type d'opération effectuée (1 : Guichet, 2 : Chèque, 3 : Virement, 4 : Carte bancaire)\n  ->")
                    while type not in ["1", "2", "3", "4"]:
                        type = input("Ce type d'opération n'existe pas.\nType d'opération effectuée : ")
                #Demande du montant
                montant = int(input("Montant de l'opération (positif pour crédit, négatif pour debit) : "))

                #Gestion des cas d'erreurs lies au type de compte
                if (Typecompte(curseur, date_creation) == 'epargne' and getSoldeCompte(curseur, date_creation) + montant < 300) :
                    print("Impossible d'effectuer l'opération. Il ne peut pas y avoir de compte epargne avec un solde en dessous de 300 €.\nAnnulation de l'opération.")
                    return
                if (Typecompte(curseur, date_creation) == 'revolving' and getSoldeCompte(curseur, date_creation) + montant > 0) :
                    print("Impossible d'effectuer l'opération. Il ne peut pas y avoir de compte revolving au dessus de 0 €.\nAnnulation de l'opération.")
                    return
                if (Typecompte(curseur, date_creation) == 'revolving' and getSoldeCompte(curseur, date_creation) + montant < GetMin(curseur, date_creation)) :
                    print("Impossible d'effectuer l'opération. Il ne peut pas y avoir de compte revolving en dessous du minimum autorisé.\nAnnulation de l'opération.")
                    return
                if (Typecompte(curseur, date_creation) == 'courant' and getSoldeCompte(curseur, date_creation) + montant < -GetDecouvert(curseur, date_creation)) :
                    print("Impossible d'effectuer l'opération. Il ne peut pas y avoir de compte courant en dessus du decouvert autorisé.\nAnnulation de l'opération.")
                    return
                if (Typecompte(curseur, date_creation) == 'epargne' and typeOpe[type] not in ['Guichet', 'Virement']):
                    print("Les comptes épargnes ne peuvent faires que des opérations guichet et virement.\nAnnulation de l'opération.")
                    return

                #Traitement des cas particuliers si le compte est bloque
                if montant < 0 and statut == "bloque":
                    print("Seules les opérations de crédit sont possibles. Annulation de l'opération.")
                elif statut == "bloque":
                    etat = "traite"
                    if type == "2":
                        #Ajout de l'operation
                        sql1 = f"INSERT INTO Operation VALUES('{id}', '{date_creation}', '{montant}', '{aujourdhui}', '{etat}', 'Cheque', 'depot')"
                        #Modification du solde
                        sql2 = f"UPDATE Compte SET solde = '{getSoldeCompte(curseur, date_creation) + montant}' WHERE date_creation = '{date_creation}')"

                    else:
                        #Ajout de l'operation
                        sql1 = f"INSERT INTO Operation VALUES({id}, '{date_creation}', {montant}, '{aujourdhui}' , '{etat}', '{typeOpe[type]}', NULL)"
                        #Modification du solde
                        sql2 = f"UPDATE Compte SET solde = '{getSoldeCompte(curseur, date_creation) + montant}' WHERE date_creation = '{date_creation}'"
                    #Ajout des reqûetes à la BDD
                    try:
                        curseur.execute(sql1)
                        curseur.execute(sql2)
                        connexion.commit()
                        #Mise à jour de la table MinMaxMois
                        UpdateMinMaxMois(connexion, curseur, date_creation)
                    except:
                        print("L'ajout de l'opération a échoué.")
                        connexion.rollback()
                    else:
                        print("Ajout de l'opération réalisé avec succès.")
                #Si le compte est ouvert, aucun souci
                else:
                    etat = "traite"
                    #Si le montant est negatif, c'est un debit
                    if type == "2" and montant < 0:
                        sql1 = f"INSERT INTO Operation VALUES({id}, '{date_creation}', {montant}, '{aujourdhui}', '{etat}', '{typeOpe[type]}', 'depot')"
                    elif type == "2":
                        sql1 = f"INSERT INTO Operation VALUES({id}, '{date_creation}', {montant}, '{aujourdhui}' , '{etat}', '{typeOpe[type]}', 'emission')"
                    else:
                        sql1 = f"INSERT INTO Operation VALUES({id}, '{date_creation}', {montant}, '{aujourdhui}' , '{etat}', '{typeOpe[type]}', NULL)"
                    #Modification du solde du compte
                    sql2 = f"UPDATE Compte SET solde = '{getSoldeCompte(curseur, date_creation) + montant}' WHERE date_creation = '{date_creation}'"
                    # Ajout dans la BDD
                    try:
                        curseur.execute(sql1)
                        curseur.execute(sql2)
                        connexion.commit()
                        #Mise à jour de la table MinMaxMois
                        UpdateMinMaxMois(curseur, date_creation)
                    except:
                        print("L'ajout de l'opération a échoué.")
                        connexion.rollback()
                    else:
                        print("Ajout de l'opération réalisé avec succès.")
            #Message d'erreur, le compte n'existe pas
            else:
                print("Ce compte n'existe pas. Abandon de l'opération.")
        #Message d'erreur, client inconnu
        else:
            print("Cet utilisateur n'est pas un client. Abandon de l'opération.")

def insererAppartenir(connexion, curseur):
    """Fonction qui rajoute un client comme propriétaire d'un compte"""
    print("*** Ajouter une relation d'appartenance ***")
    clients = getClients(curseur)
    # Test du nombre de clients
    if len(clients) == 0:
        print("Aucun client dans la base de données. Veuillez d'abord ajouter un utilisateur.\nAbandon de l'ajout de propriétaire.")
    else:
        # Affichage de la liste des clients
        print("Liste des clients (ID, nom) : ")
        for client in clients:
            print(f"{client[0]}\t{client[1]}")
        # Demande de l'id du client
        id = int(input("ID du client : "))
        if id not in [client[0] for client in clients]:
            print("Ce client n'existe pas.")
            return
        comptes = getAllComptes(curseur)
        if len(comptes) == 0:
            print("Aucun compte dans la base de donnees. Veuillez d'abord ajouter un compte.\nAbandon de l'ajout de proprietaire.")
            return
        #Affichage de tous les comptes
        print("Liste des comptes de l'utilisateur choisi (date de creation, statut, solde) : ")
        for compte in comptes:
            print(f"{compte[0]}\t{compte[1]}\t{compte[2]}")
        date_creation = input("Date de creation du compte où vous voulez être proprietaire (YYYY-MM-DD) : ")
        if date_creation not in [f"{compte[0]}" for compte in comptes]:
            print("Ce compte n'existe pas. Abandon de l'ajout de propriétaire.")
            return
        #Si id client correct et date de creation de compte correcte
        sql = f"""INSERT INTO Appartenir VALUES({id}, '{date_creation}')"""
        try:
            curseur.execute(sql)
            connexion.commit()
        except psycopg2.IntegrityError:
            print("Le client est déjà propriétaire de ce compte !")
            connexion.rollback()
        except psycopg2.errors.UniqueViolation:
            print("Violation d'une contrainte d'unicité. Annulation de la création d'appartenance.")
            connexion.rollback()
        except psycopg2.errors.ForeignKeyViolation:
            print("Violation d'une contrainte de clé étrangère. Annulation de la création d'appartenance. ")
        except:
            print("La création de la relation d'appartenance a échoué.")
            connexion.rollback()
        else:
            print("Ajout de la relation d'appartenance client-compte.")
