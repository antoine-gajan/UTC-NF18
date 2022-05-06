def afficheMenuPrincipal():
    """Fonction qui affiche le menu principal"""
    print("======= GESTION DE COMPTE BANCAIRE =======")
    print("""1. Insertion\n2. Modification\n3. Suppression\n4. Affichage de la base de données\nRequêtes :\n5. Montant d'un compte\n6. Nombre de chèques émis par un client\n7. Quitter""")

def afficheMenuInsertion():
    """Fonction qui affiche le menu d'insertion de données"""
    print("*** Insertion de données ***")
    print("""1. Ajout d'un client\n2. Création d'un compte\n3. Ajout d'une opération sur un compte""")

def afficheMenuModification():
    """Fonction qui affiche le menu de modification de données"""
    print("*** Suppression de données ***")
    print("""1. Suppresion d'un client\n2. Suppresion d'un compte""")

def afficheMenuSuppression():
    """Fonction qui affiche le menu de suppressionde données"""
    print("*** Suppression de données ***")
    print("""1. Suppresion d'un client\n2. Suppresion d'un compte""")

def afficheMenuInsertionCompte():
    """Fonction qui affiche le menu d'insertion de comptes"""
    print("*** Insertion d'un compte ***")
    print("""1. Ajout d'un compte courant\n2. Ajout d'un compte revolving\n3. Ajout d'un compte épargne""")


def afficherTable(cur, table, limite):
    sql = f"SELECT * FROM {table} LIMIT {limite}"
    cur.execute(sql)
    res = cur.fetchall()
    col_names = [attribut[0] for attribut in cur.description]
    string_col = f"{'X':5}"
    for att in col_names:
        string_col += f"{att:30s}"
    print(string_col)
    for i, raw  in enumerate(res):
        string_att = f"{i+1:5}"
        for att in raw:
            string_att += f"{att:30s}"
        print(string_att)

