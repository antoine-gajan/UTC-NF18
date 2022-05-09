def afficheMenuPrincipal():
    """Fonction qui affiche le menu principal"""
    print("=========== GESTION DE COMPTE BANCAIRE ===========\n")
    print("""*** MODIFICATION ET AFFICHAGE DE LA BASE DE DONNEES ***\n
1. Insertion\n2. Modification\n3. Suppression\n4. Affichage de la base de donnees\n\n*** REQUETES ***\n
5. Montant d'un compte\n6. Nombre de cheques emis par un client\n7. Historique des opérations d'un compte\n8 . Somme des montants des opérations effectuées par un client\n9. Quitter\n""")

def afficheMenuInsertion():
    """Fonction qui affiche le menu d'insertion de donnees"""
    print("*** Insertion de donnees ***")
    print("""1. Ajout d'un client\n2. Creation d'un compte\n3. Ajout d'un propriétaire d'un compte\n4. Ajout d'une operation sur un compte\n""")

def afficheMenuModification():
    """Fonction qui affiche le menu de modification de donnees"""
    print("*** Modification de donnees ***")
    print("""1. Modification d'un client\n2. Modification d'un compte\n""")

def afficheMenuSuppression():
    """Fonction qui affiche le menu de suppressionde donnees"""
    print("*** Suppression de donnees ***")
    print("""1. Suppresion d'un client\n2. Suppresion d'un compte\n3. Suppression de propriétaire de compte""")

def afficheMenuInsertionCompte():
    """Fonction qui affiche le menu d'insertion de comptes"""
    print("*** Insertion d'un compte ***")
    print("""1. Ajout d'un compte courant\n2. Ajout d'un compte revolving\n3. Ajout d'un compte epargne\n""")

def afficherMenuAffichage():
    """Fonction qui affiche le menu d'affichage des tables"""
    print("*** Choix d'une table ***")
    print("Tables disponibles : ")
    print("1.Client\n2.Compte\n3.Appartenir\n4.Operation\n5.MinMaxMois\n")

def afficherTable(cur, table, limite):
    sql = f"SELECT * FROM {table} LIMIT {limite}"
    cur.execute(sql)
    res = cur.fetchall()
    col_names = [attribut[0] for attribut in cur.description]

    print("________"+("_"*31)*len(col_names))
    string_col = f"|{'Ligne':6s}|"
    for att in col_names:
        string_col += f"{str(att):30s}|"
    print(string_col)
    print("|------|"+("-"*30 + "|")*len(col_names))
    for i, raw in enumerate(res):
        string_att = f"|{str(i+1):6s}|"
        for att in raw:
            string_att += f"{str(att):30s}|"
        print(string_att)
    print("▔▔▔▔▔▔▔▔" + ("▔" * 31) * len(col_names))
