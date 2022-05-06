from insertion import *
from connexion import *
from affichage import *


def main():
    """Fonction pricipale"""
    #Connexion à la BDD
    conn, cur = connexion()
    continuer = True
    # Boucle principale
    while continuer:
        afficheMenuPrincipal()
        #Demande du choix de l'utilisateur
        reponse = -1
        #Tant que la réponse n'est pas valide
        while reponse < 1 or reponse > 7:
            print("Veuillez entrer un numéro correct.")
            reponse = int(input("Votre choix : "))

        #Si l'utilisateur choisit l'option d'ajout
        if reponse == 1:
            afficheMenuInsertion()
            repInsertion = -1
            while repInsertion < 1 or repInsertion > 3:
                print("Veuillez entrer un numéro correct.")
                reponse = int(input("Votre choix : "))
            if repInsertion == 1:
                insererClient(cur)
            elif repInsertion == 2:
                afficheMenuInsertionCompte()
                repInsertionCompte = -1
                while repInsertionCompte < 1 or repInsertionCompte > 3:
                    print("Veuillez entrer un numéro correct.")
                    reponse = int(input("Votre choix : "))
                if repInsertionCompte == 1:
                    insererCompteCourant(cur)
                elif repInsertionCompte == 2:
                    insererCompteRevolving(cur)
                elif repInsertionCompte == 3:
                    insererCompteEpargne(cur)
            else:
                insererOperation(cur)
        #Si l'utilisateur choisit l'option de modification
        elif reponse == 2:
            afficheMenuModification()
        #Si l'utilisateur choisit l'option de suppression
        elif reponse == 3:
            afficheMenuSuppression()
            repSuppresion = -1
            while repSuppresion < 1 or repSuppresion > 2:
                print("Veuillez entrer un numéro correct.")
                repSuppresion = int(input("Votre choix : "))
            if repSuppresion == 1:
                print("*** Suppression d'un client")
                supprimerClient(cur)
            elif repSuppresion == 2:
                print("*** Suppression d'un compte ***")
                supprimerCompte(cur)
        # Affichage de la BDD
        elif reponse == 4:
        elif reponse == 5:
            print("*** Solde d'un compte ***")
            date_creation = input("Date de création du compte (YYYY-MM-DD) : ")
            #Montant d'un compte
            solde = getSoldeCompte(cur, date_creation)
            if len(solde) == 0:
                #Compte inexistant
                print("Aucun compte créé à cette date.")
            else:
                print(f"Le solde du compte est de : {solde[0][0]}")
        #Si l'utilisateur veut savoir le nombre d'opération faite sur un compte
        elif reponse == 6:
            print("*** Nombre des chèques émis par un client ***")
            numero = input("Numéro de téléphone du client : ")
            nombreChequeEmis = getNbCheque(cur, numero, "E")
            #Si le numéro de téléphone ne correspond à aucun numéro de la BDD
            if len(nombreChequeEmis) == 0:
                print("Aucun compte avec ce numéro de téléphone")
            else:
                print(f"Le nombre de chèques émis par ce client est de : {nombreChequeEmis[0][0]}")
        #Si l'utilisateur souhaite quitter le programme
        if reponse == 7:
            print("Vous allez quitter le programme.")
            continuer = False
            close(conn)



if __name__ == "__main__":
    main()