-- Création de la table globale Compte


CREATE TYPE Statut AS ENUM ('ouvert', 'ferme', 'bloque');


CREATE TABLE Compte(
date_creation date primary key,
statut Statut not null,
solde decimal not null,
proprietaires JSON,
type_compte JSON
);



-- Insertion de données test


INSERT INTO Compte VALUES (
'2022-05-01', 
'ouvert',
500, 
‘[
{
“id” : 1,
“nom” : "Dupont", 
“prenom” : "Pierre",  
“operations” : [
{
“montant” : -25, 
“date” : “2022-05-12”,
“etat” : “traite”,
“typeOperation” : “Guichet”
},
{
“montant” : 150,
“date” : “2022-05-13”,
“etat” : “traite”, 
“typeOperation” : “Virement”
}
]
},
{
“id” : 3,
“nom” : "Jean", 
“prenom” : "Nemar",  
“operations” : [
{
“montant” : -10, 
“date” : “2022-05-18”, 
“etat” : ”traite”, 
“typeOperation” : “Virement”
}
]
}
]’, 
‘{
“type” : “CompteEpargne”
}’
);



INSERT INTO Compte VALUES (
'2022-05-02', 
'ouvert',
200, 
‘[
{
“id” : 2,
“nom” : "Martin", 
“prenom” : "Hugo",  
“operations” : [
{
“montant” : -70, 
“date” : “2022-05-14”,
“etat” : “traite”,
“typeOperation” : “Guichet”
},
{
“montant” : 15,
“date” : “2022-05-10”,
“etat” : “traite”, 
“typeOperation” : “Virement”
}
]
},
{
“id” : 3,
“nom” : "Jean", 
“prenom” : "Nemar",  
“operations” : [
{
“montant” : 10, 
“date” : “2022-05-20”, 
“etat” : “traite”, 
“typeOperation” : “Cheque”, 
“typeCheque” : “depot”
}
]
}
]’, 
‘{
“type” : "CompteCourant",
“decouvert_autorise” : "200",
“MinMaxMois” : 
{
                        “annee” : 2022,
                        “mois” : 5,
                        “min” : 100,
                        “max” : 500
}
}’
);


INSERT INTO Compte VALUES (
'2022-05-03', 
'ouvert',
-650, 
‘[
{
“id” : 4,
“nom” : "Garcia", 
“prenom” : "Fanny",  
“operations” : [
{
“montant” : 100, 
“date” : “2022-05-12”,
“etat” : “traite”,
“typeOperation” : “Virement”
},
{
“montant” : 150,
“date” : “2022-05-13”,
“etat” : “traite”, 
“typeOperation” : “Guichet”
}
]
},
{
“id” : 3,
“nom” : "Jean", 
“prenom” : "Nemar",  
“operations” : [
{
“montant” : 600, 
“date” : “2022-05-18”, 
“etat” : “traite”, 
“typeOperation” : “Cheque”,
“typeCheque” : “Emission”
}
]
}
]’, 
‘{
“type” : “CompteRevolving”,
“montant_min” : -1500,
“taux_interet_journalier” : 0.6
}’
)
