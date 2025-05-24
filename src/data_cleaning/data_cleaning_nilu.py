import sys
import os
import pandas as pd
import json
import numpy as np
from sklearn.impute import KNNImputer

if __name__ == "__main__":
    # When running directly
    from data_validators import *
else:
    # When imported as module
    from .data_validators import *

# Filsti til JSON-filene
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
raw_json_file = os.path.join(project_root, 'data', 'raw', 'api_nilu_air_quality.json')
cleaned_json_file = os.path.join(project_root, 'data', 'clean', 'cleaned_data_nilu.json')

# Kolonnen som skal fjernes
column_to_remove = 'Benzo(a)pyrene in PM10 (aerosol)'

def load_json(file_path):
    """
    Laster inn en JSON-fil og returnerer dataen.

    Args:
        file_path (str): Filstien til JSON-filen.

    Returns:
        list: Dataen fra JSON-filen som en liste.
    """
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

def build_dataframe(data):
    """
    Bygger en pandas DataFrame fra JSON-data.

    Args:
        data (list): Dataen fra JSON-filen.

    Returns:
        pd.DataFrame: En DataFrame med dataen.
    """
    df_all = pd.DataFrame()
    for entry in data:
        component = entry.get('component', 'Unknown')  # Henter komponentnavn
        values = entry.get('values', [])  # Henter verdier
        df_component = pd.json_normalize(values)  # Normaliserer JSON-data
        df_component['component'] = component  # Legger til komponentnavn
        df_all = pd.concat([df_all, df_component], ignore_index=True)  # Kombinerer data
    return df_all

def clean_data(df_all, column_to_remove, num_std, n_neighbors):
    """
    Renser dataen ved å fjerne outliers, fylle inn manglende datoer og imputere manglende verdier.

    Args:
        df_all (pd.DataFrame): DataFrame med rådata.
        column_to_remove (str): Kolonnen som skal fjernes.
        num_std (int): Antall standardavvik for å definere outliers.
        n_neighbors (int): Antall naboer for KNN-imputasjon.

    Returns:
        tuple: En tuple med den rensede DataFrame og informasjon om fjernede outliers.
    """
    # Konverterer 'dateTime' til datetime-format
    df_all['dateTime'] = pd.to_datetime(df_all['dateTime'])

    # Kopierer 'dateTime' til 'referenceTime' for kompatibilitet med validatorene
    df_all['referenceTime'] = df_all['dateTime']

    # Lager en pivot-tabell
    df_pivot = df_all.pivot_table(index='dateTime', columns='component', values='value')
    df_pivot = df_pivot.reset_index()  # Beholder 'dateTime' som en kolonne
    df_pivot['referenceTime'] = df_pivot['dateTime']  # Kopierer 'dateTime' til 'referenceTime'

    # Fjerner spesifisert kolonne
    if column_to_remove in df_pivot.columns:
        df_pivot.drop(columns=[column_to_remove], inplace=True)

    # Fyller inn manglende datoer ved hjelp av DateContinuityValidator
    date_validator = DateContinuityValidator()
    missing_dates, df_pivot = date_validator.validate(df_pivot, date_column='referenceTime')

    # Fjerner outliers ved hjelp av OutlierValidator
    valid_ranges = {col: (df_pivot[col].mean() - num_std * df_pivot[col].std(),
                          df_pivot[col].mean() + num_std * df_pivot[col].std()) for col in df_pivot.columns if col not in ['dateTime', 'referenceTime']}
    outlier_validator = OutlierValidator(valid_ranges)
    outliers_removed, df_pivot = outlier_validator.validate(df_pivot)

    # Fyller inn manglende verdier ved hjelp av ImputationValidator
    imputation_validator = ImputationValidator(n_neighbors=n_neighbors)
    imputation_info, df_pivot = imputation_validator.validate(df_pivot)

    return df_pivot, outliers_removed

def print_dataset_info(df_pivot, outliers_removed):
    """
    Skriver ut informasjon om datasettet.

    Args:
        df_pivot (pd.DataFrame): Den rensede DataFrame.
        outliers_removed (dict): Informasjon om fjernede outliers.

    Returns:
        dict: Informasjon om datasettet.
    """
    generated_counts = {col: int(df_pivot[col].sum()) for col in df_pivot.columns if col.startswith('generated_')}
    
    # Teller antall outliers som er fjernet for hver kolonne
    outliers_count = {col: len(counts) for col, counts in outliers_removed.items()}
    
    info = {
        "Antall rader": len(df_pivot),
        "Genererte verdier per kolonne": generated_counts,
        "Outliers fjernet per kolonne": outliers_count
    }

    print("Dataset informasjon:\n")
    print(f"Antall rader i datasettet: {info['Antall rader']}")
    print("\nAntall outliers fjernet per verdi:")
    for col, count in info["Outliers fjernet per kolonne"].items():
        print(f"  - {col}: {count} outliers fjernet")
    print("\nGenererte verdier:")
    for col, count in info["Genererte verdier per kolonne"].items():
        print(f"  - {col}: {count} genererte verdier")
   

    return info

def save_cleaned_data(df_pivot, file_path):
    """
    Lagrer den rensede dataen i en JSON-fil.

    Args:
        df_pivot (pd.DataFrame): Den rensede DataFrame.
        file_path (str): Filstien for lagring av dataen.
    """
    try:
        # Sjekk om DataFrame er tom
        if df_pivot.empty:
            print("Advarsel: DataFrame er tom. Ingen data å lagre.")
            return

        # Lag en kopi av dataframe for å unngå modifikasjoner på original
        df_to_save = df_pivot.copy()
        
        # Sørg for at dateTime er i riktig format og er unik
        if 'dateTime' in df_to_save.columns:
            df_to_save['dateTime'] = pd.to_datetime(df_to_save['dateTime'])

            # Sjekk for duplikater og fjern dem
            duplicates = df_to_save[df_to_save['dateTime'].duplicated()]
            if not duplicates.empty:
                df_to_save = df_to_save.drop_duplicates(subset=['dateTime'], keep='first')
            df_to_save['dateTime'] = df_to_save['dateTime'].dt.strftime('%Y-%m-%d')

        # Fjern referenceTime hvis den finnes siden vi allerede har dateTime
        if 'referenceTime' in df_to_save.columns:
            df_to_save = df_to_save.drop('referenceTime', axis=1)

        # Fjern eventuelle problematiske kolonner som kan forårsake dupliserte nøkler
        problematic_columns = ['index', 'level_0']
        for col in problematic_columns:
            if col in df_to_save.columns:
                df_to_save = df_to_save.drop(col, axis=1)
        
        # Konverter DataFrame til liste av dictionaries
        print("\nKonverterer data til JSON format...")
        data_to_save = []
        for idx, row in df_to_save.iterrows():
            row_dict = {}
            for column in df_to_save.columns:
                value = row[column]
                if pd.isna(value):
                    row_dict[column] = None
                else:
                    row_dict[column] = value
            data_to_save.append(row_dict)

        # Lagre til JSON
        with open(file_path, 'w') as json_file:
            json.dump(data_to_save, json_file, indent=4)
        print(f"Renset data lagret i '{file_path}'")
        
    except Exception as e:
        print(f"Feil ved lagring av data: {str(e)}")
        print("\nDetaljer om feilen:")
        print("DataFrame kolonner:", df_to_save.columns.tolist())
        print("DataFrame første rad:", df_to_save.iloc[0].to_dict() if not df_to_save.empty else "Tom DataFrame")

def main_dc_nilu():
    """
    Hovedfunksjonen som kjører alle funksjonene for datarensing.
    """
    data = load_json(raw_json_file)  # Laster inn rådata fra JSON-fil
    
    df_all = build_dataframe(data)  # Bygger en DataFrame fra rådata
    df_pivot, outliers_removed = clean_data(df_all, column_to_remove, 4, 100)  # Renser dataen
    dataset_info = print_dataset_info(df_pivot, outliers_removed)  # Skriver ut informasjon om datasettet
    save_cleaned_data(df_pivot, cleaned_json_file)  # Lagrer den rensede dataen
    print("\nData rensing fullført")

# Kjører hovedfunksjonen
if __name__ == "__main__":
    main_dc_nilu()
