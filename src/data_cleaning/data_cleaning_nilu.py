import pandas as pd
import json
import os
import numpy as np

# Definer prosjektets rotkatalog
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Filsti til JSON-filene
raw_json_file = os.path.join(project_root, 'data', 'raw', 'raw_api_nilu_air_quality_trondheim_2010_to_2024.json')
cleaned_json_file = os.path.join(project_root, 'data', 'clean', 'cleaned_data_nilu.json')

# Kolonnen som skal fjernes
column_to_remove = 'Benzo(a)pyrene in PM10 (aerosol)'

# Les JSON-filen
try:
    with open(raw_json_file, 'r') as file:
        data = json.load(file)
    print("\nJSON-filen ble lastet vellykket.\n")
except Exception as e:
    print(f"Feil ved lesing av JSON-filen: {e}")
    exit()

# Initialiser en tom DataFrame
df_all = pd.DataFrame()

# Bygg DataFrame fra JSON-data
for entry in data:
    component = entry['component']
    df_component = pd.json_normalize(entry, 'values')
    df_component['component'] = component
    df_all = pd.concat([df_all, df_component], ignore_index=True)

# Konverter 'dateTime' til datetime-format
df_all['dateTime'] = pd.to_datetime(df_all['dateTime'])

# Pivotere DataFrame slik at hver målingstype blir en egen kolonne
df_pivot = df_all.pivot_table(index='dateTime', columns='component', values='value')

# Fjern uønsket kolonne
df_pivot.drop(columns=[column_to_remove], errors='ignore', inplace=True)

# Reindekser for å inkludere alle datoer
all_dates = pd.date_range(start=df_pivot.index.min(), end=df_pivot.index.max(), freq='D')
df_pivot = df_pivot.reindex(all_dates)

# Lag en kopi før interpolasjon
df_before_interpolation = df_pivot.copy()

# Fyll inn manglende verdier med lineær interpolasjon
df_pivot = df_pivot.interpolate(method='linear')

# Bruk numpy for å markere interpolerte verdier
generated_values = np.isnan(df_before_interpolation) & ~np.isnan(df_pivot)
generated_columns = {col: f'generated_{col}' for col in df_pivot.columns}
df_pivot = df_pivot.assign(**{new_col: generated_values[col] for col, new_col in generated_columns.items()})

# Rund av verdiene til maks 4 desimaler
df_pivot = df_pivot.round(4)

# Fjern duplikater
duplicates_before = df_pivot.index.duplicated(keep='first').sum()
df_pivot = df_pivot[~df_pivot.index.duplicated(keep='first')]

# Håndter negative verdier med numpy
negative_values_before = (df_pivot < 0).sum().sum()
df_pivot = np.maximum(df_pivot, 0)

# Tell antall genererte verdier for hver kolonne
generated_counts = {col: df_pivot[f'generated_{col}'].sum() for col in df_pivot.columns if col.startswith('generated_')}

# Print informasjon om datasettet
print(f"Antall rader i datasettet: {len(df_pivot)}")
print("Antall genererte verdier:")
for col, count in generated_counts.items():
    print(f"  {col}: {count}")
print(f"Totalt antall genererte verdier: {sum(generated_counts.values())}")
print(f"Antall duplikater før fjerning: {duplicates_before}")
print(f"Antall negative verdier før fjerning: {negative_values_before}")

# Reset index for å inkludere datoene som en kolonne
df_pivot.reset_index(inplace=True)
df_pivot.rename(columns={'index': 'dateTime'}, inplace=True)
df_pivot['dateTime'] = df_pivot['dateTime'].dt.strftime('%Y-%m-%d')

# Konverter DataFrame til JSON-vennlig format
data_to_save = df_pivot.to_dict(orient='records')

# Erstatt NaN med None for å lagre som null i JSON
for record in data_to_save:
    for key, value in record.items():
        if pd.isna(value):
            record[key] = None

# Lagre den rensede dataen
with open(cleaned_json_file, 'w') as json_file:
    json.dump(data_to_save, json_file, indent=4)

print(f"Renset data lagret i '{cleaned_json_file}'")
