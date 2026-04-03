# Customer Data Pipeline & Analytics (E-commerce)

**Projet réalisé d'avril à juin 2025**

## 🎯 Objectif
Construire un **pipeline ETL complet** pour collecter, nettoyer et structurer des données e-commerce, réaliser une analyse exploratoire approfondie (EDA), et produire des **dashboards interactifs Power BI** avec des insights actionnables pour les équipes Marketing, Sales et Ops.

## 🛠️ Tech Stack
- **Langage** : Python 3.11
- **Data Manipulation** : Pandas, NumPy
- **Visualisation** : Matplotlib, Seaborn, Plotly
- **Base de données** : SQLite
- **BI Tool** : Power BI Desktop
- **Versioning** : Git + GitHub

## 📁 Structure du projet
```bash
customer-data-pipeline-ecommerce/
├── data/
│   ├── raw/                    ← Données brutes Kaggle
│   └── processed/              ← Données nettoyées + tables dimensionnelles
├── notebooks/
│   ├── 01_ETL_pipeline.ipynb
│   └── 02_EDA_exploratory.ipynb
│   └──    ecommerce.db
├── scripts/
│   └── etl_pipeline.py
├── dashboards/
│   └── Ecommerce_Customer_Analytics.pbix
├── docs/
│   ├── insights_business.md
│   └── figures/                ← Captures d'écran des dashboards
├── README.md
├── requirements.txt

🚀 Pipeline ETL réalisé

Extract : Chargement du dataset principal (sales_main.csv) et tables relationnelles
Transform :
Nettoyage des doublons, valeurs manquantes et types de données
Conversion des dates et création de features business (age_group, order_month, order_year)
Calcul de total_price et standardisation des statuts de livraison
Création d’un star schema simplifié (dim_customers, dim_products, fact_orders)

Load : Sauvegarde en CSV + base SQLite (ecommerce.db)

📊 Analyse Exploratoire (EDA)

Statistiques descriptives et profiling des données
Analyse du CA par région, catégorie et mois
Segmentation clients (âge, genre, RFM)
Calcul du taux de retour et identification des tendances

KPI clés issus de l’EDA :

Chiffre d’affaires total : 4 924 090 $
Nombre de commandes : 3 588
Clients uniques : 292
Panier moyen (AOV) : 1 372,38 $
Taux de retour : 30,5 %

📈 Dashboards Power BI
Un dashboard interactif complet composé de 4 pages :

Executive Summary : KPI globaux, évolution du CA et répartition des statuts de livraison
Customer Analytics : Segmentation clients (âge, genre, RFM), Top 10 clients
Product & Sales Performance : Performance par catégorie/produit avec focus sur le taux de retour
Geographic Insights : Analyse par région (CA et taux de retour)

Mesures DAX créées : Total Revenue, AOV, Return Rate, Recency, Revenue per Customer, etc.
💡 Insights Métier Clés
1. Taux de retour anormalement élevé (30,5 %)
Presque 1 commande sur 3 est retournée. C’est le principal levier d’amélioration identifié.
Recommandations : Audit qualité produit, amélioration des descriptions/photos, contrôle avant expédition.
2. Forte concentration du CA
Seulement 292 clients génèrent près de 5 millions de dollars. Les Top 10 clients représentent une part très importante du CA.
Opportunité : Mise en place d’un programme VIP / Key Account Management.
3. Panier Moyen élevé
Un AOV de 1 372 $ indique un positionnement premium → fort potentiel d’upsell et cross-sell.
4. Segmentation RFM
Présence de clients "Champions" à fidéliser et de nombreux clients inactifs (forte Recency) à réactiver via des campagnes ciblées.
🎯 Recommandations Stratégiques Prioritaires

Réduire le taux de retour sous les 15 % (priorité n°1)
Lancer un programme de fidélité VIP pour les gros clients
Mettre en place des campagnes de réactivation basées sur la segmentation RFM
Optimiser la qualité des produits et la transparence du shipping

Impact business attendu :

+15-20 % de marge en réduisant les retours
+10-15 % de CA grâce à une meilleure rétention

📸 Dashboards Power BI
<img src="dashboards/screenshots/Executive_Summary.png" alt="Executive Summary">
<img src="dashboards/screenshots/Customer_Analytics.png" alt="Customer Analytics">
<img src="dashboards/screenshots/Product_Performance.png" alt="Product Performance">
<img src="dashboards/screenshots/Geographic_Insights.png" alt="Geographic Insights">
🚀 Comment exécuter le projet
Bash# 1. Créer et activer l'environnement
pip install -r requirements.txt

# 2. Lancer le pipeline ETL
python scripts/etl_pipeline.py

# 3. Lancer les notebooks
jupyter notebook
🧠 Ce que j'ai appris

Conception et implémentation d’un pipeline ETL robuste
Modélisation en star schema
Création de mesures DAX avancées dans Power BI
Production d’insights business actionnables à partir de données réelles
Gestion de projet end-to-end (du raw data jusqu’aux recommandations métier)


Auteur : Fresnel Mbouma