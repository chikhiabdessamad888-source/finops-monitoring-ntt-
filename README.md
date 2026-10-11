# ⚡ Pipeline FinOps & Optimisation des Coûts Cloud 

Ce dépôt contient le code source, les pipelines d'automatisation et les scripts de simulation pour le projet de stage réalisé dans le cadre du cursus d'ingénieur .

## 🚀 À propos du projet
Le projet vise à concevoir une architecture analytique pour la détection et la remédiation des ressources cloud "zombies" (sous-utilisées) à travers plusieurs environnements (AWS, Azure, Google Cloud).

## 🛠️ Stack Technique
- **Langage :** Python (Pandas, NumPy, Matplotlib, Seaborn)
- **Base de données Cloud :** Snowflake
- **Tableau de bord :** Streamlit 
- **Automatisation & CI/CD :** GitHub Actions (`.github/workflows/`)

## 📂 Structure du Dépôt
- `monitoring_zombies.py` : Script principal de détection et d'analyse des ressources.
- `dataset_finops_powerbi (1).csv` : Jeu de données synthétique (800 ressources).
- `.github/workflows/` : Workflows CI/CD pour l'automatisation et la surveillance continue.

## ⚙️ Utilisation
Pour lancer le tableau de bord interactif en local :
```bash
streamlit run app.py
