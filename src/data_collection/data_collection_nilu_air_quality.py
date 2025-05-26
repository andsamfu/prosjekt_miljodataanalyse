import requests  # For å sende HTTP-forespørsler
import json  # For å håndtere JSON-data

class AirQualityDataFetcher:
    def __init__(self, latitude, longitude, fromtime, totime, radius=20):
        """
        Initialiserer klassen med koordinater, tidsperiode og radius.

        Args:
            latitude (float): Breddegrad for stedet.
            longitude (float): Lengdegrad for stedet.
            fromtime (str): Startdato for data i formatet 'YYYY-MM-DD'.
            totime (str): Sluttdato for data i formatet 'YYYY-MM-DD'.
            radius (int, optional): Radius i kilometer for søket. Standard er 20 km.
        """
        self.latitude = latitude
        self.longitude = longitude
        self.fromtime = fromtime
        self.totime = totime
        self.radius = radius
        # Setter opp URL for API-forespørselen
        self.url = f"https://api.nilu.no/stats/day/{self.fromtime}/{self.totime}/{self.latitude}/{self.longitude}/{self.radius}"

    def fetch_data(self):
        """
        Henter data fra NILU API.

        Returns:
            list: En liste med data hvis forespørselen er vellykket.
            None: Hvis forespørselen mislykkes eller ingen data er tilgjengelig.
        """
        response = requests.get(self.url)  # Sender en GET-forespørsel til API-et
        if response.status_code == 200:  # Sjekker om forespørselen var vellykket
            data = response.json()  # Leser JSON-data fra responsen
            if data:
                return data  # Returnerer data hvis tilgjengelig
            else:
                print("Ingen data tilgjengelig for den angitte perioden.")
                return None
        else:
            print(f"Feil ved henting av data: {response.status_code}")
            return None

    def save_data(self, data, filename):
        """
        Lagrer data som en JSON-fil.

        Args:
            data (list): Data som skal lagres.
            filename (str): Filnavn for lagring.
        """
        # Legger til 'referenceTime' basert på 'dateTime' hvis den ikke finnes
        for record in data:
            for value in record.get('values', []):
                if 'dateTime' in value and 'referenceTime' not in value:
                    value['referenceTime'] = value['dateTime']

        # Lagrer data som en JSON-fil
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)  # Indentasjon for bedre lesbarhet
        print(f"Data lagret som '{filename}'")

    def run(self):
        """
        Kjører hele prosessen for å hente og lagre data.
        """
        data = self.fetch_data()  # Henter data fra API-et
        if data:
            self.save_data(data, 'data/raw/api_nilu_air_quality.json')  # Lagrer data i en JSON-fil

# Initialiserer klassen med de ønskede verdiene
latitude = 63.43038  # Breddegrad for stedet
longitude = 10.39355  # Lengdegrad for stedet
fromtime = "2010-01-01"  # Startdato for data
totime = "2024-12-31"  # Sluttdato for data

# Setter premissene for å hente data
fetcher = AirQualityDataFetcher(latitude, longitude, fromtime, totime)
fetcher.run()  # Kjører prosessen for å hente og lagre data
