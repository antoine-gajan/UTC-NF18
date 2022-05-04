def supprimerClient(cur):
    """Fonction qui supprime un client de la BDD"""
    numero = input("Numéro de téléphone du client : ")
    sql = f"DELETE FROM Client WHERE telephone = {numero}"
    try:
        cur.execute(sql)
        cur.commit()
    except:
        cur.rollback()
        print("Erreur rencontrée. Impossible de supprimer ce client.")

def supprimerCompte(cur):
    """Fonction qui supprime un compte de la BDD"""
    date_creation = input("Date de création du compte : ")
    sql = f"""DELETE FROM Client WHERE date_creation = TO_DATE({date_creation}, "YYYY-MM-DD")"""
    try:
        cur.execute(sql)
        cur.commit()
    except:
        cur.rollback()
        print("Erreur rencontrée. Impossible de supprimer ce compte.")
