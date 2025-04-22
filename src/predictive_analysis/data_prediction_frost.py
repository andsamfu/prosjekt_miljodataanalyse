import sqlite3
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import os

# Load data from the SQLite database
db_path = os.path.join('data', 'clean', 'frost.db')
conn = sqlite3.connect(db_path)
df = pd.read_sql_query("SELECT * FROM weather_data", conn)
conn.close()

# Convert date and create features
df['referenceTime'] = pd.to_datetime(df['referenceTime'])
df = df.sort_values('referenceTime')

# Create all necessary features
df['DayOfYear'] = df['referenceTime'].dt.dayofyear
df['Month'] = df['referenceTime'].dt.month
df['sin_day'] = np.sin(2 * np.pi * df['DayOfYear']/365)
df['cos_day'] = np.cos(2 * np.pi * df['DayOfYear']/365)

# Calculate the split point at 3/4 of the data
split_point = int(len(df) * 0.75)
df_train = df[:split_point]
df_future = df[split_point:]

# Calculate how many years of future data we have
future_years = (df_future['referenceTime'].max() - df_future['referenceTime'].min()).days / 365.25

# Create features for training data
X_train = df_train[['DayOfYear', 'Month', 'sin_day', 'cos_day']]
y_train = df_train['mean_air_temperature']

# Create features for future prediction (including beyond available data)
last_date = df_future['referenceTime'].iloc[-1]
future_dates = pd.date_range(
    start=df_future['referenceTime'].iloc[0],
    end=last_date + pd.DateOffset(years=int(future_years)),
    freq='D'
)

# Create future features DataFrame
future_df = pd.DataFrame({'referenceTime': future_dates})
future_df['DayOfYear'] = future_df['referenceTime'].dt.dayofyear
future_df['Month'] = future_df['referenceTime'].dt.month
future_df['sin_day'] = np.sin(2 * np.pi * future_df['DayOfYear']/365)
future_df['cos_day'] = np.cos(2 * np.pi * future_df['DayOfYear']/365)

# Train the model and make predictions
model = LinearRegression()
model.fit(X_train, y_train)
X_future_extended = future_df[['DayOfYear', 'Month', 'sin_day', 'cos_day']]
y_pred_extended = model.predict(X_future_extended)

# Evaluate the model on the known future period
X_future_known = df_future[['DayOfYear', 'Month', 'sin_day', 'cos_day']]
y_pred_known = model.predict(X_future_known)
mse = mean_squared_error(df_future['mean_air_temperature'], y_pred_known)
r2 = r2_score(df_future['mean_air_temperature'], y_pred_known)

# Create the time series plot
plt.figure(figsize=(15, 6))

# Function to split data into continuous segments
def split_into_segments(dates, values, max_gap_days=31):
    if len(dates) == 0:
        return [], []
        
    segments_x = []
    segments_y = []
    current_x = [dates.iloc[0]]
    current_y = [values.iloc[0]]
    
    for i in range(1, len(dates)):
        gap = (dates.iloc[i] - dates.iloc[i-1]).days
        if gap > max_gap_days:
            segments_x.append(current_x)
            segments_y.append(current_y)
            current_x = []
            current_y = []
        current_x.append(dates.iloc[i])
        current_y.append(values.iloc[i])
    
    if current_x:  # Add the last segment if it exists
        segments_x.append(current_x)
        segments_y.append(current_y)
    return segments_x, segments_y

# Plot training data (blue for real, red for generated)
mask_train_real = df_train['generated_mean_air_temperature'] == 0
mask_train_generated = df_train['generated_mean_air_temperature'] == 1

# Plot real training data segments
dates_real = df_train.loc[mask_train_real, 'referenceTime']
temps_real = df_train.loc[mask_train_real, 'mean_air_temperature']
segments_x, segments_y = split_into_segments(dates_real, temps_real)
for seg_x, seg_y in zip(segments_x, segments_y):
    plt.plot(seg_x, seg_y, color='blue', alpha=0.7)
if len(dates_real) > 0:  # Only add to legend if there's data
    plt.plot([], [], color='blue', label='Training Data', alpha=0.7)

# Plot generated training data segments
dates_gen = df_train.loc[mask_train_generated, 'referenceTime']
temps_gen = df_train.loc[mask_train_generated, 'mean_air_temperature']
segments_x, segments_y = split_into_segments(dates_gen, temps_gen)
for seg_x, seg_y in zip(segments_x, segments_y):
    plt.plot(seg_x, seg_y, color='red', alpha=0.7)
if len(dates_gen) > 0:  # Only add to legend if there's data
    plt.plot([], [], color='red', label='Generated Data', alpha=0.7)

# Plot future data segments (green for real, red for generated)
mask_future_real = df_future['generated_mean_air_temperature'] == 0
mask_future_generated = df_future['generated_mean_air_temperature'] == 1

# Plot real future data segments
dates_future = df_future.loc[mask_future_real, 'referenceTime']
temps_future = df_future.loc[mask_future_real, 'mean_air_temperature']
segments_x, segments_y = split_into_segments(dates_future, temps_future)
for seg_x, seg_y in zip(segments_x, segments_y):
    plt.plot(seg_x, seg_y, color='green', alpha=0.7)
if len(dates_future) > 0:  # Only add to legend if there's data
    plt.plot([], [], color='green', label='Actual Future', alpha=0.7)

# Plot generated future data segments
dates_future_gen = df_future.loc[mask_future_generated, 'referenceTime']
temps_future_gen = df_future.loc[mask_future_generated, 'mean_air_temperature']
segments_x, segments_y = split_into_segments(dates_future_gen, temps_future_gen)
for seg_x, seg_y in zip(segments_x, segments_y):
    plt.plot(seg_x, seg_y, color='red', alpha=0.7)

# Plot predictions
plt.plot(future_df['referenceTime'], y_pred_extended,
         color='orange', label='Predicted Future',
         linestyle='--', linewidth=2, alpha=1)

plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.title('Temperature Prediction Model')
plt.legend(loc='upper right')
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print("Model Performance:")
print(f"Mean Squared Error: {mse:.2f}")
print(f"R² Score: {r2:.2f}")

# Print model coefficients
feature_names = ['DayOfYear', 'Month', 'sin_day', 'cos_day']
print("\nModel Coefficients:")
for feature, coef in zip(feature_names, model.coef_):
    print(f"{feature}: {coef:.4f}")
print(f"Intercept: {model.intercept_:.4f}")