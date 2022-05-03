def createBDD(curseur):
    """Fonction qui initialise la base de données"""
    #Création des tables
    curseur.execute(open("TABLE.SQL", "r").read())
    #Insertion des données tests
    curseur.execute(open("DATA.SQL", "r").read())

def getClients(curseur):
    """Fonction qui renvoie l'ensemble des clients de la BDD"""
    sql = "SELECT id, nom FROM Client"
    clients = curseur.execute(sql)
    return clients

def getAllComptes(curseur):
    """Fonction qui renvoie l'ensemble des comptes de la BDD"""
    sql = "SELECT date_creation, statut, solde FROM Compte"
    comptes = curseur.execute(sql)
    return comptes

def getComptesUtilisateur(curseur, id):
    """Fonction qui renvoie l'ensemble des comptes d'un utilisateur"""
    sql = f"SELECT date_creation, statut, solde FROM Compte C INNER JOIN Appartenir A ON A.client = C.id WHERE C.id = {id}"
    comptes = curseur.execute(sql)
    return comptes


def getSoldeCompte(curseur, date_creation):
    """Fonction qui rentourne le solde du compte crée à date_creation"""
    sql = f"SELECT solde FROM Compte WHERE date_creation = {date_creation}"
    solde = curseur.execute(sql)
    return solde

def getInfosCompte(curseur, date_creation):
    """Fonction qui rentourne les informations du compte crée à date_creation"""
    sql = f"SELECT * FROM Compte WHERE date_creation = {date_creation}"
    compte = curseur.execute(sql)
    return compte