import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

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

def split_nilu_data(df, split_ratio=0.75):
    split_point = int(len(df) * split_ratio)
    df_train = df[:split_point]
    df_future = df[split_point:]
    return df_train, df_future

def train_nilu_model(df_train, target_variable):
    X_train = df_train[['DayOfYear', 'Month', 'sin_day', 'cos_day']]
    y_train = df_train[target_variable]
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    return model