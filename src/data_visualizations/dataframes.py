import os
import pandas as pd
import json
import sqlite3

# Juster Pandas' utskriftsinnstillinger
pd.set_option('display.max_columns', None)  # Vis alle kolonner
pd.set_option('display.width', 1000)       # Øk bredden på utskriften

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def build_dataframe_from_json(json_path):
    """
    Bygger en dataframe fra en JSON-fil.
    """
    full_path = os.path.join(project_root, json_path)
    with open(full_path, 'r') as file:
        data = json.load(file)
    return pd.DataFrame(data).head(6)

def build_dataframe_from_db(db_path, table_name):
    """
    Bygger en dataframe fra en database.
    """
    full_path = os.path.join(project_root, db_path)
    conn = sqlite3.connect(full_path)
    query = f"SELECT * FROM {table_name} LIMIT 6"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Bruk relative stier
#nilu_df = build_dataframe_from_json('data/clean/cleaned_data_nilu.json')
#print(nilu_df)

frost_df = build_dataframe_from_db('data/clean/frost.db', 'weather_data')
print(frost_df)
