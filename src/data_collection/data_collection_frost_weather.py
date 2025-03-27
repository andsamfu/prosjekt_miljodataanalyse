import requests
import os
import json
from dotenv import load_dotenv

class WeatherDataFetcher:
    def __init__(self, latitude, longitude, from_date, to_date):
        load_dotenv()
        self.client_id = os.getenv('API_KEY_frost')
        self.latitude = latitude
        self.longitude = longitude
        self.from_date = from_date
        self.to_date = to_date
        self.sources_endpoint = 'https://frost.met.no/sources/v0.jsonld'
        self.observations_endpoint = 'https://frost.met.no/observations/v0.jsonld'
        self.source_id = None

    # Find den nærmeste værstasjonen
    def fetch_sources(self):
        sources_parameters = {
            'geometry': f'nearest(POINT({self.longitude} {self.latitude}))',
            'elements': 'mean(air_temperature P1D),sum(precipitation_amount P1D),mean(wind_speed P1D)',
        }
        sources_response = requests.get(self.sources_endpoint, params=sources_parameters, auth=(self.client_id, ''))

        if sources_response.status_code == 200:
            sources_data = sources_response.json()
            self.source_id = sources_data['data'][0]['id']  # Get the nearest source
            print(f'Funnet kilde: {self.source_id}')
        else:
            print('Feil ved henting av kilder! Returnert statuskode %s' % sources_response.status_code)
            exit()

    # Hente data fra nærmeste stasjonen
    def fetch_observations(self):
        observations_parameters = {
            'sources': self.source_id,
            'elements': 'mean(air_temperature P1D),sum(precipitation_amount P1D),mean(wind_speed P1D)',
            'referencetime': f'{self.from_date}/{self.to_date}',
        }
        r = requests.get(self.observations_endpoint, params=observations_parameters, auth=(self.client_id, ''))

        if r.status_code == 200:
            json_data = r.json()
            return json_data['data']
        else:
            print('Feil! Returnert statuskode %s' % r.status_code)
            json_data = r.json()
            if 'error' in json_data:
                print('Melding: %s' % json_data['error']['message'])
                print('Årsak: %s' % json_data['error']['reason'])
            exit()

    def run(self):
        self.fetch_sources()
        data = self.fetch_observations()
        
        # Save the original data to a JSON file
        json_file_path = 'data/raw/api_frost_weather.json'
        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        
        print(f"Data lagret i '{json_file_path}' i JSON-format.")

# Example usage
latitude = 63.43038
longitude = 10.39355
from_date = "2010-01-01"
to_date = "2019-12-31"

# Create an instance of the WeatherDataFetcher class
fetcher = WeatherDataFetcher(latitude, longitude, from_date, to_date)

# Run the data fetching and saving
fetcher.run()
