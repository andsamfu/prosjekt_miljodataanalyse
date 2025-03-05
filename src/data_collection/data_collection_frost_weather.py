import requests
import pandas as pd
import pandasql as ps
import sqlite3
import os
from dotenv import load_dotenv

# Laster inn API-nøkler og andre secrets
load_dotenv()

# Sett inn din egen klient-ID her
client_id = os.getenv('API_KEY_frost')

# Definerer endepunkt for å hente kilder
sources_endpoint = 'https://frost.met.no/sources/v0.jsonld'
latitude = 63.43038
longitude = 10.39355
sources_parameters = {
    'geometry': f'nearest(POINT({longitude} {latitude}))',  # Bruker nearest med koordinater
    'elements': 'mean(air_temperature P1D),sum(precipitation_amount P1D),mean(wind_speed P1D)',
}

# Hent kilder basert på koordinater
sources_response = requests.get(sources_endpoint, params=sources_parameters, auth=(client_id, ''))

if sources_response.status_code == 200:
    sources_data = sources_response.json()
    source_id = sources_data['data'][0]['id']  # Henter den nærmeste kilden
    print(f'Funnet kilde: {source_id}')
else:
    print('Feil ved henting av kilder! Returnert statuskode %s' % sources_response.status_code)
    exit()

# Definerer endepunkt og parametere for å hente observasjoner
observations_endpoint = 'https://frost.met.no/observations/v0.jsonld'
observations_parameters = {
    'sources': source_id,  # Bruker den funnet kilden
    'elements': 'mean(air_temperature P1D),sum(precipitation_amount P1D),mean(wind_speed P1D)',
    'referencetime': '2010-01-01/2019-12-31',  # Tidsperiode fra 2010 til 2019
}

# Utfør en HTTP GET-forespørsel for observasjoner
r = requests.get(observations_endpoint, params=observations_parameters, auth=(client_id, ''))

# Sjekk om forespørselen fungerte, og skriv ut eventuelle feil
json_data = None  # Definer json_data før if-setningen

if r.status_code == 200:
    json_data = r.json()
    data = json_data['data']
    print('Data hentet fra frost.met.no!')
else:
    print('Feil! Returnert statuskode %s' % r.status_code)
    json_data = r.json()  # Hent json_data for å vise feilmeldingen
    if 'error' in json_data:
        print('Melding: %s' % json_data['error']['message'])
        print('Årsak: %s' % json_data['error']['reason'])
    exit()

# Opprett en liste for å lagre observasjonsdataene
dataframes = []
for i in range(len(data)):
    row = pd.DataFrame(data[i]['observations'])
    row['referenceTime'] = data[i]['referenceTime']
    row['sourceId'] = data[i]['sourceId']
    dataframes.append(row)

# Kombinerer alle DataFrames til én
df = pd.concat(dataframes, ignore_index=True)

# Velg relevante kolonner
columns = ['sourceId', 'referenceTime',
           'elementId', 'value', 'unit', 'timeOffset']
df2 = df[columns].copy()

# Konverter tid til datetime-format
df2['referenceTime'] = pd.to_datetime(df2['referenceTime'])

# Filtrer for temperatur, nedbør og vindstyrke
df2 = df2[df2['elementId'].isin(
    ['mean(air_temperature P1D)', 'sum(precipitation_amount P1D)', 'mean(wind_speed P1D)'])]

# Bruk pandasql for å hente data for hver dag
query = """
SELECT 
    DATE(referenceTime) AS date,
    MAX(CASE WHEN elementId = 'mean(air_temperature P1D)' THEN value END) AS mean_air_temperature,
    SUM(CASE WHEN elementId = 'sum(precipitation_amount P1D)' THEN value END) AS total_precipitation,
    MAX(CASE WHEN elementId = 'mean(wind_speed P1D)' THEN value END) AS mean_wind_speed
FROM df2
GROUP BY date
ORDER BY date
"""

# Kjør SQL-spørsmålet
result = ps.sqldf(query, locals())

# Vis resultatet
print(result)

# Lagre resultatet i en SQLite-database
database_file = 'data/raw/raw_api_frost_weather_trondheim_2010_to_2019.db'
conn = sqlite3.connect(database_file)
result.to_sql('weather_data', conn, if_exists='replace', index=False)
conn.close()

print(f"Data lagret i '{database_file}' i tabellen 'weather_data'.")
