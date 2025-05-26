import sys
import os

# Legg til prosjektets src-mappe i sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
sys.path.append(os.path.join(project_root, 'src'))

import pandas as pd
import json
import sqlite3
from data_visualizations.data_visualizations_nilu import get_cleaned_data_path  # Importer funksjonen

# Juster Pandas' utskriftsinnstillinger
pd.set_option('display.max_columns', None)  # Vis alle kolonner
pd.set_option('display.width', 1000)       # Øk bredden på utskriften

def build_dataframe_from_json(json_filename):
    """
    Bygger en dataframe fra en JSON-fil.
    """
    full_path = get_cleaned_data_path(json_filename)  # Bruker den sentrale funksjonen
    with open(full_path, 'r') as file:
        data = json.load(file)
    return pd.DataFrame(data).head(6)

def build_dataframe_from_db(db_filename, table_name):
    """
    Bygger en dataframe fra en database.
    """
    full_path = get_cleaned_data_path(db_filename)  # Bruker den sentrale funksjonen
    conn = sqlite3.connect(full_path)
    query = f"SELECT * FROM {table_name} LIMIT 6"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

