from requete import *

def UpdateMinMaxMois(curseur, date_creation):
    """Fonction qui met à jour le min/max du mois d'un compte, et qui créé une nouvelle isntance si on a changé de mois"""
    sql = f"SELECT * FROM MinMaxMois WHERE compte = {date_creation} AND annee = {date.today().year} AND mois = {date.today().month}"
    MinMax = curseur.execute(sql)

    # Pas d'instance pour ce mois ci, on la crée
    if (len(MinMax) == 0):
        sql = f"INSERT INTO MinMaxMois (annee, min, max, mois, compte) VALUES ({date.today().year}, {getSoldeCompte(curseur, date_creation)}, {getSoldeCompte(curseur, date_creation)}, {date.today().month}, {date_creation})"
        try:
            curseur.execute(sql)
            curseur.commit()
        except:
            curseur.rollback()

    # Déjà une instance pour ce mois ci, on la met à jour si nécéssaire
    else:
        if (getSoldeCompte(curseur, date_creation) > MinMax[2]):
            sql = f"UPDATE MinMaxMois SET max = {getSoldeCompte(curseur, date_creation)} WHERE compte = {date_creation} AND annee = {date.today().year} AND mois = {date.today().month}"
            try:
                curseur.execute(sql)
                curseur.commit()
            except:
                curseur.rollback()

        if (getSoldeCompte(curseur, date_creation) < MinMax[1]):
            sql = f"UPDATE MinMaxMois SET min = {getSoldeCompte(curseur, date_creation)} WHERE compte = {date_creation} AND annee = {date.today().year} AND mois = {date.today().month}"
            try:
                curseur.execute(sql)
                curseur.commit()
            except:
                curseur.rollback()
