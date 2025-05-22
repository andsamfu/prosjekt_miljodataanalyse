import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def load_and_prepare_nilu_data(file_path):
    df = pd.read_json(file_path)
    df['dateTime'] = pd.to_datetime(df['dateTime'])
    df = df.sort_values('dateTime')
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

def evaluate_nilu_model(model, df_future, target_variable):
    X_test = df_future[['DayOfYear', 'Month', 'sin_day', 'cos_day']]
    y_test = df_future[target_variable]
    y_pred = model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    return mse, r2, y_test, y_pred