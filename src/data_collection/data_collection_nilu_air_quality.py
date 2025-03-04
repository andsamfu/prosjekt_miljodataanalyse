import requests
import json

# Koordinater for Trondheim
latitude = 63.43038
longitude = 10.39355
radius = 1  # Radius i kilometer

# Definerer tidsperioden for 2009 til 2024 (er ikke mer data enn dette)
fromtime = "2009-01-01"
totime = "2024-12-31"

# URL for å hente døgn data
url = f"https://api.nilu.no/stats/day/{fromtime}/{totime}/{latitude}/{longitude}/{radius}"

# Komponent vi ønsker å filtrere på
# component = "PM2.5"
# URL med times data
# url = f"https://api.nilu.no/aq/historical/{fromtime}/{totime}/{latitude}/{longitude}/{radius}?components={component}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    if data:
        # Lagre dataene som en JSON-fil
        with open('data/raw/raw_api_nilu_air_quality_trondheim_2009_to_2024.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)  # Indentasjon for bedre lesbarhet
        print("Data lagret som 'trondheim_air_quality_pm25_2024.json'")
    else:
        print("Ingen data tilgjengelig for den angitte perioden.")
else:
    print(f"Feil ved henting av data: {response.status_code}")
