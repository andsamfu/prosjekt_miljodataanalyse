import pandas as pd
import json
import os
import numpy as np
from sklearn.impute import KNNImputer

# Definer prosjektets rotkatalog
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Filsti til JSON-filene
raw_json_file = os.path.join(project_root, 'data', 'raw', 'api_nilu_air_quality.json')
cleaned_json_file = os.path.join(project_root, 'data', 'clean', 'cleaned_data_nilu.json')

# Kolonnen som skal fjernes
column_to_remove = 'Benzo(a)pyrene in PM10 (aerosol)'

# Funksjon for å laste inn JSON-fil og returnere data
def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        print("\nJSON-filen ble lastet vellykket.\n")
        return data
    except FileNotFoundError:
        print(f"Filen '{file_path}' ble ikke funnet.")
        return []
    except json.JSONDecodeError:
        print(f"JSON-filen '{file_path}' har feil format.")
        return []

# Funksjon for å bygge en DataFrame fra JSON-data
def build_dataframe(data):
    df_all = pd.DataFrame()
    for entry in data:
        component = entry.get('component', 'Unknown')
        values = entry.get('values', [])
        df_component = pd.json_normalize(values)
        df_component['component'] = component
        df_all = pd.concat([df_all, df_component], ignore_index=True)
    return df_all

# Funksjon for å fjerne outliers
def remove_outliers(df, num_std=4):
    outliers_removed = {}
    for column in df.columns:
        mean = df[column].mean()
        std = df[column].std()
        lower_bound = mean - num_std * std
        upper_bound = mean + num_std * std
        outliers_removed[column] = ((df[column] < lower_bound) | (df[column] > upper_bound)).sum()
        df[column] = df[column].where((df[column] >= lower_bound) & (df[column] <= upper_bound), np.nan)
    return df, outliers_removed

# Funksjon for å fylle inn manglende verdier med KNN-imputasjon
def impute_missing_values(df, n_neighbors=5):
    imputer = KNNImputer(n_neighbors=n_neighbors)
    df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns, index=df.index)
    return df_imputed

# Funksjon for å rense dataen
def clean_data(df_all, column_to_remove, num_std=4, n_neighbors=5):
    df_all['dateTime'] = pd.to_datetime(df_all['dateTime'])
    df_pivot = df_all.pivot_table(index='dateTime', columns='component', values='value')

    if column_to_remove in df_pivot.columns:
        df_pivot.drop(columns=[column_to_remove], inplace=True)

    df_pivot, outliers_removed = remove_outliers(df_pivot, num_std=num_std)
    all_dates = pd.date_range(start=df_pivot.index.min(), end=df_pivot.index.max(), freq='D')
    df_pivot = df_pivot.reindex(all_dates)

    df_before_imputation = df_pivot.copy()
    df_pivot_imputed = impute_missing_values(df_pivot, n_neighbors=n_neighbors)

    for column in df_pivot.columns:
        df_pivot_imputed[f'generated_{column}'] = np.isnan(df_before_imputation[column])

    df_pivot_imputed[df_pivot.columns] = df_pivot_imputed[df_pivot.columns].round(4)
    return df_pivot_imputed, outliers_removed

# Funksjon for å skrive ut informasjon om datasettet
def print_dataset_info(df_pivot, outliers_removed):
    print("\n=== Dataset Information ===")
    print(f"Antall rader i datasettet: {len(df_pivot)}")
    print("\nGenererte verdier per kolonne:")
    for col in df_pivot.columns:
        if col.startswith('generated_'):
            print(f"  - {col}: {int(df_pivot[col].sum())} genererte verdier")
    print("\nAntall outliers fjernet per kolonne:")
    for col, count in outliers_removed.items():
        print(f"  - {col}: {count} outliers fjernet")
    print("===========================\n")

# Funksjon for å lagre den rensede dataen i en JSON-fil
def save_cleaned_data(df_pivot, file_path):
    try:
        df_pivot.reset_index(inplace=True)
        df_pivot.rename(columns={'index': 'dateTime'}, inplace=True)
        df_pivot['dateTime'] = df_pivot['dateTime'].dt.strftime('%Y-%m-%d')

        data_to_save = df_pivot.to_dict(orient='records')
        for record in data_to_save:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None

        with open(file_path, 'w') as json_file:
            json.dump(data_to_save, json_file, indent=4)
        print(f"Renset data lagret i '{file_path}'")
    except Exception as e:
        print(f"Feil ved lagring av data: {e}")

# Funksjon for å generere mock-data for testing
def generate_mock_data():
    data = [
        {"dateTime": "2025-01-01", "component": "NO2", "value": 20},
        {"dateTime": "2025-01-02", "component": "NO2", "value": 25},
        {"dateTime": "2025-01-01", "component": "PM10", "value": 15},
        {"dateTime": "2025-01-02", "component": "PM10", "value": None},
    ]
    return pd.DataFrame(data)

# Hovedfunksjonen som kjører alle funksjonene
def main():
    data = load_json(raw_json_file)
    df_all = build_dataframe(data)
    df_pivot, outliers_removed = clean_data(df_all, column_to_remove, num_std=4, n_neighbors=5)
    dataset_info = print_dataset_info(df_pivot, outliers_removed)
    print(dataset_info)
    save_cleaned_data(df_pivot, cleaned_json_file)

# Kjør hovedfunksjonen
if __name__ == "__main__":
    main()
