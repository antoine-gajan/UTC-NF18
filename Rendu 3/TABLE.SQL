CREATE TABLE Client(
id serial primary key,
nom varchar(30) not null,
telephone varchar(10) unique not null,
adresse varchar(50) not null
);

CREATE TYPE Statut AS ENUM ('ouvert', 'ferme', 'bloque');

CREATE TABLE Compte(
date_creation date primary key,
statut Statut not null,
solde decimal not null
);

CREATE TABLE Appartenir(
client integer REFERENCES Client(id),
compte date REFERENCES Compte(date_creation),
PRIMARY KEY (client, compte)
);

CREATE TABLE CompteCourant(
compte date REFERENCES Compte(date_creation) primary key,
date_decouvert date,
decouvert_autorise decimal not null CHECK(decouvert_autorise > 0)
);

CREATE TABLE CompteRevolving(
compte date REFERENCES Compte(date_creation)  primary key,
montant_min decimal not null,
taux_interet_journalier decimal not null CHECK(taux_interet_journalier > 0)
);

CREATE TABLE CompteEpargne(
compte date REFERENCES Compte(date_creation) primary key
);

CREATE TABLE MinMaxMois (
annee int not null,
min int not null,
max int not null,
mois int not null CHECK(mois > 0 and mois < 13),
compte Date not null,
foreign key (compte) references Compte(date_creation),
primary key (annee, mois, compte)
);

Create Type Etat as ENUM('traite', 'non traite', 'en cours');

Create Type TypeOperation as ENUM ('Guichet', 'Cheque', 'CB', 'Virement');

Create Type TypeCheque as  ENUM ('depot', 'emission');

CREATE TABLE Operation(
client int REFERENCES Client(id) NOT NULL,
compte date REFERENCES Compte(date_creation),
montant int NOT NULL,
date date,
etat  Etat NOT NULL,
type_operation TypeOperation NOT NULL,
type_cheque TypeCheque,
PRIMARY KEY (compte, client, date)
);


