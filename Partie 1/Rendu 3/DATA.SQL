INSERT INTO Compte (date_creation, statut, solde)
VALUES ('2022-05-01', 'ferme', 300);
INSERT INTO Compte (date_creation, statut, solde)
VALUES ('2022-05-02', 'ouvert', 1006);
INSERT INTO Compte (date_creation, statut, solde)
VALUES ('2022-05-03', 'ouvert', 100);
INSERT INTO Compte (date_creation, statut, solde)
VALUES ('2022-05-04', 'ouvert', -10);
INSERT INTO Compte (date_creation, statut, solde)
VALUES ('2022-05-05', 'ferme', 908.68);
INSERT INTO Compte (date_creation, statut, solde)
VALUES ('2022-05-06', 'ferme', -70.27);
INSERT INTO Compte (date_creation, statut, solde)
VALUES ('2022-05-07', 'bloque', 46);
INSERT INTO Compte (date_creation, statut, solde)
VALUES ('2022-05-08', 'bloque', 49.99);
INSERT INTO Compte (date_creation, statut, solde)
VALUES ('2022-05-09', 'bloque', 400000);


INSERT INTO Client (nom, telephone, adresse) VALUES('jean', '0123456789', '3 rue de utc');
INSERT INTO Client (nom, telephone, adresse) VALUES('antoine', '9876543210', '5 rue du chateau');
INSERT INTO Client (nom, telephone, adresse) VALUES('theo', '7410258963', '2 rue du caillou');
INSERT INTO Client (nom, telephone, adresse) VALUES('esther', '159856325', '25 rue de la grande allee');
INSERT INTO Client (nom, telephone, adresse) VALUES('massil', '0655555555', '80 rue de payut');
INSERT INTO Client (nom, telephone, adresse) VALUES('clement', '0327859687', 'chez moi');
INSERT INTO Client (nom, telephone, adresse) VALUES('hortense', '3571458625', '56 rue du parc');
INSERT INTO Client (nom, telephone, adresse) VALUES('martin', '5232014584', '36 rue gildas auto');
INSERT INTO Client (nom, telephone, adresse) VALUES('pierre', '0854715632', '6 rue Henry au lait');
INSERT INTO Client (nom, telephone, adresse) VALUES('sacha', '0170210836', '12 rue du pont neuf');




INSERT INTO Appartenir (client, compte) VALUES(6, '2022-05-01');
INSERT INTO Appartenir (client, compte) VALUES(1, '2022-05-01');
INSERT INTO Appartenir (client, compte) VALUES(9, '2022-05-02');
INSERT INTO Appartenir (client, compte) VALUES(8, '2022-05-03');
INSERT INTO Appartenir (client, compte) VALUES(5, '2022-05-04');
INSERT INTO Appartenir (client, compte) VALUES(10, '2022-05-05');
INSERT INTO Appartenir (client, compte) VALUES(2, '2022-05-08');
INSERT INTO Appartenir (client, compte) VALUES(2, '2022-05-09');
INSERT INTO Appartenir (client, compte) VALUES(7, '2022-05-04');
INSERT INTO Appartenir (client, compte) VALUES(7, '2022-05-05');
INSERT INTO appartenir (client, compte) VALUES(10, '2022-05-01');
INSERT INTO Appartenir (client, compte) VALUES(3, '2022-05-06');
INSERT INTO Appartenir (client, compte) VALUES(4, '2022-05-07');


INSERT INTO comptecourant (compte, date_decouvert, decouvert_autorise) VALUES('2022-05-07', '2022-06-01', 100);


INSERT INTO comptecourant (compte, date_decouvert, decouvert_autorise) VALUES('2022-05-08', '2022-06-08', 200);


INSERT INTO comptecourant (compte, date_decouvert, decouvert_autorise) VALUES('2022-05-03', '2022-06-15', 1000);


INSERT INTO compterevolving (compte, montant_min, taux_interet_journalier) VALUES('2022-05-06', -150,0.4);
INSERT INTO compterevolving (compte, montant_min, taux_interet_journalier) VALUES('2022-05-04', -3000, 1);


INSERT INTO compteepargne (compte) VALUES('2022-05-09');
INSERT INTO compteepargne (compte) VALUES('2022-05-05');
INSERT INTO compteepargne (compte) VALUES('2022-05-02');
INSERT INTO compteepargne (compte) VALUES('2022-05-01');




INSERT INTO MinMaxMois VALUES(2022, 220, 340, 5, '2022-05-01');
INSERT INTO MinMaxMois VALUES(2022, 800, 1220, 5, '2022-05-02');
INSERT INTO MinMaxMois VALUES (2022, 99, 101, 5, '2022-05-03');
INSERT INTO MinMaxMois VALUES(2022, -20, 11, 5, '2022-05-04');
INSERT INTO MinMaxMois VALUES(2022, 900, 910, 5, '2022-05-05');
INSERT INTO MinMaxMois VALUES(2022, -100, -50, 5, '2022-05-06');
INSERT INTO MinMaxMois VALUES(2022, 40, 50, 5, '2022-05-07');
INSERT INTO MinMaxMois VALUES(2022, 49, 50, 5, '2022-05-08');
INSERT INTO MinMaxMois VALUES (2022, 1550, 500000, 5, '2022-05-094');






INSERT INTO operation (client, compte, montant, date, etat, type_operation, type_cheque) VALUES (1, '2022-05-02', -25.23, '2022-05-03', 'traite', 'Guichet', NULL);
INSERT INTO operation (client, compte, montant, date, etat, type_operation, type_cheque) VALUES (1, '2022-05-03', 55.23, '2022-05-04', 'non traite', 'Cheque', 'depot');
INSERT INTO operation (client, compte, montant, date, etat, type_operation, type_cheque) VALUES (1, '2022-05-04', -22.13, '2022-05-05', 'en cours', 'Virement', NULL);

UPDATE Compte SET solde = 980.77 WHERE date_creation = '2022-05-02';
UPDATE Compte SET solde = 155.23 WHERE date_creation = '2022-05-03';
UPDATE Compte SET solde = -33.23 WHERE date_creation = '2022-05-04';