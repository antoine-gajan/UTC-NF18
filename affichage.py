def afficheMenuPrincipal():
    """Fonction qui affiche le menu principal"""
    print("======= GESTION DE COMPTE BANCAIRE =======")
    print("""1. Insertion\n2. Modification\n3. Suppression\n4. Affichage de la base de donnees\nRequêtes :\n5. Montant d'un compte\n6. Nombre de cheques emis par un client\n7. Quitter""")

def afficheMenuInsertion():
    """Fonction qui affiche le menu d'insertion de donnees"""
    print("*** Insertion de donnees ***")
    print("""1. Ajout d'un client\n2. Creation d'un compte\n3. Ajout d'une operation sur un compte""")

def afficheMenuModification():
    """Fonction qui affiche le menu de modification de donnees"""
    print("*** Suppression de donnees ***")
    print("""1. Suppresion d'un client\n2. Suppresion d'un compte""")

def afficheMenuSuppression():
    """Fonction qui affiche le menu de suppressionde donnees"""
    print("*** Suppression de donnees ***")
    print("""1. Suppresion d'un client\n2. Suppresion d'un compte""")

def afficheMenuInsertionCompte():
    """Fonction qui affiche le menu d'insertion de comptes"""
    print("*** Insertion d'un compte ***")
    print("""1. Ajout d'un compte courant\n2. Ajout d'un compte revolving\n3. Ajout d'un compte epargne""")

def afficherMenuAffichage():
    """Fonction qui affiche le menu d'affichage des tables"""
    print("*** Choix d'une table ***")
    print("Tables disponibles : ")
    print("1.Client\n2.Compte\n3.Appartenir\n4.Operation\n5.MinMaxMois")

def afficherTable(cur, table, limite):
    sql = f"SELECT * FROM {table} LIMIT {limite}"
    cur.execute(sql)
    res = cur.fetchall()
    col_names = [attribut[0] for attribut in cur.description]
    string_col = ""
    for att in col_names:
        string_col += f"{str(att):30s}|"
    print(string_col)
    print(("-"*30 + "|")*len(col_names))
    for i, raw  in enumerate(res):
        string_att = ""
        for att in raw:
            string_att += f"{str(att):30s}|"
        print(string_att)
