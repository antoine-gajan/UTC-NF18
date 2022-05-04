from datetime import date


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
    return solde[0][0]


def getInfosCompte(curseur, date_creation):
    """Fonction qui rentourne les informations du compte crée à date_creation"""
    sql = f"SELECT * FROM Compte WHERE date_creation = {date_creation}"
    compte = curseur.execute(sql)
    return compte


def getNbCheque(curseur, numero, typecheque):
    """Fonction qui rentourne le nombre de chèque émis ou déposé par un client identifié par son num de tel"""
    if typecheque == "D" or typecheque == "E":
        sql = f"SELECT COUNT(*) FROM Operation INNER JOIN Client ON Operation.client = Client.id WHERE Client.telephone = '{numero}' AND Operation.type_operation = 'Chèque' AND Operation.type_cheque = '{typecheque}'"
    else:
        sql = f"SELECT COUNT(*) FROM Operation INNER JOIN Client ON Operation.client = 	Client.id WHERE Client.telephone = '{numero}' AND Operation.type_operation = 'Chèque'"

    compte = curseur.execute(sql)
    return compte


def getNbOperation(curseur, numero, type_operation):
    """Fonction qui rentourne le nombre d'operation effectuée par un client identifié par son num de tel pour un type d'operation donné"""
    if type_operation == "Chèque":
        typecheque = input('nombre de chèque émis (E), deposé (D) ou les deux(A) ?')
        getNbCheque(curseur, numero, typecheque)
    sql = f"SELECT COUNT(*) FROM Operation INNER JOIN Client ON Operation.client = Client.id WHERE Client.telephone = '{numero}' AND Operation.type_operation = '{type_operation}'"
    compte = curseur.execute(sql)
    return compte[0][0]


def getMontantOperation(curseur, numero, date):
    """Fonction qui retourne le montant d'une operation a partir du numero de client et de la date de l'operation"""
    sql = f"SELECT montant, type_operation FROM Operation INNER JOIN Client ON Operation.client = Client.id WHERE Client.telephone = '{numero}' AND Operation.date = {date}"
    montant = curseur.execute(sql)
    return montant[0][0]


def getSommeTotale(curseur, telephone, type_operation):
    """Fonction qui retourne la somme totale effectuée par un client identifié par son telephone"""
    sql = f"SELECT SUM(ABS(Operation.montant)) FROM Operation INNER JOIN Client ON Operation.client = Client.id WHERE Client.telephone = {telephone}"
    montant = curseur.execute(sql)
    return montant[0][0]


def Typecompte(curseur, date_creation):
    """Fonction qui détermine le type d'un compte"""
    sql1 = f"SELECT * FROM Compte JOIN CompteCourant ON CompteCourant.compte = Compte.date_creation WHERE date_creation = {date_creation}"
    sql2 = f"SELECT * FROM Compte JOIN CompteRevolving ON CompteRevolving.compte = Compte.date_creation WHERE date_creation = {date_creation}"
    compte = curseur.execute(sql1)
    if len(compte) == 0:
        compte = curseur.execute(sql2)
        if len(compte) == 0:
            return "epargne"
        else:
            return "revolving"
    return "courant"


def GetMin(curseur, date_creation):
    """Fonction qui rentourne le min autorsé d'un compte revolving"""
    sql = f"SELECT montant_min FROM CompteRevolving WHERE date_creation = {date_creation}"
    compte = curseur.execute(sql)
    return compte[0][0]


def GetDecouvert(curseur, date_creation):
    """Fonction qui rentourne le découvert autorsé d'un compte courant"""
    sql = f"SELECT decouvert_autorise FROM CompteCourant WHERE date_creation = {date_creation}"
    compte = curseur.execute(sql)
    return compte[0][0]


def UpdateMinMaxMois(curseur, date_creation):
    """Fonction qui met à jour le min/max du mois d'un compte, et qui créé une nouvelle isntance si on a changé de mois"""
    sql = f"SELECT * FROM MinMaxMois WHERE compte = {date_creation} AND annee = {date.today().year} AND mois = {date.today().month}"
    MinMax = curseur.execute(sql)

    # Pas d'instance pour ce mois ci, on la crée
    if (len(MinMax) == 0):
        sql = f"INSERT INTO MinMaxMois (annee, min, max, mois, compte) VALUES ({date.today().year}, {getSoldeCompte(curseur, date_creation)[0][0]}, {getSoldeCompte(curseur, date_creation)[0][0]}, {date.today().month}, {date_creation})"
        try:
            curseur.execute(sql)
            curseur.commit()
        except:
            curseur.rollback()

    # Déjà une instance pour ce mois ci, on la met a jour si nécéssaire
    else:
        if (getSoldeCompte(curseur, date_creation)[0][0] > MinMax[2]):
            sql = f"UPDATE MinMaxMois SET max = {getSoldeCompte(curseur, date_creation)[0][0]} WHERE compte = {date_creation} AND annee = {date.today().year} AND mois = {date.today().month}"
            try:
                curseur.execute(sql)
                curseur.commit()
            except:
                curseur.rollback()

        if (getSoldeCompte(curseur, date_creation)[0][0] < MinMax[1]):
            sql = f"UPDATE MinMaxMois SET min = {getSoldeCompte(curseur, date_creation)[0][0]} WHERE compte = {date_creation} AND annee = {date.today().year} AND mois = {date.today().month}"
            try:
                curseur.execute(sql)
                curseur.commit()
            except:
                curseur.rollback()