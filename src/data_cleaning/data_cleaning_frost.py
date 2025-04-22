import sys
sys.dont_write_bytecode = True

import pandas as pd
import json
import os
import numpy as np
import sqlite3
from data_validators import MissingValueValidator, OutlierValidator, DateContinuityValidator, ImputationValidator

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
    # Strip time component when initially loading the data
    df['referenceTime'] = pd.to_datetime(df['referenceTime']).dt.strftime('%Y-%m-%d')
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
    outlier_validator = OutlierValidator(frost_valid_ranges)
    continuity_validator = DateContinuityValidator()
    imputation_validator = ImputationValidator(n_neighbors=5)
    
    # 1. Check for missing values
    missing_results, df_cleaned = missing_validator.validate(df_pivot)
    missing_validator.report(missing_results)
    
    # 2. Check and handle outliers
    outlier_results, df_cleaned = outlier_validator.validate(df_cleaned)
    outlier_validator.report(outlier_results)
    
    # 3. Check and handle date continuity
    gap_results, df_cleaned = continuity_validator.validate(df_cleaned)
    continuity_validator.report(gap_results)
    
    # 4. Impute missing values
    imputation_results, df_cleaned = imputation_validator.validate(df_cleaned)
    imputation_validator.report(imputation_results)
    
    # Save the cleaned data including generated_ columns
    os.makedirs(os.path.dirname(db_file), exist_ok=True)
    conn = sqlite3.connect(db_file)
    
    # Convert date format when saving
    df_cleaned['referenceTime'] = pd.to_datetime(df_cleaned['referenceTime']).dt.strftime('%Y-%m-%d')
    df_cleaned.to_sql('weather_data', conn, if_exists='replace', index=False)
    conn.close()

    print(f"\nCleaned data saved to '{db_file}' in the table 'weather_data'.")

# Example usage
json_file = os.path.join('data', 'raw', 'api_frost_weather.json')
db_file = os.path.join('data', 'clean', 'frost.db')

clean_frost_data(json_file, db_file)

