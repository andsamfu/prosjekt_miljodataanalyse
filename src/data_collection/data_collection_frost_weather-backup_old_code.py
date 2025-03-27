import requests
import pandas as pd
import pandasql as ps
import sqlite3
import os
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

    def process_data(self, data):
        dataframes = []
        for i in range(len(data)):
            row = pd.DataFrame(data[i]['observations'])
            row['referenceTime'] = data[i]['referenceTime']
            row['sourceId'] = data[i]['sourceId']
            dataframes.append(row)

        df = pd.concat(dataframes, ignore_index=True)
        columns = ['sourceId', 'referenceTime', 'elementId', 'value', 'unit', 'timeOffset']
        df2 = df[columns].copy()
        df2['referenceTime'] = pd.to_datetime(df2['referenceTime'])
        df2 = df2[df2['elementId'].isin(['mean(air_temperature P1D)', 'sum(precipitation_amount P1D)', 'mean(wind_speed P1D)'])]
        return df2

    def run(self):
        self.fetch_sources()
        data = self.fetch_observations()
        processed_data = self.process_data(data)

        query = """
        SELECT 
            DATE(referenceTime) AS date,
            MAX(CASE WHEN elementId = 'mean(air_temperature P1D)' THEN value END) AS mean_air_temperature,
            SUM(CASE WHEN elementId = 'sum(precipitation_amount P1D)' THEN value END) AS total_precipitation,
            MAX(CASE WHEN elementId = 'mean(wind_speed P1D)' THEN value END) AS mean_wind_speed
        FROM processed_data
        GROUP BY date
        ORDER BY date
        """

        result = ps.sqldf(query, locals())
        print(result)

        # Save the result to a SQLite database
        database_file = 'data/raw/api_frost_weather.db'
        conn = sqlite3.connect(database_file)
        result.to_sql('weather_data', conn, if_exists='replace', index=False)
        conn.close()

        print(f"Data lagret i '{database_file}' i tabellen 'weather_data'.")

# Example usage
latitude = 63.43038
longitude = 10.39355
from_date = "2010-01-01"
to_date = "2019-12-31"

# Create an instance of the WeatherDataFetcher class
fetcher = WeatherDataFetcher(latitude, longitude, from_date, to_date)

# Run the data fetching and processing
fetcher.run()
