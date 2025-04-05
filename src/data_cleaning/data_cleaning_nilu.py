import pandas as pd
import json
import os
import numpy as np

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
    except Exception as e:
        print(f"Feil ved lesing av JSON-filen: {e}")
        exit()

# Funksjon for å bygge en DataFrame fra JSON-data
def build_dataframe(data):
    df_all = pd.DataFrame()
    for entry in data:
        component = entry['component']
        df_component = pd.json_normalize(entry, 'values')
        df_component['component'] = component
        df_all = pd.concat([df_all, df_component], ignore_index=True)
    return df_all

# Funksjon for å rense dataen og returnere en renset DataFrame
def clean_data(df_all, column_to_remove):
    
    # Konverter 'dateTime' til datetime-format
    df_all['dateTime'] = pd.to_datetime(df_all['dateTime'])

    # Pivotere DataFrame slik at hver målingstype blir en egen kolonne
    df_pivot = df_all.pivot_table(index='dateTime', columns='component', values='value')

    # Fjern uønsket kolonne
    if column_to_remove in df_pivot.columns:
        df_pivot.drop(columns=[column_to_remove], inplace=True)

    # Fjern outliers basert på standardavvik
    num_std = 3  # Antall standardavvik som definerer outliers
    outliers_removed = {}  # Dictionary for å lagre antall outliers per kolonne
    for column in df_pivot.columns:
        mean = df_pivot[column].mean()
        std = df_pivot[column].std()
        lower_bound = mean - num_std * std
        upper_bound = mean + num_std * std
        # Tell antall verdier som blir outliers
        outliers_removed[column] = ((df_pivot[column] < lower_bound) | (df_pivot[column] > upper_bound)).sum()
        # Sett verdier utenfor [lower_bound, upper_bound] til NaN
        df_pivot[column] = df_pivot[column].where((df_pivot[column] >= lower_bound) & (df_pivot[column] <= upper_bound), np.nan)

    # Reindekser for å inkludere alle datoer
    all_dates = pd.date_range(start=df_pivot.index.min(), end=df_pivot.index.max(), freq='D')
    df_pivot = df_pivot.reindex(all_dates)

    # Lag en kopi før interpolasjon
    df_before_interpolation = df_pivot.copy()

    # Fyll inn manglende verdier med lineær interpolasjon
    df_pivot = df_pivot.interpolate(method='linear')

    # Bruk numpy for å markere interpolerte verdier
    for column in df_pivot.columns:
        df_pivot[f'generated_{column}'] = np.isnan(df_before_interpolation[column]) & ~np.isnan(df_pivot[column])

    # Rund av verdiene til maks 4 desimaler
    df_pivot = df_pivot.round(4)

    # Fjern duplikater
    duplicates_before = df_pivot.index.duplicated(keep='first').sum()
    df_pivot = df_pivot[~df_pivot.index.duplicated(keep='first')]

    # Håndter negative verdier med numpy
    negative_values_before = (df_pivot < 0).sum().sum()
    df_pivot = np.maximum(df_pivot, 0)

    return df_pivot, duplicates_before, negative_values_before, outliers_removed

# Funksjon for å skrive ut informasjon om datasettet
def print_dataset_info(df_pivot, duplicates_before, negative_values_before, outliers_removed):
    
    generated_counts = {col: df_pivot[col].sum() for col in df_pivot.columns if col.startswith('generated_')}
    print(f"Antall rader i datasettet: {len(df_pivot)}")
    print("Antall genererte verdier:")
    for col, count in generated_counts.items():
        print(f"  {col}: {count}")
    print(f"Totalt antall genererte verdier: {sum(generated_counts.values())}")
    print(f"Antall duplikater før fjerning: {duplicates_before}")
    print(f"Antall negative verdier før fjerning: {negative_values_before}")
    print("Antall outliers fjernet per kolonne:")
    for column, count in outliers_removed.items():
        print(f"  {column}: {count}")

# Funksjon for å lagre den rensede dataen i en JSON-fil
def save_cleaned_data(df_pivot, file_path):
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

# Hovedfunksjonen som kjører alle funksjonene
def main():
    data = load_json(raw_json_file)
    df_all = build_dataframe(data)
    df_pivot, duplicates_before, negative_values_before, outliers_removed = clean_data(df_all, column_to_remove)
    print_dataset_info(df_pivot, duplicates_before, negative_values_before, outliers_removed)
    save_cleaned_data(df_pivot, cleaned_json_file)

# Kjør hovedfunksjonen
main()
