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


