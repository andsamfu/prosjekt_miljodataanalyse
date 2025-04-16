import pandas as pd
import json
import os
import numpy as np
import sqlite3
from data_validators import MissingValueValidator, ValueRangeValidator, DateContinuityValidator

def clean_frost_data(json_file, db_file):
    # Load the JSON data
    with open(json_file, 'r') as file:
        raw_data = json.load(file)

    # Process the data
    dataframes = []
    for entry in raw_data:
        if 'observations' in entry and entry['observations']:
            df = pd.DataFrame(entry['observations'])
            df['referenceTime'] = entry['referenceTime']
            df['sourceId'] = entry['sourceId']
            dataframes.append(df)

    if not dataframes:
        print("No valid data found in the JSON file.")
        return

    # Combine all dataframes
    df = pd.concat(dataframes, ignore_index=True)

    # Filter and reshape the data
    df = df[df['elementId'].isin(['mean(air_temperature P1D)', 'sum(precipitation_amount P1D)', 'mean(wind_speed P1D)'])]
    df['referenceTime'] = pd.to_datetime(df['referenceTime']).dt.date  # Format date as "YYYY-MM-DD"
    df_pivot = df.pivot_table(index='referenceTime', columns='elementId', values='value', aggfunc='first').reset_index()

    # Rename columns for clarity
    df_pivot.rename(columns={
        'mean(air_temperature P1D)': 'mean_air_temperature',
        'sum(precipitation_amount P1D)': 'total_precipitation',
        'mean(wind_speed P1D)': 'mean_wind_speed'
    }, inplace=True)

    # Define valid ranges for FROST weather data
    frost_valid_ranges = {
        'mean_air_temperature': (-50, 50),
        'total_precipitation': (0, 500),
        'mean_wind_speed': (0, 100)
    }

    # Initialize validators
    missing_validator = MissingValueValidator()
    range_validator = ValueRangeValidator(frost_valid_ranges)
    continuity_validator = DateContinuityValidator()
    
    # Perform validations
    missing_results = missing_validator.validate(df_pivot)
    range_results = range_validator.validate(df_pivot)
    gap_results = continuity_validator.validate(df_pivot)
    
    # Report validation results
    if missing_results:
        print("\nMissing values detected:")
        for column, count in missing_results.items():
            print(f"{column}: {count} missing values")
    
    if range_results:
        print("\nOut of range values detected:")
        for column, values in range_results.items():
            print(f"\n{column}:")
            print(values)
    
    if gap_results:
        print("\nDate gaps detected:")
        for start, end in gap_results:
            print(f"Gap from {start.date()} to {end.date()}")

    # Save to SQLite database
    os.makedirs(os.path.dirname(db_file), exist_ok=True)  # Ensure the directory exists
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS weather_data")  # Explicitly drop the table if it exists
    conn.commit()
    df_pivot.to_sql('weather_data', conn, if_exists='replace', index=False)
    conn.close()

    print(f"Cleaned data saved to '{db_file}' in the table 'weather_data'.")

# Example usage
json_file = os.path.join('data', 'raw', 'api_frost_weather.json')
db_file = os.path.join('data', 'clean', 'frost.db')

clean_frost_data(json_file, db_file)

