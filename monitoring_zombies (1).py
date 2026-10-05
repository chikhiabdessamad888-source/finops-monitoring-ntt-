# =============================================================
# Monitoring automatisé des ressources cloud sous-utilisées
# Phase "Operate" du cycle FinOps / Étape 6 "Deployment & Monitoring"
# Stage de première année - NTT DATA
# =============================================================
# Ce script illustre comment la détection des ressources "zombies"
# peut être automatisée et exécutée périodiquement (ex: tâche planifiée
# quotidienne), afin d'assurer une surveillance continue des coûts
# plutôt qu'une analyse ponctuelle unique.
# =============================================================

import pandas as pd
from datetime import datetime

# -------------------------------------------------------------
# Paramètres de la règle métier (identiques à l'analyse initiale)
# -------------------------------------------------------------
SEUIL_COUT_HORAIRE = 1.5       # euros / heure
SEUIL_CPU_PCT = 15             # pourcentage d'utilisation CPU
SEUIL_ALERTE_ECONOMIE = 50000  # seuil (€) déclenchant une alerte "critique"


def charger_donnees(chemin_csv):
    """Charge le dernier export de données de consommation cloud."""
    df = pd.read_csv(chemin_csv)
    df["Creation_Date"] = pd.to_datetime(df["Creation_Date"])
    return df


def detecter_ressources_zombies(df, seuil_cout=SEUIL_COUT_HORAIRE, seuil_cpu=SEUIL_CPU_PCT):
    """Applique la règle métier FinOps de détection du gaspillage."""
    zombies = df[(df["Hourly_Cost"] > seuil_cout) & (df["CPU_Utilization_Pct"] < seuil_cpu)]
    return zombies


def generer_rapport_alerte(zombies):
    """Construit un message d'alerte synthétique, prêt à être envoyé
    par email ou par webhook (Slack, Teams) en conditions réelles."""
    horodatage = datetime.now().strftime("%Y-%m-%d %H:%M")
    nb = len(zombies)
    economie = zombies["Projected_Monthly_Spend"].sum()

    niveau = "CRITIQUE" if economie > SEUIL_ALERTE_ECONOMIE else "INFO"

    message = (
        f"[{niveau}] Rapport de surveillance FinOps — {horodatage}\n"
        f"{'-'*55}\n"
        f"Ressources zombies détectées : {nb}\n"
        f"Économie mensuelle potentielle : {economie:,.2f} €\n"
    )

    if nb > 0:
        top5 = zombies.sort_values("Projected_Monthly_Spend", ascending=False).head(5)
        message += "\nTop 5 ressources à traiter en priorité :\n"
        for _, r in top5.iterrows():
            message += (f"  - {r['Resource_ID']} ({r['Cloud_Provider']}, "
                         f"{r['Resource_Type']}) : {r['Projected_Monthly_Spend']:.2f} €/mois\n")

    return message


def envoyer_alerte(message):
    """Point d'intégration pour une notification réelle.
    En environnement de production, cette fonction enverrait le message
    par email (smtplib) ou vers un canal Slack/Teams (requests + webhook).
    Dans le cadre de ce projet, l'alerte est affichée en console et
    journalisée dans un fichier local."""
    print(message)
    with open("journal_alertes_finops.log", "a", encoding="utf-8") as f:
        f.write(message + "\n" + "=" * 55 + "\n")


def executer_cycle_surveillance(chemin_csv="dataset_finops_powerbi.csv"):
    """Point d'entrée du script : à exécuter périodiquement
    (ex: tâche planifiée quotidienne ou hebdomadaire)."""
    df = charger_donnees(chemin_csv)
    zombies = detecter_ressources_zombies(df)
    message = generer_rapport_alerte(zombies)
    envoyer_alerte(message)


if __name__ == "__main__":
    executer_cycle_surveillance()
