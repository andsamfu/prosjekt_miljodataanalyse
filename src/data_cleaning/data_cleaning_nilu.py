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
        tuple: En tuple med den rensede DataFrame og alle validering resultater.
    """
    # Konverterer 'dateTime' til datetime-format
    df_all['dateTime'] = pd.to_datetime(df_all['dateTime'])

    # Kopierer 'dateTime' til 'referenceTime' for kompatibilitet med validatorene
    df_all['referenceTime'] = df_all['dateTime']

    # Lager en pivot-tabell
    df_pivot = df_all.pivot_table(index='dateTime', columns='component', values='value')
    df_pivot = df_pivot.reset_index()  # Beholder 'dateTime' som en kolonne
    df_pivot['referenceTime'] = df_pivot['dateTime']  # Kopierer 'dateTime' til 'referenceTime'    # Fjerner spesifisert kolonne
    if column_to_remove in df_pivot.columns:
        df_pivot.drop(columns=[column_to_remove], inplace=True)

    # Initialiser validatorer
    missing_validator = MissingValueValidator()  # Validator for manglende verdier
    outlier_validator = OutlierValidator({})  # Midlertidig, oppdateres under
    continuity_validator = DateContinuityValidator()  # Validator for datokontinuitet
    imputation_validator = ImputationValidator(n_neighbors=n_neighbors)  # Validator for imputasjon

    # 1. Sjekk for manglende verdier
    missing_results, df_pivot = missing_validator.validate(df_pivot)

    # 2. Fyller inn manglende datoer ved hjelp av DateContinuityValidator
    gap_results, df_pivot = continuity_validator.validate(df_pivot, date_column='referenceTime')

    # 3. Fjerner outliers ved hjelp av OutlierValidator
    valid_ranges = {col: (df_pivot[col].mean() - num_std * df_pivot[col].std(),
                          df_pivot[col].mean() + num_std * df_pivot[col].std()) for col in df_pivot.columns if col not in ['dateTime', 'referenceTime']}
    outlier_validator = OutlierValidator(valid_ranges)
    outlier_results, df_pivot = outlier_validator.validate(df_pivot)

    # 4. Fyller inn manglende verdier ved hjelp av ImputationValidator
    imputation_results, df_pivot = imputation_validator.validate(df_pivot)

    return df_pivot, missing_results, outlier_results, gap_results, imputation_results

def print_dataset_info(df_cleaned, missing_results, outlier_results, gap_results, imputation_results):
    """
    Skriver ut informasjon om datasettet i ønsket format.

    Args:
        df_cleaned (pd.DataFrame): Den rensede DataFrame.
        missing_results (dict): Informasjon om manglende verdier.
        outlier_results (dict): Informasjon om fjernede outliers.
        gap_results (list): Informasjon om datohull.
        imputation_results (dict): Informasjon om genererte verdier.

    Returns:
        dict: Informasjon om datasettet.
    """
    # Antall rader i datasettet
    total_rows = len(df_cleaned)

    # Teller antall outliers som er fjernet for hver kolonne
    outliers_count = {col: len(counts) for col, counts in outlier_results.items()}

    # Teller antall genererte verdier per kolonne
    generated_counts = {col: int(df_cleaned[col].sum()) for col in df_cleaned.columns if col.startswith('generated_')}

    # Utskrift i ønsket format
    print(f"Antall rader i datasettet: {total_rows}")

    # Bruk validator rapport-metodene for å vise resultater
    # 1. Manglende verdier
    missing_validator = MissingValueValidator()
    missing_validator.report(missing_results)

    # 2. Outliers 
    outlier_validator = OutlierValidator({})  # Trenger ikke ranges for rapport
    outlier_validator.report(outlier_results)

    # 3. Datohull
    continuity_validator = DateContinuityValidator()
    continuity_validator.report(gap_results)

    # 4. Genererte verdier
    imputation_validator = ImputationValidator()
    imputation_validator.report(imputation_results)

    return {
        "Antall rader": total_rows,
        "Manglende verdier": missing_results,
        "Outliers fjernet per kolonne": outliers_count,
        "Datohull": gap_results,
        "Genererte verdier per kolonne": generated_counts
    }

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

        # Lag en kopi av dataframe for å unngå endringer på original
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
    try:
        # Laster inn rådata fra JSON-fil
        data = load_json(raw_json_file)
    except Exception as e:
        print(f"Feil ved innlasting av JSON-fil: {e}")
        return

    try:
        # Bygger en DataFrame fra rådata
        df_all = build_dataframe(data)
    except Exception as e:
        print(f"Feil ved bygging av DataFrame: {e}")
        return

    try:
        # Renser dataen
        df_pivot, missing_results, outlier_results, gap_results, imputation_results = clean_data(df_all, column_to_remove, 4, 100)
    except Exception as e:
        print(f"Feil under datarensing: {e}")
        return

    try:
        # Skriver ut informasjon om datasettet
        dataset_info = print_dataset_info(df_pivot, missing_results, outlier_results, gap_results, imputation_results)
    except Exception as e:
        print(f"Feil ved utskrift av dataset-informasjon: {e}")
        return

    try:
        # Lagrer den rensede dataen
        save_cleaned_data(df_pivot, cleaned_json_file)
    except Exception as e:
        print(f"Feil ved lagring av renset data: {e}")
        return

    print("\nData rensing fullført")

# Kjører hovedfunksjonen
if __name__ == "__main__":
    try:
        main_dc_nilu()
    except Exception as e:
        print(f"En uventet feil oppstod: {e}")
