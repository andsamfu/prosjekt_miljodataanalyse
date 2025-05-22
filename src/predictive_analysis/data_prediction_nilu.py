import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_prepare_nilu_data(file_path):

    df = pd.read_json(file_path)
    df['dateTime'] = pd.to_datetime(df['dateTime'])
    df = df.dropna(subset=['NO2', 'PM10', 'PM2.5'])
    return df.sort_values('dateTime')

def extend_dates(df, years=5):

    last_date = df['dateTime'].iloc[-1]
    future_dates = pd.date_range(start=last_date, periods=years * 365, freq='D')
    return future_dates

def plot_nilu_with_regression_and_prediction(df, components, years=5):

    sns.set(style="whitegrid")
    fig, axes = plt.subplots(len(components), 1, figsize=(14, 12), sharex=True)
    fig.subplots_adjust(hspace=0.4)

    for i, component in enumerate(components):
        # Scatter plot
        axes[i].scatter(df['dateTime'], df[component], alpha=0.6, label='Historiske data', color='blue', s=10)

        # Regresjonslinje
        X = np.arange(len(df)).reshape(-1, 1)
        y = df[component].values
        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)
        axes[i].plot(df['dateTime'], y_pred, color='red', label='Regresjonslinje')

        # Prediksjon for fremtidige datoer
        future_dates = extend_dates(df, years)
        future_X = np.arange(len(df), len(df) + len(future_dates)).reshape(-1, 1)
        future_y_pred = model.predict(future_X)
        axes[i].plot(future_dates, future_y_pred, color='green', linestyle='--', label='Prediksjon')

        # Aksetitler
        axes[i].set_title(f"Utvikling og prediksjon for {component} (daglig)", fontsize=13)
        axes[i].set_ylabel(f"{component} (µg/m³)")
        axes[i].set_xlabel("Dato")

    plt.suptitle("Daglig utvikling og prediksjon i luftforurensningsnivåer (NILU)", fontsize=15, y=0.95)
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.legend(loc='upper right')
    plt.show()

def main_nilu_prediction(file_path):

    df = load_and_prepare_nilu_data(file_path)
    components = ['NO2', 'PM10', 'PM2.5']
    plot_nilu_with_regression_and_prediction(df, components, years=5)

# Kjør hovedfunksjonen
file_path = 'data/clean/cleaned_data_nilu.json'
main_nilu_prediction(file_path)