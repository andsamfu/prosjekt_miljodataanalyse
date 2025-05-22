import pandas as pd
import numpy as np

def load_and_prepare_nilu_data(json_file_path):

    # Last inn data
    df = pd.read_json(json_file_path)
    
    # Konverter 'dateTime' til datetime-format
    df['dateTime'] = pd.to_datetime(df['dateTime'])
    df = df.sort_values('dateTime')
    
    # Lag funksjoner for sesongvariasjoner
    df['DayOfYear'] = df['dateTime'].dt.dayofyear
    df['Month'] = df['dateTime'].dt.month
    df['sin_day'] = np.sin(2 * np.pi * df['DayOfYear'] / 365)
    df['cos_day'] = np.cos(2 * np.pi * df['DayOfYear'] / 365)
    
    return df