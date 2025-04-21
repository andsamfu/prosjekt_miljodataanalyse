import sqlite3
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Les inn data
conn = sqlite3.connect(os.path.join('data', 'clean', 'frost.db'))
df = pd.read_sql_query("SELECT * FROM weather_data", conn)
conn.close()

# Rens data
df = df.dropna(subset=['mean_air_temperature', 'total_precipitation'])
df['referenceTime'] = pd.to_datetime(df['referenceTime'])

# Lag nye kolonner
df['DayOfYear'] = df['referenceTime'].dt.dayofyear
df['Year'] = df['referenceTime'].dt.year
df['Month'] = df['referenceTime'].dt.month

# Trigonometrisk sesongmodellering
df['sin_doy'] = np.sin(2 * np.pi * df['DayOfYear'] / 365.25)
df['cos_doy'] = np.cos(2 * np.pi * df['DayOfYear'] / 365.25)

# Lag laggede funksjoner (Temperatur fra 1 dag, 7 dager og 30 dager før)
df['temp_lag_1'] = df['mean_air_temperature'].shift(1)  # 1 dag før
df['temp_lag_7'] = df['mean_air_temperature'].shift(7)  # 7 dager før
df['temp_lag_30'] = df['mean_air_temperature'].shift(30)  # 30 dager før

# Fjern NaN verdier etter at vi har lagt til laggede funksjoner
df = df.dropna(subset=['temp_lag_1', 'temp_lag_7', 'temp_lag_30'])

# Funksjoner (X) og målvariabel (y)
X = df[['DayOfYear', 'Month', 'Year', 'total_precipitation', 'sin_doy', 'cos_doy', 'temp_lag_1', 'temp_lag_7', 'temp_lag_30']]
y = df['mean_air_temperature']

# Splitt datasettet
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Tren modellen
model = LinearRegression()
model.fit(X_train, y_train)

# Prediksjoner
y_pred = model.predict(X_test)

# Evaluer
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse:.2f}")
print(f"R² Score: {r2:.2f}")
