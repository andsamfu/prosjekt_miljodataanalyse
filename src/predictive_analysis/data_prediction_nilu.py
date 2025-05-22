import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_prepare_nilu_data(file_path):
    
    df = pd.read_json(file_path)
    df['dateTime'] = pd.to_datetime(df['dateTime'])
    return df.sort_values('dateTime')

def plot_nilu_components(df, components):

    sns.set(style="whitegrid")
    fig, axes = plt.subplots(len(components), 1, figsize=(14, 12), sharex=True)
    fig.subplots_adjust(hspace=0.4)

    for ax, component in zip(axes, components):
        ax.scatter(df['dateTime'], df[component], alpha=0.6, color='blue', s=10)
        ax.set_title(f"Utvikling i {component}-nivåer (daglig)", fontsize=13)
        ax.set_ylabel(f"{component} (µg/m³)")
        ax.set_xlabel("Dato")

    plt.suptitle("Daglig utvikling i luftforurensningsnivåer (NILU)", fontsize=15, y=0.95)
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.show()

def plot_nilu_with_regression(df, components):
    """
    Visualiserer NILU-komponenter med regresjonslinjer.
    """
    sns.set(style="whitegrid")
    fig, axes = plt.subplots(len(components), 1, figsize=(14, 12), sharex=True)
    fig.subplots_adjust(hspace=0.4)

    for i, component in enumerate(components):
        # Scatter plot
        axes[i].scatter(df['dateTime'], df[component], alpha=0.6, label=component, color='blue', s=10)

        # Regresjonslinje
        X = np.arange(len(df)).reshape(-1, 1)
        y = df[component].values
        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)
        axes[i].plot(df['dateTime'], y_pred, color='red', label='Regresjonslinje')

        # Aksetitler
        axes[i].set_title(f"Utvikling i {component}-nivåer (daglig)", fontsize=13)
        axes[i].set_ylabel(f"{component} (µg/m³)")
        axes[i].set_xlabel("")

    plt.suptitle("Daglig utvikling i luftforurensningsnivåer med regresjonsmodell (NILU)", fontsize=15, y=0.95)
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.show()

def main_nilu_visualization(file_path):
    """
    Hovedfunksjon for å laste inn, analysere og visualisere NILU-data.
    """
    df = load_and_prepare_nilu_data(file_path)
    components = ['NO2', 'PM10', 'PM2.5']
    plot_nilu_with_regression(df, components)


