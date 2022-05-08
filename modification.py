from requete import *

def UpdateMinMaxMois(conn, curseur, date_creation):
    """Fonction qui met à jour le min/max du mois d'un compte, et qui cree une nouvelle isntance si on a change de mois"""
    sql = f"SELECT * FROM MinMaxMois WHERE compte = '{date_creation}' AND annee = {date.today().year} AND mois = {date.today().month}"
    MinMax = curseur.execute(sql)

    # Pas d'instance pour ce mois ci, on la cree
    if (len(MinMax) == 0):
        sql = f"INSERT INTO MinMaxMois (annee, min, max, mois, compte) VALUES ({date.today().year}, {getSoldeCompte(curseur, date_creation)}, {getSoldeCompte(curseur, date_creation)}, {date.today().month}, '{date_creation}')"
        try:
            curseur.execute(sql)
            conn.commit()
        except:
            conn.rollback()

    # Dejà une instance pour ce mois ci, on la met à jour si necessaire
    else:
        if (getSoldeCompte(curseur, date_creation) > MinMax[2]):
            sql = f"UPDATE MinMaxMois SET max = {getSoldeCompte(curseur, date_creation)} WHERE compte = '{date_creation}' AND annee = {date.today().year} AND mois = {date.today().month}"
            try:
                curseur.execute(sql)
                conn.commit()
            except:
                conn.rollback()

        if (getSoldeCompte(curseur, date_creation) < MinMax[1]):
            sql = f"UPDATE MinMaxMois SET min = {getSoldeCompte(curseur, date_creation)} WHERE compte = '{date_creation}' AND annee = {date.today().year} AND mois = {date.today().month}"
            try:
                curseur.execute(sql)
                conn.commit()
            except:
                conn.rollback()
