

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

def getNbCheque(curseur, numero, typecheque):
    """Fonction qui rentourne le nombre de chèque émis ou déposé par un client identifié par son num de tel"""
if typecheque=="D" or typecheque=="E" :
		sql = f"SELECT COUNT(*) FROM Opération INNER JOIN Client ON Opération.client = Client.id WHERE Client.téléphone = '{numero}' AND Opération.TypeOpération = 'Chèque' AND Opération.TypeChèque = '{typecheque}'"
else :
		sql = f"SELECT COUNT(*) FROM Opération INNER JOIN Client ON Opération.client = 	Client.id WHERE Client.téléphone = '{numero}' AND Opération.TypeOpération = 'Chèque'"
	
compte = curseur.execute(sql)
	return compte
    
    
def getNbOperation(curseur, numero, typeoperation):
	"""Fonction qui rentourne le nombre d'operation effectuée par un client identifié par son num de tel pour un type d'operation donné"""
if typeoperation == 'Chèque':
    	typecheque = input ('nombre de chèque émis (E), deposé (D) ou les deux(A) ?')
    	getNbCheque(curseur, numero, typecheque)
    	 
sql = f"SELECT COUNT(*) FROM Opération INNER JOIN Client ON Opération.client = Client.id WHERE Client.téléphone = '{numero}' AND Opération.TypeOpération = '{typeoperation}'"
compte = curseur.execute(sql)
return compte
    
def getMontantOperation(curseur, numero, date):
    """Fonction qui rentourne le montant d'une operation a partir du numero de client et de la date de l'operation"""
    sql = f"SELECT montant, TypeOpération FROM Opération INNER JOIN Client ON Opération.client = Client.id WHERE Client.téléphone = '{numero}' AND Opération.date = {date}"
    montant = curseur.execute(sql)
    return montant
    
def getSommeTotale (curseur, typeoperation)
"""  la somme totale effectuée par un client id par numtel en fonction d’un type d’opération"""

choix = input('voulez-vous connaitre le montant de votre activité depuis une date précise ? (O/N)')

if choix == 'O':
	date = input('balances la date : (YYYY-MM-DD)')
	if typeoperation == 'Chèque':
    		typecheque = input ('nombre de chèque émis (E), deposé (D) ou les deux(A) ?')
    		getSommeTotale2(curseur, typecheque) #a definir
	sql = f"SELECT SUM(Operation.montant) FROM Opération INNER JOIN Client ON Opération.client = Client.id WHERE Client.téléphone = '{numero}' AND Opération.TypeOpération = '{typeoperation}' AND Date<'{date}'"
	
sql = f"SELECT SUM(Operation.montant) FROM Opération INNER JOIN Client ON Opération.client = Client.id WHERE Client.téléphone = TELEPHONE AND Opération.TypeOpération = TypeOpération"
    montant = curseur.execute(sql)
    return montant





