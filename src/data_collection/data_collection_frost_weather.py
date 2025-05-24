import requests
import os
import json
from dotenv import load_dotenv

class WeatherDataFetcher:
    """
    En klasse for å hente værdata fra Frost API basert på geografiske koordinater og tidsperiode.

    Argumenter:
        latitude (float): Breddegrad for ønsket lokasjon.
        longitude (float): Lengdegrad for ønsket lokasjon.
        from_date (str): Startdato for tidsperioden (format: 'YYYY-MM-DD').
        to_date (str): Sluttdato for tidsperioden (format: 'YYYY-MM-DD').
    """
    def __init__(self, latitude, longitude, from_date, to_date):
        load_dotenv()  # Laster inn miljøvariabler fra en .env-fil
        self.client_id = os.getenv('API_KEY_frost')  # API-nøkkel for autentisering
        self.latitude = latitude
        self.longitude = longitude
        self.from_date = from_date
        self.to_date = to_date
        self.sources_endpoint = 'https://frost.met.no/sources/v0.jsonld' 
        self.observations_endpoint = 'https://frost.met.no/observations/v0.jsonld' 
        self.source_id = None  # ID for nærmeste værstasjon

    def fetch_sources(self):
        """
        Henter den nærmeste værstasjonen basert på geografiske koordinater.
        """
        sources_parameters = {
            'geometry': f'nearest(POINT({self.longitude} {self.latitude}))',  # Finner nærmeste punkt
            'elements': 'mean(air_temperature P1D),sum(precipitation_amount P1D),mean(wind_speed P1D)',  # Ønskede elementer
        }
        # Gjør en GET-forespørsel til Frost API for å hente værstasjoner
        sources_response = requests.get(self.sources_endpoint, params=sources_parameters, auth=(self.client_id, ''))

        if sources_response.status_code == 200:
            sources_data = sources_response.json()
            self.source_id = sources_data['data'][0]['id']  # Henter ID for nærmeste værstasjon
            print(f'Funnet kilde: {self.source_id}')
        else:
            print('Feil ved henting av kilder! Returnert statuskode %s' % sources_response.status_code)
            exit()  # Avslutter programmet ved feil

    def fetch_observations(self):
        """
        Henter værdata fra den nærmeste værstasjonen for en gitt tidsperiode.

        Returnerer:
            list: En liste med værdata i JSON-format.
        """
        observations_parameters = {
            'sources': self.source_id,  # ID for værstasjonen
            'elements': 'mean(air_temperature P1D),sum(precipitation_amount P1D),mean(wind_speed P1D)',  # Ønskede elementer
            'referencetime': f'{self.from_date}/{self.to_date}',  # Tidsperiode
            'timeoffsets': 'default'  # Standard tidsforskyvning
        }
        # Gjør en GET-forespørsel til Frost API for å hente observasjoner
        r = requests.get(self.observations_endpoint, params=observations_parameters, auth=(self.client_id, ''))

        if r.status_code == 200:
            json_data = r.json()
            return json_data['data']  # Returnerer værdata
        else:
            print('Feil! Returnert statuskode %s' % r.status_code)
            json_data = r.json()
            if 'error' in json_data:
                print('Melding: %s' % json_data['error']['message'])
                print('Årsak: %s' % json_data['error']['reason'])
            exit()  # Avslutter programmet ved feil

    def run(self):
        """
        Kjører hele prosessen for å hente værdata og lagre dem i en JSON-fil.
        """
        self.fetch_sources()  # Henter nærmeste værstasjon
        data = self.fetch_observations()  # Henter værdata
        
        # Lagrer de hentede dataene i en JSON-fil
        json_file_path = 'data/raw/api_frost_weather.json'
        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        
        print(f"Data lagret i '{json_file_path}' i JSON-format.")

# Eksempel på bruk
latitude = 63.43038  # Breddegrad for Trondheim
longitude = 10.39355  # Lengdegrad for Trondheim
from_date = "2010-01-01"  # Startdato
to_date = "2019-12-31"  # Sluttdato

# Oppretter en instans av WeatherDataFetcher-klassen
fetcher = WeatherDataFetcher(latitude, longitude, from_date, to_date)

# Kjører prosessen for å hente og lagre værdata
fetcher.run()
