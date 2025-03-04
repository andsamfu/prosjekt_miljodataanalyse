import pandas as pd
import json
import os

# Definer prosjektets rotkatalog
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Filsti til JSON-filen
json_file = os.path.join(project_root, 'data', 'raw', 'raw_api_nilu_air_quality_trondheim_2009_to_2024.json')

# Les JSON-filen
try:
    with open(json_file, 'r') as file:
        data = json.load(file)
    print("\nJSON-filen ble lastet vellykket.\n")
except Exception as e:
    print(f"Feil ved lesing av JSON-filen: {e}")
    exit()

# Konverter JSON-data til en Pandas DataFrame
df = pd.json_normalize(data, 'values')

# Konverter 'dateTime' kolonnen til datetime-format
df['dateTime'] = pd.to_datetime(df['dateTime'])

# Sett 'dateTime' som indeks
df.set_index('dateTime', inplace=True)

# Fjern 'coverage' kolonnen
df.drop(columns=['coverage'], inplace=True)

# Fjern duplikate etiketter i indeksen
df = df[~df.index.duplicated(keep='first')]

# Vier informasjon om datasettet i sin helhet
print("Antall rader i datasettet:", len(df),"\n")

# Identifiser start- og sluttdato
start_date = df.index.min()
end_date = df.index.max()

# Opprett en komplett tidsserie med alle datoer mellom start- og sluttdato
all_dates = pd.date_range(start=start_date, end=end_date, freq='D')

# Reindekser DataFrame for å inkludere alle datoer
df = df.reindex(all_dates)

# Sjekk antall manglende dager
missing_days = df.isnull().sum().max()
print(f"Antall manglende dager i datasettet: {missing_days}\n")

# Fyll inn manglende verdier i 'value' kolonnen med interpolasjon
df['value'] = df['value'].interpolate(method='linear')

# Rund av verdiene til maks 4 desimaler
df['value'] = df['value'].round(4)

# Sjekk for duplikater
duplicates = df.duplicated().sum()
print("Antall duplikater i datasettet:", duplicates, "\n")

# Fjern duplikater
df.drop_duplicates(inplace=True)

# Sjekk for uvanlige verdier (f.eks. negative verdier for 'value')
unusual_values = df[df['value'] < 0]
print("Rader med negative verdier for 'value':\n", unusual_values, "\n")

# Endre negative verdier til null
df.loc[df['value'] < 0, 'value'] = 0

# Bekreft at negative verdier er fikset
fixed_values = df[df['value'] == 0]
print("Rader med negative verdier er nå fikset!\n")

# Definer stien til katalogen for rensede data
cleaned_dir = os.path.join(project_root, 'data', 'clean')

# Lagre den rensede dataen i en ny JSON-fil med lesbare datoer inkludert
cleaned_json_file = os.path.join(cleaned_dir, 'cleaned_data_nilu.json')
df.reset_index(inplace=True)
df.rename(columns={'index': 'dateTime'}, inplace=True)
df['dateTime'] = df['dateTime'].dt.strftime('%Y-%m-%d')
df.to_json(cleaned_json_file, orient='records', lines=True)
print(f"Renset data lagret i '{cleaned_json_file}'")

