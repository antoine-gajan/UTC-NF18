import psycopg2
from requete import *
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
        while reponse < 0 or reponse > 7:
            print("Veuillez entrer un numéro correct.")
            reponse = int(input("Votre choix : "))

        #Si l'utilisateur choisit l'option d'ajout
        if reponse == 1:
            afficheMenuInsertion()
            repInsertion = -1
            while repInsertion < 0 or repInsertion > 3:
                print("Veuillez entrer un numéro correct.")
                reponse = int(input("Votre choix : "))

        #Si l'utilisateur souhaite quitter le programme
        if reponse == 7:
            continuer = False

if __name__ == "__main__":
    main()