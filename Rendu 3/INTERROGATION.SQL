--Ensemble des id et nom des clients
SELECT id, nom FROM Client;

--renvoie l'ensemble des comptes de la BDD
SELECT date_creation, statut, solde FROM Compte;

--renvoie l'ensemble des comptes d'un utilisateur dont l'id est id
SELECT date_creation, statut, solde FROM Compte C INNER JOIN Appartenir A ON A.compte = C.date_creation WHERE A.client = id;

--renvoie le solde du compte cree � date_creation
SELECT solde FROM Compte WHERE date_creation = 'date_creation';

--renvoie les informations du compte cree � date_creation
SELECT * FROM Compte WHERE date_creation = 'date_creation'

--renvoie le nombre de cheque �mis ou depose par un client identifi� par son numero de tel
SELECT COUNT(*) FROM Operation INNER JOIN Client ON Operation.client = Client.id WHERE Client.telephone = 'numero' AND Operation.type_operation = 'Cheque' AND Operation.type_cheque = 'emission';

--renvoie le montant d'une operation a partir du numero de client et de la date de l'operation
SELECT montant, type_operation FROM Operation INNER JOIN Client ON Operation.client = Client.id WHERE Client.telephone = 'numero' AND Operation.date = 'date';

--renvoie les montant des operation effectu�es entre deux dates d�but et fin donn�es par un client identifi� a partir du numero de client
SELECT Operation.montant, Operation.type_operation, Operation.date FROM Operation INNER JOIN Client ON Operation.client = Client.id WHERE Client.telephone = 'numero' AND Operation.date >= 'debut' AND Operation.date <= 'fin';

--retourne la somme totale effectuee par un client identifie par son telephone
SELECT SUM(ABS(Operation.montant)) FROM Operation INNER JOIN Client ON Operation.client = Client.id WHERE Client.telephone = 'telephone';











