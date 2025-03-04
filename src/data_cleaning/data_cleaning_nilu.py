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
    print("JSON-filen ble lastet vellykket.")
except Exception as e:
    print(f"Feil ved lesing av JSON-filen: {e}")
    exit()

# Konverter JSON-data til en Pandas DataFrame
df = pd.json_normalize(data, 'values')

# Vier informasjon om datasettet i sin helhet
print("Antall rader i datasettet:", len(df))
print("Kolonner i datasettet:", df.columns.tolist())

# Sjekk for manglende verdier
missing_values = df.isnull().sum()
print("Manglende verdier i hver kolonne:\n", missing_values)

# Fyll inn manglende verdier i 'value' kolonnen med interpolasjon
df['value'] = df['value'].interpolate(method='linear')

# Rund av verdiene til maks 4 desimaler
df['value'] = df['value'].round(4)
df['coverage'] = df['coverage'].round(4)

# Sjekk for duplikater
duplicates = df.duplicated().sum()
print("Antall duplikater i datasettet:", duplicates)

# Fjern duplikater
df.drop_duplicates(inplace=True)

# Sjekk for uvanlige verdier (f.eks. negative verdier for 'value')
unusual_values = df[df['value'] < 0]
print("Rader med negative verdier for 'value':\n", unusual_values)

# Endre negative verdier til null
df.loc[df['value'] < 0, 'value'] = 0

# Bekreft at negative verdier er fikset
fixed_values = df[df['value'] == 0]
print("Rader med negative verdier er nå fikset:\n", fixed_values)

# Definer stien til katalogen for rensede data
cleaned_dir = os.path.join(project_root, 'data', 'clean')

# Lagre den rensede dataen i en ny JSON-fil
cleaned_json_file = os.path.join(cleaned_dir, 'cleaned_data_nilu.json')
df.to_json(cleaned_json_file, orient='records', lines=True)
print(f"Renset data lagret i '{cleaned_json_file}'")

