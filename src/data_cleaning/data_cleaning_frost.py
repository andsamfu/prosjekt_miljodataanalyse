import sys
import pandas as pd
import json
import os
import numpy as np
import sqlite3

if __name__ == "__main__":
    # Når skriptet kjøres direkte
    from data_validators import *
else:
    # Når skriptet importeres som modul
    from .data_validators import *

def print_dataset_info(df_cleaned, outlier_results, imputation_results):
    """
    Skriver ut informasjon om datasettet i ønsket format.

    Args:
        df_cleaned (pd.DataFrame): Den rensede DataFrame.
        outlier_results (dict): Informasjon om fjernede outliers.
        imputation_results (dict): Informasjon om genererte verdier.

    Returns:
        dict: Informasjon om datasettet.
    """
    # Antall rader i datasettet
    total_rows = len(df_cleaned)

    # Teller antall outliers som er fjernet for hver kolonne
    outliers_count = {col: len(counts) for col, counts in outlier_results.items()}

    # Teller antall genererte verdier per kolonne
    generated_counts = {col: int(imputation_results.get(col, 0)) for col in df_cleaned.columns if col.startswith('generated_')}

    # Utskrift i ønsket format
    print("\nDataset informasjon:")
    print(f"Antall rader i datasettet: {total_rows}\n")

    print("Antall outliers fjernet per verdi:")
    for col, count in outliers_count.items():
        print(f"  - {col}: {count} outliers fjernet")

    print("\nGenererte verdier:")
    for col, count in generated_counts.items():
        print(f"  - {col}: {count} genererte verdier")

    print("\nData renset og lagret i SQLite-database.")

    return {
        "Antall rader": total_rows,
        "Outliers fjernet per kolonne": outliers_count,
        "Genererte verdier per kolonne": generated_counts
    }

def clean_frost_data(json_file, db_file):
    """
    Renser og validerer værdata fra FROST API, og lagrer resultatet i en SQLite-database.

    Args:
        json_file (str): Filsti til JSON-filen med rådata fra FROST API.
        db_file (str): Filsti til SQLite-databasen der rensede data skal lagres.
    """
    # Last inn JSON-data
    with open(json_file, 'r') as file:
        raw_data = json.load(file)

    # Prosesser dataene og konverter til pandas DataFrame
    dataframes = []
    for entry in raw_data:
        if 'observations' in entry and entry['observations']:
            df = pd.DataFrame(entry['observations'])
            df['referenceTime'] = entry['referenceTime']  # Legg til referansetid
            df['sourceId'] = entry['sourceId']  # Legg til kilde-ID
            dataframes.append(df)

    if not dataframes:
        print("Ingen gyldige data funnet i JSON-filen.")
        return

    # Kombiner alle dataframes til én
    df = pd.concat(dataframes, ignore_index=True)

    # Filtrer og omform dataene
    df = df[df['elementId'].isin(['mean(air_temperature P1D)', 'sum(precipitation_amount P1D)', 'mean(wind_speed P1D)'])]
    df['referenceTime'] = pd.to_datetime(df['referenceTime']).dt.strftime('%Y-%m-%d')  # Fjern tidskomponent
    df_pivot = df.pivot_table(index='referenceTime', columns='elementId', values='value', aggfunc='first').reset_index()

    # Gi kolonnene mer beskrivende navn
    df_pivot.rename(columns={
        'mean(air_temperature P1D)': 'mean_air_temperature',
        'sum(precipitation_amount P1D)': 'total_precipitation',
        'mean(wind_speed P1D)': 'mean_wind_speed'
    }, inplace=True)

    # Definer gyldige verdier for værdata basert på klima i Trondheim
    frost_valid_ranges = {
        'mean_air_temperature': (-30, 40),  # Temperatur i Celsius
        'total_precipitation': (0, 250),   # Nedbør i mm
        'mean_wind_speed': (0, 60)         # Vindhastighet i m/s
    }

    # Initialiser validatorer
    missing_validator = MissingValueValidator()  # Validator for manglende verdier
    outlier_validator = OutlierValidator(frost_valid_ranges)  # Validator for uteliggere
    continuity_validator = DateContinuityValidator()  # Validator for datokontinuitet
    imputation_validator = ImputationValidator(n_neighbors=5)  # Validator for imputasjon

    # 1. Sjekk for manglende verdier
    missing_results, df_cleaned = missing_validator.validate(df_pivot)

    # 2. Sjekk og håndter uteliggere
    outlier_results, df_cleaned = outlier_validator.validate(df_cleaned)

    # 3. Sjekk og håndter datokontinuitet
    gap_results, df_cleaned = continuity_validator.validate(df_cleaned)

    # 4. Imputer manglende verdier
    imputation_results, df_cleaned = imputation_validator.validate(df_cleaned)

    # Skriv ut dataset-informasjon
    print_dataset_info(df_cleaned, outlier_results, imputation_results)

    # Lagre de rensede dataene i en SQLite-database
    os.makedirs(os.path.dirname(db_file), exist_ok=True)
    conn = sqlite3.connect(db_file)
    df_cleaned['referenceTime'] = pd.to_datetime(df_cleaned['referenceTime']).dt.strftime('%Y-%m-%d')  # Konverter datoformat
    df_cleaned.to_sql('weather_data', conn, if_exists='replace', index=False)
    conn.close()

    print(f"\nRensede data lagret i '{db_file}' i tabellen 'weather_data'.")

def default_clean_frost_data(project_root):
    """
    Standardfunksjon for å rense FROST-data med forhåndsdefinerte filstier.

    Args:
        project_root (str): Rotmappe for prosjektet.
    """    # Sett opp filstier relativt til prosjektets rotmappe
    json_file = os.path.join(project_root, 'data', 'raw', 'api_frost_weather.json')
    db_file = os.path.join(project_root, 'data', 'clean', 'cleaned_data_frost.db')
    clean_frost_data(json_file, db_file)

# Kjør skriptet direkte
if __name__ == "__main__":
    default_clean_frost_data('')