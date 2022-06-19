# NF18 - Projet 3 - Gestion de comptes bancaires

Ce projet nous a permis de concevoir une application utilisant une base de données afin de gérer des comptes bancaires.


## Cloner le repository
```
mkdir dossier
git init
git clone https://gitlab.utc.fr/nf18-projet-gestion-de-comptes-bancaires/nf18-projet-gestion-de-comptes-bancaires.git
```


## Créer sa base de données

Dans le terminal psql à installer, il faut d'abord se connecter puis instancier une nouvelle base de données (en local).


```
CREATE DATABASE Banque;
```

Il faut ensuite éxécuter les fichiers TABLE.SQL puis DATA.SQL.
```
\i \chemin_depuis_racine\TABLE.SQL
\i \chemin_depuis_racine\DATA.SQL
```

En cas de problèmes de droits, il est également possible de copier/coller le code dans le terminal.


## Lancer l'application

Avant de lancer l'application, il faut modifier dans le fichier Partie 1/Rendu 4/connexion.py les informations de connexion. Remplacer les informations de connexion avec les votres.

```
HOST = "localhost"
USER = "YOUR_USERNAME"
PASSWORD = "YOUR_PASSWORD"
DATABASE = "banque"
```

Enfin, vous pourrez lancer l'application ;)

---------------------------------------------------------------------
<b>Projet réalisé par BOUZAR Massil - DUBUS Théo - FABRE Esther - GAJAN Antoine <br>
Semestre P22</b>

