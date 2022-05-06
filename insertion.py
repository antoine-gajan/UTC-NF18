import datetime
import psycopg2
from psycopg2 import errors

from modification import *

def insererClient(curseur):
    print("*** Ajout d'un client ***")
    nom = input("Nom du client : ")
    telephone = input("Telephone : ")
    adresse = input("Adresse : ")
    sql = f"INSERT INTO Client (nom, telephone, adresse) VALUES({nom}, {telephone}, {adresse})"
    try:
        curseur.execute(sql)
        curseur.commit()
    except psycopg2.IntegrityError:
        print("Impossible de créer le compte client : problème sur la clé primaire.")
        curseur.rollback()
    except psycopg2.errors.UniqueViolation:
        print("Violation d'une contrainte d'unicité. Annulation de la création du compte client.")
        curseur.rollback()
    except:
        print("La création du compte client a échoué.")
        curseur.rollback()
    else:
        print("Création du compte client réalisé avec succès.")


def insererCompteCourant(curseur):
    """Fonction qui insère un compte courant dans la BDD"""
    print("*** Ajout d'un compte courant ***")
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
    except psycopg2.IntegrityError:
        print("Impossible de créer le compte : problème sur la clé primaire.")
        curseur.rollback()
    except psycopg2.errors.UniqueViolation:
        print("Violation d'une contrainte d'unicité. Annulation de la création du compte.")
        curseur.rollback()
    except:
        print("La création du compte a échoué.")
        curseur.rollback()
    else:
        print("Création du compte réalisé avec succès.")

def insererCompteRevolving(curseur):
    """Fonction qui insère un compte courant dans la BDD"""
    print("*** Ajout d'un compte revolving ***")
    #Création de la date de création
    date_creation = input("Date de création du compte (YYYY-MM-DD) : ")
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
    except psycopg2.IntegrityError:
        print("Impossible de créer le compte : problème sur la clé primaire.")
        curseur.rollback()
    except psycopg2.errors.UniqueViolation:
        print("Violation d'une contrainte d'unicité. Annulation de la création du compte.")
        curseur.rollback()
    except:
        print("La création du compte a échoué.")
        curseur.rollback()
    else:
        print("Création du compte réalisé avec succès.")

def insererCompteEpargne(curseur):
    """Fonction qui insère un compte d'épargne dans la BDD"""
    print("*** Ajout d'un compte d'épargne ***")
    #Création de la date de création
    date_creation = input("Date de création du compte (YYYY-MM-DD) : ")
    #Solde du compte
    solde = int(input("Solde du compte : "))
    if solde < 300 :
        #Impossible
        solde = int(input("Le solde doit être supérieur à 300€.\nSolde du compte : "))
    #Statut du compte
    statut = {"1":"ouvert", "2":"bloqué", "3":"fermé"}
    s = int(input("Statut du compte (1 : ouvert, 2 : bloqué, 3 : fermé) : "))
    while s not in ["1", "2", "3"]:
        s = input("Statut incorrect.\nStatut du compte (1 : ouvert, 2 : bloqué, 3 : fermé) : ")
    #Requête SQL
    sql1 = f"""INSERT INTO Compte VALUES(TO_DATE({date_creation}, 'YYYY-MM-DD'), '{statut[s]}', '{solde}');"""
    sql2 = f"""INSERT INTO CompteEpargne VALUES(TO_DATE({date_creation}, 'YYYY-MM-DD'));"""
    #Ajout dans la BDD
    try:
        curseur.execute(sql1)
        curseur.execute(sql2)
        curseur.commit()
    except psycopg2.IntegrityError:
        print("Impossible de créer le compte : problème sur la clé primaire.")
        curseur.rollback()
    except psycopg2.errors.UniqueViolation:
        print("Violation d'une contrainte d'unicité. Annulation de la création du compte.")
        curseur.rollback()
    except:
        print("La création du compte a échoué.")
        curseur.rollback()
    else:
        print("Création du compte réalisé avec succès.")

def insererOperation(curseur):
    """Fonction qui permet d'insérer une opération dans la BDD"""
    print("*** Effectuer une opération ***")
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
                statut = getInfosCompte(curseur, date_creation)[0][1]
                #Si compte fermé, aucune opération possible
                if statut == "fermé":
                    print("Le compte est fermé. Aucune opération possible.")
                    return
                #Si statut bloqué, uniquement opération guichet et chèque avec montant > 0 (crédit)
                elif statut == "bloqué":
                    typeOpe = {"1" : "Guichet", "2" : "Chèque"}
                    type = input("Type d'opération effectuée (1 : Guichet, 2 : Chèque)\n  ->")
                    while type not in ["1", "2"]:
                        type = input("Ce type d'opération n'existe pas.\nType d'opération effectuée : ")
                #Si le compte est ouvert, tous types d'opération possible
                else:
                    typeOpe = {"1" : "Guichet", "2" : "Chèque", "3" : "Virement", "4" : "CB"}
                    type = input("Type d'opération effectuée (1 : Guichet, 2 : Chèque, 3 : Virement, 4 : Carte bancaire)\n  ->")
                    while type not in ["1", "2", "3", "4"]:
                        type = input("Ce type d'opération n'existe pas.\nType d'opération effectuée : ")
                #Demande du montant
                montant = int(input("Montant de l'opération (positif pour crédit, négatif pour débit) : "))

                #Gestion des cas d'erreurs liés au type de compte
                if (Typecompte(curseur, date_creation) == 'epargne' and getSoldeCompte(curseur, date_creation) + montant < 300) :
                    print("Impossible d'effectuer l'opération. Il ne peut pas y avoir de compte épargne avec un solde en dessous de 300 €.\nAnnulation de l'opération.")
                    return
                if (Typecompte(curseur, date_creation) == 'revolving' and getSoldeCompte(curseur, date_creation) + montant > 0) :
                    print("Impossible d'effectuer l'opération. Il ne peut pas y avoir de compte revolving au dessus de 0 €.\nAnnulation de l'opération.")
                    return
                if (Typecompte(curseur, date_creation) == 'revolving' and getSoldeCompte(curseur, date_creation) + montant < GetMin(curseur, date_creation)) :
                    print("Impossible d'effectuer l'opération. Il ne peut pas y avoir de compte revolving en dessous du minimum autorisé.\nAnnulation de l'opération.")
                    return
                if (Typecompte(curseur, date_creation) == 'courant' and getSoldeCompte(curseur, date_creation) + montant < -GetDecouvert(curseur, date_creation)) :
                    print("Impossible d'effectuer l'opération. Il ne peut pas y avoir de compte courant en dessus du découvert autorisé.\nAnnulation de l'opération.")
                    return
                if (Typecompte(curseur, date_creation) == 'epargne' and typeOpe[type] not in ['Guichet', 'Virement']):
                    print("Les comptes épargnes ne peuvent faires que des opérations guichet et virment.\nAnnulation de l'opération.")
                    return

                #Traitement des cas particuliers si le compte est bloqué
                if montant < 0 and statut == "bloqué":
                    print("Seules les opérations de crédit sont possibles. Annulation de l'opération.")
                elif statut == "bloqué":
                    etat = "traité"
                    if type == "2":
                        #Ajout de l'opération
                        sql1 = f"INSERT INTO Operation VALUES('{id}', '{date_creation}', '{montant}', CURRENT_DATE(), '{etat}', 'Chèque', 'depot')"
                        #Modification du solde
                        sql2 = f"UPDATE Compte SET solde = '{getSoldeCompte(curseur, date_creation)[0][0] + montant}' WHERE date_creation = '{date_creation}')"

                    else:
                        #Ajout de l'opération
                        sql1 = f"INSERT INTO Operation VALUES('{id}', '{date_creation}', '{montant}', CURRENT_DATE(), '{etat}', '{typeOpe[type]}', NULL)"
                        #Modification du solde
                        sql2 = f"UPDATE Compte SET solde = '{getSoldeCompte(curseur, date_creation)[0][0] + montant}' WHERE date_creation = '{date_creation}')"
                    #Ajout des reqûetes à la BDD
                    try:
                        curseur.execute(sql1)
                        curseur.execute(sql2)
                        curseur.commit()
                        #Mise à jour de la table MinMaxMois
                        UpdateMinMaxMois(curseur, date_creation)

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
                        sql1 = f"INSERT INTO Operation VALUES('{id}', '{date_creation}', '{montant}', CURRENT_DATE(), '{etat}', '{typeOpe[type]}', 'depot')"
                    elif type == "2":
                        sql1 = f"INSERT INTO Operation VALUES('{id}', '{date_creation}', '{montant}', CURRENT_DATE(), '{etat}', '{typeOpe[type]}', 'emission')"
                    else:
                        sql1 = f"INSERT INTO Operation VALUES('{id}', '{date_creation}', '{montant}', CURRENT_DATE(), '{etat}', '{typeOpe[type]}', NULL)"
                    #Modification du solde du compte
                    sql2 = f"UPDATE Compte SET solde = '{getSoldeCompte(curseur, date_creation)[0][0] + montant}' WHERE date_creation = '{date_creation}')"
                    # Ajout dans la BDD
                    try:
                        curseur.execute(sql1)
                        curseur.execute(sql2)
                        curseur.commit()
                        #Mise à jour de la table MinMaxMois
                        UpdateMinMaxMois(curseur, date_creation)
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

def insererAppartenir(curseur):
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
            print("Aucun compte dans la base de données. Veuillez d'abord ajouter un compte.\nAbandon de l'ajout de propriétaire.")
            return
        #Affichage de tous les comptes
        print("Liste des comptes de l'utilisateur choisi (date de création, statut, solde) : ")
        for compte in comptes:
            print(f"{compte[0]}\t{compte[1]}\t{compte[2]}")
        date_creation = input("Date de création du compte où vous voulez être propriétaire (YYYY-MM-DD) : ")
        if date_creation not in [compte[0] for compte in comptes]:
            print("Ce compte n'existe pas. Abandon de l'ajout de propriétaire.")
            return
        #Si id client correct et date de création de compte correcte
        sql = f"""INSERT INTO Appartenir VALUES({id}, 'TO_DATE("{date_creation}", "YYYY-MM-DD")')"""
        try:
            curseur.execute(sql)
            curseur.commit()
        except psycopg2.IntegrityError:
            print("Le client est déjà propriétaire de ce compte !")
            curseur.rollback()
        except psycopg2.errors.UniqueViolation:
            print("Violation d'une contrainte d'unicité. Annulation de la création d'appartenance.")
            curseur.rollback()
        except psycopg2.errors.ForeignKeyViolation:
            print("Violation d'une contrainte de clé étrangère. Annulation de la création d'appartenance. ")
        except:
            print("La création de la relation d'appartenance a échoué.")
            curseur.rollback()
        else:
            print("Ajout de la relation d'appartenance client-compte.")