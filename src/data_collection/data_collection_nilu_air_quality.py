import requests
import json

class AirQualityDataFetcher:
    def __init__(self, latitude, longitude, fromtime, totime, radius=20):
        self.latitude = latitude
        self.longitude = longitude
        self.fromtime = fromtime
        self.totime = totime
        self.radius = radius
        self.url = f"https://api.nilu.no/stats/day/{self.fromtime}/{self.totime}/{self.latitude}/{self.longitude}/{self.radius}"

    def fetch_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            data = response.json()
            if data:
                return data
            else:
                print("Ingen data tilgjengelig for den angitte perioden.")
                return None
        else:
            print(f"Feil ved henting av data: {response.status_code}")
            return None

    def save_data(self, data, filename):
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)  # Indentasjon for bedre lesbarhet
        print(f"Data lagret som '{filename}'")

    def run(self):
        data = self.fetch_data()
        if data:
            self.save_data(data, 'data/raw/api_nilu_air_quality.json')

# Initialiserer klassen med de ønskede verdiene
latitude = 63.43038
longitude = 10.39355
fromtime = "2010-01-01"
totime = "2024-12-31"

# Oppretter et objekt av klassen og kjører metoden
fetcher = AirQualityDataFetcher(latitude, longitude, fromtime, totime)
fetcher.run()
