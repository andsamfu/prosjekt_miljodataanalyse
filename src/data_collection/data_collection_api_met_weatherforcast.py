import requests
import json
from datetime import datetime
import pytz

# URL til Yr.no API
url = "https://api.met.no/weatherapi/locationforecast/2.0/compact"

# Sett opp parametere for forespørselen til Trondheim
params = {
    'lat': 63.43,  # Breddegrad for stedet
    'lon': 10.39    # Lengdegrad for stedet
}

# Legg til User-Agent header som kreves av API-en
headers = {
    'User-Agent': 'Skole_prosjekt_NTNU/1.0'
}

# Send forespørselen
response = requests.get(url, params=params, headers=headers)

# Sjekk om forespørselen var vellykket
if response.status_code == 200:
    data = response.json()  # Konverter JSON-responsen til et Python-objekt
    
    # Lagre raw dataen
    with open('data/raw/raw_api_met_weatherforcast_trondheim.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)  # Lagre med 4 mellomrom for bedre lesbarhet
    
    # Ekstraher timeseriene fra dataene
    timeseries = data['properties']['timeseries']
    
    # Fjern uønskede felt fra hver timeserie og konverter tid
    for item in timeseries:
        # Konverter tid fra UTC til Oslo-tid
        utc_time = datetime.fromisoformat(item['time'].replace('Z', '+00:00'))  # Konverter til datetime-objekt
        oslo_tz = pytz.timezone('Europe/Oslo')  # Definer Oslo-tidssone
        oslo_time = utc_time.astimezone(oslo_tz)  # Konverter til Oslo-tid
        item['time'] = oslo_time.strftime('%Y-%m-%dT%H:%M:%S')  # Formater tid som ISO 8601 uten Z
        
        # Hent ut verdier fra 'instant' og 'next_1_hours'
        details = item['data']['instant']['details']
        next_1_hours = item['data'].get('next_1_hours', {})
        
        # Oppdater 'item' med ønskede verdier direkte
        item['air_temperature'] = details['air_temperature']
        item['cloud_area_fraction'] = details['cloud_area_fraction']
        item['relative_humidity'] = details['relative_humidity']
        item['wind_speed'] = details['wind_speed']
        item['symbol_code'] = next_1_hours.get('summary', {}).get('symbol_code', None)  # Hent symbol_code
        
        # Hent 'precipitation_amount' fra 'next_1_hours' og legg til i item
        item['precipitation_amount'] = next_1_hours.get('details', {}).get('precipitation_amount', 0.0)  # Standard til 0.0 hvis ikke tilgjengelig
        
        # Fjern 'data' nøkkelen
        item.pop('data', None)

    # Lagre de modifiserte dataene til en JSON-fil
    with open('data/filtered/filtered_api_met_weatherforcast_trondheim.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)  # Lagre med 4 mellomrom for bedre lesbarhet
    
    print("Dataene er lagret i 'data_yr_weather.json'")
else:
    print(f"Feil ved henting av data: {response.status_code}")
