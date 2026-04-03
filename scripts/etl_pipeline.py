import pandas as pd
import numpy as np
import os
import sqlite3
from datetime import datetime
from sqlalchemy import create_engine

# ===================== CONFIGURATION =====================
RAW_PATH = 'data/raw/'
PROCESSED_PATH = 'data/processed/'
DB_PATH = 'data/ecommerce.db'

os.makedirs(PROCESSED_PATH, exist_ok=True)

# ===================== FONCTIONS ETL =====================

def extract_data():
    """Charge le dataset principal"""
    file_path = os.path.join(RAW_PATH, 'sales_main.csv')
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Fichier non trouvé : {file_path}")
    
    df = pd.read_csv(file_path)
    print(f"✅ Extraction réussie : {df.shape[0]:,} lignes et {df.shape[1]} colonnes")
    print(f"Colonnes : {df.columns.tolist()}")
    return df


def transform_data(df):
    """Nettoyage + enrichissement des données"""
    df = df.copy()
    
    # 1. Standardisation des noms de colonnes (snake_case)
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    
    # 2. Conversion des types
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
    df['total_price'] = pd.to_numeric(df['total_price'], errors='coerce')
    df['shipping_fee'] = pd.to_numeric(df['shipping_fee'], errors='coerce')
    df['age'] = pd.to_numeric(df['age'], errors='coerce')
    
    # 3. Calcul de Total Price si manquant ou incohérent
    mask = df['total_price'].isna() | (df['total_price'] == 0)
    df.loc[mask, 'total_price'] = df.loc[mask, 'unit_price'] * df.loc[mask, 'quantity']
    
    # 4. Nettoyage des valeurs manquantes
    df['age'] = df['age'].fillna(df['age'].median())
    df['region'] = df['region'].fillna('Unknown')
    df['gender'] = df['gender'].fillna('Unknown')
    
    # 5. Création de features business
    df['order_year'] = df['order_date'].dt.year
    df['order_month'] = df['order_date'].dt.month
    df['order_dayofweek'] = df['order_date'].dt.dayofweek
    
    # Age groups
    df['age_group'] = pd.cut(df['age'], 
                             bins=[0, 25, 35, 50, 100],
                             labels=['18-25', '26-35', '36-50', '51+'])
    
    # Shipping status propre
    df['shipping_status'] = df['shipping_status'].str.strip().str.title()
    
    # 6. RFM basics (on le complétera dans l'EDA)
    # Pour l'instant on garde juste les données brutes nécessaires
    
    # 7. Suppression des doublons (basé sur Customer ID + Order Date + Product)
    initial_rows = len(df)
    df = df.drop_duplicates(subset=['customer_id', 'order_date', 'product_name'])
    print(f"   → {initial_rows - len(df)} doublons supprimés")
    
    print(f"✅ Transformation terminée : {df.shape[0]:,} lignes")
    return df


def create_star_schema(df):
    """Crée des tables dimensionnelles (Star Schema simplifié)"""
    
    # dim_customers
    dim_customers = df[['customer_id', 'gender', 'age', 'age_group', 'region']].drop_duplicates().reset_index(drop=True)
    dim_customers['customer_key'] = range(1, len(dim_customers) + 1)
    
    # dim_products
    dim_products = df[['product_name', 'category']].drop_duplicates().reset_index(drop=True)
    dim_products['product_key'] = range(1, len(dim_products) + 1)
    
    # fact_orders (table de faits)
    fact_orders = df.merge(dim_customers[['customer_id', 'customer_key']], on='customer_id', how='left') \
                    .merge(dim_products[['product_name', 'product_key']], on='product_name', how='left')
    
    fact_orders = fact_orders[[
        'customer_key', 'product_key', 'order_date', 'unit_price', 'quantity',
        'total_price', 'shipping_fee', 'shipping_status', 'order_year', 'order_month'
    ]].copy()
    
    print(f"✅ Star Schema créé :\n"
          f"   - dim_customers : {dim_customers.shape[0]} lignes\n"
          f"   - dim_products  : {dim_products.shape[0]} lignes\n"
          f"   - fact_orders   : {fact_orders.shape[0]} lignes")
    
    return dim_customers, dim_products, fact_orders


def load_data(dim_customers, dim_products, fact_orders):
    """Sauvegarde en CSV + base SQLite"""
    
    # Sauvegarde CSV
    dim_customers.to_csv(os.path.join(PROCESSED_PATH, 'dim_customers.csv'), index=False)
    dim_products.to_csv(os.path.join(PROCESSED_PATH, 'dim_products.csv'), index=False)
    fact_orders.to_csv(os.path.join(PROCESSED_PATH, 'fact_orders.csv'), index=False)
    
    # Sauvegarde dans SQLite
    engine = create_engine(f'sqlite:///{DB_PATH}')
    
    dim_customers.to_sql('dim_customers', engine, if_exists='replace', index=False)
    dim_products.to_sql('dim_products', engine, if_exists='replace', index=False)
    fact_orders.to_sql('fact_orders', engine, if_exists='replace', index=False)
    
    print(f"✅ Données chargées dans :\n"
          f"   - {PROCESSED_PATH} (CSV)\n"
          f"   - {DB_PATH} (SQLite)")


def main():
    """Pipeline complet"""
    print("🚀 Démarrage du Pipeline ETL - E-commerce\n")
    
    start_time = datetime.now()
    
    # Extract → Transform → Star Schema → Load
    df_raw = extract_data()
    df_clean = transform_data(df_raw)
    dim_c, dim_p, fact = create_star_schema(df_clean)
    load_data(dim_c, dim_p, fact)
    
    elapsed = datetime.now() - start_time
    print(f"\n🎉 Pipeline terminé en {elapsed.seconds} secondes !")
    print(f"Base de données disponible : {DB_PATH}")


if __name__ == "__main__":
    main()