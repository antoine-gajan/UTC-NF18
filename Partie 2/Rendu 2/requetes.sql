-- Requêtes sur données test 

-- Connaître les soldes de tous les comptes 
SELECT date_creation, solde FROM Compte;

-- Connaître le statut d’un compte créé à une date donnée 
SELECT statut FROM Compte WHERE date_creation = date_voulue;

-- Connaître l’opération effectuée et le montant de celle-ci par un client à une date précise
SELECT proprietaires->operations->>‘montant’, proprietaires->operations->>‘typeOperation’ FROM Compte C, JSON_ARRAY_ELEMENTS(C.proprietaires) proprietaires WHERE C.date_creation = date  AND proprietaires->operations->>date = date_voulue

-- Connaître la somme totale des montants effectués par un client id par numtel en fonction d’un type d’opération 
SELECT SUM(proprietaires->operations->>montant) FROM Compte C, JSON_ARRAY_ELEMENTS(C.proprietaires) proprietaires WHERE date_creation = date AND proprietaires->operations->>typeOperation = type_voulu; 

-- Historique des opérations réalisées par un client
SELECT proprietaires->operations->>montant, proprietaires->operations->date,  proprietaires->operations->etat, proprietaires->operations->typeOperation FROM Compte C, JSON_ARRAY_ELEMENTS(C.proprietaires) proprietaires WHERE proprietaires->>id = id_voulu;
