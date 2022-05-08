from insertion import *
from connexion import *
from affichage import *
from suppression import *
from time import sleep


def main():
    """Fonction pricipale"""
    #Connexion à la BDD
    conn, cur = connexion()
    continuer = True
    # Boucle principale
    while continuer:
        afficheMenuPrincipal()
        #Demande du choix de l'utilisateur
        reponse = int(input("Votre choix : "))
        #Tant que la reponse n'est pas valide
        while reponse < 1 or reponse > 7:
            print("Veuillez entrer un numero correct.")
            reponse = int(input("Votre choix : "))

        #Si l'utilisateur choisit l'option d'ajout
        if reponse == 1:
            afficheMenuInsertion()
            repInsertion = int(input("Votre choix : "))
            while repInsertion < 1 or repInsertion > 3:
                print("Veuillez entrer un numero correct.")
                repInsertion = int(input("Votre choix : "))
            if repInsertion == 1:
                insererClient(conn, cur)
                sleep(2)
            elif repInsertion == 2:
                afficheMenuInsertionCompte()
                repInsertionCompte = int(input("Votre choix : "))
                while repInsertionCompte < 1 or repInsertionCompte > 3:
                    print("Veuillez entrer un numero correct.")
                    repInsertionCompte = int(input("Votre choix : "))
                if repInsertionCompte == 1:
                    insererCompteCourant(conn, cur)
                    sleep(2)
                elif repInsertionCompte == 2:
                    insererCompteRevolving(conn, cur)
                    sleep(2)
                elif repInsertionCompte == 3:
                    insererCompteEpargne(conn, cur)
                    sleep(2)
            else:
                insererOperation(conn, cur)
                sleep(2)
        #Si l'utilisateur choisit l'option de modification
        elif reponse == 2:
            afficheMenuModification()
            repModification = int(input("Votre choix : "))
            while repModification < 1 or repModification > 2:
                print("Veuillez entrer un numero correct.")
                repSuppresion = int(input("Votre choix : "))

        #Si l'utilisateur choisit l'option de suppression
        elif reponse == 3:
            afficheMenuSuppression()
            repSuppresion = int(input("Votre choix : "))
            while repSuppresion < 1 or repSuppresion > 2:
                print("Veuillez entrer un numero correct.")
                repSuppresion = int(input("Votre choix : "))
            if repSuppresion == 1:
                print("*** Suppression d'un client")
                supprimerClient(conn, cur)
                sleep(2)
            elif repSuppresion == 2:
                print("*** Suppression d'un compte ***")
                supprimerCompte(conn, cur)
                sleep(2)
        # Affichage de la BDD
        elif reponse == 4:
            dico_tables = {"1" : "Client", "2" : "Compte", "3" : "Appartenir", "4" : "Operation", "5" : "MinMaxMois"}
            afficherMenuAffichage()
            repAffiche = input("Entrez le numero correspondant à une table : ")
            while (repAffiche not in [str(num) for num in range(1,6)]):
                repAffiche = input("Numero invalide. Veuillez entrer un numero de table valide : ")
            nb_resultats = int(input("Nombre de résultats souhaités : "))
            while nb_resultats < 0:
                nb_resultats = int(input("Nombre de résultats souhaités : "))
            afficherTable(cur, dico_tables[repAffiche], nb_resultats)
            sleep(2)
        elif reponse == 5:
            print("*** Solde d'un compte ***")
            date_creation = input("Date de creation du compte (YYYY-MM-DD) : ")
            #Montant d'un compte
            solde = getSoldeCompte(cur, date_creation)
            if solde is None:
                #Compte inexistant
                print("Aucun compte cree à cette date.")
            else:
                print(f"Le solde du compte est de : {solde}")
            sleep(2)
        #Si l'utilisateur veut savoir le nombre d'operation faite sur un compte
        elif reponse == 6:
            print("*** Nombre des cheques emis par un client ***")
            numero = input("Numero de telephone du client : ")
            nombreChequeEmis = getNbCheque(cur, numero, "E")
            #Si le numero de telephone ne correspond à aucun numero de la BDD
            if nombreChequeEmis is None:
                print("Aucun compte avec ce numero de telephone")
            else:
                print(f"Le nombre de cheques emis par ce client est de : {nombreChequeEmis}")
            sleep(2)
        #Si l'utilisateur souhaite quitter le programme
        elif reponse == 7:
            print("Vous allez quitter le programme.")
            continuer = False
            close(conn)
            sleep(2)

if __name__ == "__main__":
    main()
