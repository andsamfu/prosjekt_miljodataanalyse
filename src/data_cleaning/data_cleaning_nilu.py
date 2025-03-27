import pandas as pd
import json
import os

# Definer prosjektets rotkatalog
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Filsti til JSON-filen
json_file = os.path.join(project_root, 'data', 'raw', 'api_nilu_air_quality.json')

# Les JSON-filen
try:
    with open(json_file, 'r') as file:
        data = json.load(file)
    print("\nJSON-filen ble lastet vellykket.\n")
except Exception as e:
    print(f"Feil ved lesing av JSON-filen: {e}")
    exit()

# Initialiser en tom DataFrame for å samle alle målingene
df_all = pd.DataFrame()

# Iterer gjennom JSON-dataene og bygg DataFrame
for entry in data:
    component = entry['component']
    df_component = pd.json_normalize(entry, 'values')
    df_component['component'] = component
    df_all = pd.concat([df_all, df_component], ignore_index=True)

# Konverter 'dateTime' kolonnen til datetime-format
df_all['dateTime'] = pd.to_datetime(df_all['dateTime'])

# Pivotere DataFrame slik at hver målingstype blir en egen kolonne
df_pivot = df_all.pivot_table(index='dateTime', columns='component', values='value')

# Fjern kolonnen med "Benzo(a)pyrene in PM10 (aerosol)"-verdiene
if 'Benzo(a)pyrene in PM10 (aerosol)' in df_pivot.columns:
    df_pivot.drop(columns=['Benzo(a)pyrene in PM10 (aerosol)'], inplace=True)

# Reindekser DataFrame for å inkludere alle datoer mellom start- og sluttdato
start_date = df_pivot.index.min()
end_date = df_pivot.index.max()
all_dates = pd.date_range(start=start_date, end=end_date, freq='D')
df_pivot = df_pivot.reindex(all_dates)

# Lag en kopi av DataFrame før interpolasjon for å sammenligne senere
df_before_interpolation = df_pivot.copy()

# Fyll inn manglende verdier med interpolasjon
df_pivot = df_pivot.interpolate(method='linear')

# Lag en kolonne som indikerer hvilke verdier som er interpolert
for column in df_pivot.columns:
    df_pivot[f'generated_{column}'] = df_before_interpolation[column].isna() & df_pivot[column].notna()

# Rund av verdiene til maks 4 desimaler
df_pivot = df_pivot.round(4)

# Fjern duplikater
duplicates_before = df_pivot.index.duplicated(keep='first').sum()
df_pivot = df_pivot[~df_pivot.index.duplicated(keep='first')]

# Sjekk for uvanlige verdier (f.eks. negative verdier) og sett dem til null
negative_values_before = (df_pivot < 0).sum().sum()
df_pivot[df_pivot < 0] = 0

# Tell antall genererte verdier for hver kolonne
generated_NO2 = df_pivot['generated_NO2'].sum()
generated_PM10 = df_pivot['generated_PM10'].sum()
generated_PM2_5 = df_pivot['generated_PM2.5'].sum()

# Beregn total antall genererte verdier
total_generated = generated_NO2 + generated_PM10 + generated_PM2_5

# Print informasjon om datasettet
print(f"Antall rader i datasettet: {len(df_pivot)}")
print(f"Antall genererte verdier:")
print(f"  NO2: {generated_NO2}")
print(f"  PM10: {generated_PM10}")
print(f"  PM2.5: {generated_PM2_5}")
print(f"Totalt antall genererte verdier: {total_generated}")
print(f"Antall duplikater før fjerning: {duplicates_before}")
print(f"Antall negative verdier før fjerning: {negative_values_before}")

# Reset index for å inkludere datoene som en kolonne
df_pivot.reset_index(inplace=True)
df_pivot.rename(columns={'index': 'dateTime'}, inplace=True)
df_pivot['dateTime'] = df_pivot['dateTime'].dt.strftime('%Y-%m-%d')

# Definer stien til katalogen for rensede data
cleaned_dir = os.path.join(project_root, 'data', 'clean')

# Lagre den rensede dataen i en ny JSON-fil med lesbare datoer inkludert
cleaned_json_file = os.path.join(cleaned_dir, 'cleaned_data_nilu.json')

# Konverter DataFrame til en liste av ordbøker
data_to_save = df_pivot.to_dict(orient='records')

# Erstatt NaN med None for å lagre som null i JSON
for record in data_to_save:
    for key, value in record.items():
        if pd.isna(value):
            record[key] = None

# Lagre dataen som en JSON-fil med firkantede parenteser
with open(cleaned_json_file, 'w') as json_file:
    json.dump(data_to_save, json_file, indent=4)

print(f"Renset data lagret i '{cleaned_json_file}'")
