from datetime import date


def getClients(curseur):
    """Fonction qui renvoie l'ensemble des clients de la BDD"""
    sql = "SELECT id, nom FROM Client"
    curseur.execute(sql)
    clients = curseur.fetchall()
    return clients


def getAllComptes(curseur):
    """Fonction qui renvoie l'ensemble des comptes de la BDD"""
    sql = "SELECT date_creation, statut, solde FROM Compte"
    curseur.execute(sql)
    comptes = curseur.fetchall()
    return comptes


def getComptesUtilisateur(curseur, id):
    """Fonction qui renvoie l'ensemble des comptes d'un utilisateur"""
    sql = f"SELECT date_creation, statut, solde FROM Compte C INNER JOIN Appartenir A ON A.compte = C.date_creation WHERE A.client = {id}"
    curseur.execute(sql)
    comptes = curseur.fetchall()
    return comptes


def getSoldeCompte(curseur, date_creation):
    """Fonction qui rentourne le solde du compte cree à date_creation"""
    sql = f"SELECT solde FROM Compte WHERE date_creation = '{date_creation}'"
    curseur.execute(sql)
    solde = curseur.fetchall()
    if len(solde) == 0:
        return None
    return solde[0][0]


def getInfosCompte(curseur, date_creation):
    """Fonction qui rentourne les informations du compte cree à date_creation"""
    sql = f"""SELECT * FROM Compte WHERE date_creation = '{date_creation}'"""
    curseur.execute(sql)
    compte = curseur.fetchall()
    if len(compte) == 0:
        return None
    return compte


def getNbCheque(curseur, numero, typecheque):
    """Fonction qui retourne le nombre de cheque émis ou depose par un client identifié par son num de tel"""
    type = {"E": "emission", "D": "depose"}
    if typecheque == "D" or typecheque == "E":
        sql = f"SELECT COUNT(*) FROM Operation INNER JOIN Client ON Operation.client = Client.id WHERE Client.telephone = '{numero}' AND Operation.type_operation = 'Cheque' AND Operation.type_cheque = '{type[typecheque]}'"
    else:
        sql = f"SELECT COUNT(*) FROM Operation INNER JOIN Client ON Operation.client = 	Client.id WHERE Client.telephone = '{numero}' AND Operation.type_operation = 'Cheque'"

    curseur.execute(sql)
    compte = curseur.fetchall()
    if len(compte) == 0:
        return None
    return compte[0][0]


def getNbOperation(curseur, numero, type_operation):
    """Fonction qui rentourne le nombre d'operation effectuee par un client identifie par son num de tel pour un type d'operation donne"""
    if type_operation == "Cheque":
        typecheque = input('nombre de cheque emis (E), depose (D) ou les deux (A) ?')
        type = {"E" : "emission", "D" : "depose"}
        getNbCheque(curseur, numero, typecheque)
    sql = f"SELECT COUNT(*) FROM Operation INNER JOIN Client ON Operation.client = Client.id WHERE Client.telephone = '{numero}' AND Operation.type_operation = '{type_operation}'"
    curseur.execute(sql)
    compte = curseur.fetchall()
    if len(compte) == 0:
        return None
    return compte[0][0]


def getMontantOperation(curseur, numero, date):
    """Fonction qui retourne le montant d'une operation a partir du numero de client et de la date de l'operation"""
    sql = f"SELECT montant, type_operation FROM Operation INNER JOIN Client ON Operation.client = Client.id WHERE Client.telephone = '{numero}' AND Operation.date = '{date}'"
    curseur.execute(sql)
    montant = curseur.fetchall()
    if len(montant) == 0:
        return None
    return montant[0][0]


def getHistoriqueOperation(curseur, numero, date1, date2):
    """Fonction qui retourne les montant des operation effectuées entre deux dates données a partir du numero de client """
    sql = f"SELECT Operation.montant, Operation.type_operation, Operation.date FROM Operation INNER JOIN Client ON Operation.client = Client.id WHERE Client.telephone = '{numero}' AND Operation.date >= '{date1}' AND Operation.date <= '{date2}'"
    curseur.execute(sql)
    montant = curseur.fetchall()
    if len(montant) == 0:
        print("Pas d'opération effectuée pour ce client sur cette période.")
    for ligne in montant:
        print(f"Montant : {ligne[0]}     Type d'opération : {ligne[1]}     Date : {ligne[2]}")


def getSommeTotale(curseur, telephone):
    """Fonction qui retourne la somme totale effectuee par un client identifie par son telephone"""
    sql = f"SELECT SUM(ABS(Operation.montant)) FROM Operation INNER JOIN Client ON Operation.client = Client.id WHERE Client.telephone = '{telephone}'"
    curseur.execute(sql)
    montant = curseur.fetchall()
    if len(montant) == 0:
        return None
    return montant[0][0]


def Typecompte(curseur, date_creation):
    """Fonction qui determine le type d'un compte"""
    sql1 = f"SELECT * FROM Compte JOIN CompteCourant ON CompteCourant.compte = Compte.date_creation WHERE date_creation = '{date_creation}'"
    sql2 = f"SELECT * FROM Compte JOIN CompteRevolving ON CompteRevolving.compte = Compte.date_creation WHERE date_creation = '{date_creation}'"
    curseur.execute(sql1)
    compte = curseur.fetchall()
    if len(compte) == 0:
        curseur.execute(sql2)
        compte = curseur.fetchall()
        if len(compte) == 0:
            return "epargne"
        else:
            return "revolving"
    return "courant"


def GetMin(curseur, date_creation):
    """Fonction qui rentourne le min autorse d'un compte revolving"""
    sql = f"SELECT montant_min FROM CompteRevolving WHERE compte = '{date_creation}'"
    curseur.execute(sql)
    compte = curseur.fetchall()
    if len(compte) == 0:
        return None
    return compte[0][0]


def GetDecouvert(curseur, date_creation):
    """Fonction qui rentourne le decouvert autorise d'un compte courant"""
    sql = f"SELECT decouvert_autorise FROM CompteCourant WHERE compte = '{date_creation}'"
    curseur.execute(sql)
    compte = curseur.fetchall()
    if len(compte) == 0:
        return None
    return compte[0][0]


def UpdateMinMaxMois(conn, curseur, date_creation):
    """Fonction qui met à jour le min/max du mois d'un compte, et qui cree une nouvelle isntance si on a change de mois"""
    sql = f"SELECT * FROM MinMaxMois WHERE compte = {date_creation} AND annee = {date.today().year} AND mois = {date.today().month}"
    curseur.execute(sql)
    MinMax = curseur.fetchall()

    # Pas d'instance pour ce mois ci, on la cree
    if len(MinMax) == 0:
        sql = f"INSERT INTO MinMaxMois (annee, min, max, mois, compte) VALUES ({date.today().year}, {getSoldeCompte(curseur, date_creation)}, {getSoldeCompte(curseur, date_creation)}, {date.today().month}, {date_creation})"
        try:
            curseur.execute(sql)
            conn.commit()
        except:
            conn.rollback()
            print("Echec lors de la mise à jour de la table MinMaxMois.")
    # Dejà une instance pour ce mois ci, on la met a jour si necessaire
    else:
        if getSoldeCompte(curseur, date_creation) > MinMax[2]:
            sql = f"UPDATE MinMaxMois SET max = {getSoldeCompte(curseur, date_creation)} WHERE compte = '{date_creation}' AND annee = {date.today().year} AND mois = {date.today().month}"
            try:
                curseur.execute(sql)
                conn.commit()
            except:
                conn.rollback()
                print("Echec lors de la mise à jour de la table MinMaxMois.")

        if getSoldeCompte(curseur, date_creation)[0][0] < MinMax[1]:
            sql = f"UPDATE MinMaxMois SET min = {getSoldeCompte(curseur, date_creation)} WHERE compte = '{date_creation}' AND annee = {date.today().year} AND mois = {date.today().month}"
            try:
                curseur.execute(sql)
                conn.commit()
            except:
                conn.rollback()
                print("Echec lors de la mise à jour de la table MinMaxMois.")


def UpdateStatutCompte(conn, curseur, date_creation, statut):
    """Fonction qui met à jour le statut d'un compte"""

    sql = f"UPDATE Compte SET statut= {statut} WHERE date_creation = '{date_creation}'"
    try:
        curseur.execute(sql)
        conn.commit()
    except:
        conn.rollback()
        print("Echec lors de la mise à jour du statut du Compte.")


def UpdateEtatOperation(conn, curseur, date_creation, etat):
    """Fonction qui met à jour l'état d'une opération d'une donnée effectué par compte donné """

    sql = f"UPDATE Operation SET etat= {etat} WHERE date = '{date}' AND compte = '{date_creation}'"
    try:
        curseur.execute(sql)
        conn.commit()
    except:
        conn.rollback()
        print("Echec lors de la mise à jour de l'état de l'Opération.")
