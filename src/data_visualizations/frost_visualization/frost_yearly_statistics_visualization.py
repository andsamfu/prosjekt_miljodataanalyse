import pandas as pd
import matplotlib.pyplot as plt

def vis_frost_statistikk_per_år(csv_path):
    # Leser inn data, hopper over de to første radene
    df = pd.read_csv(csv_path, skiprows=2)

    # Setter tydelige kolonnenavn
    df.columns = [
        'year',
        'mean_air_temperature_mean',
        'mean_air_temperature_median',
        'mean_air_temperature_std',
        'total_precipitation_mean',
        'total_precipitation_median',
        'total_precipitation_std',
        'mean_wind_speed_mean',
        'mean_wind_speed_median',
        'mean_wind_speed_std'
    ]

    # Lager 3 horisontale delplott: gjennomsnitt, median, standardavvik
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Gjennomsnitt
    axes[0].plot(df['year'], df['mean_air_temperature_mean'], marker='o', label='Temperatur')
    axes[0].plot(df['year'], df['total_precipitation_mean'], marker='o', label='Nedbør')
    axes[0].plot(df['year'], df['mean_wind_speed_mean'], marker='o', label='Vind')
    axes[0].set_title('Gjennomsnitt')
    axes[0].set_xlabel('År')
    axes[0].set_ylabel('Verdi')
    axes[0].grid(True, linestyle='--')
    axes[0].legend()

    # Median
    axes[1].plot(df['year'], df['mean_air_temperature_median'], marker='o', label='Temperatur')
    axes[1].plot(df['year'], df['total_precipitation_median'], marker='o', label='Nedbør')
    axes[1].plot(df['year'], df['mean_wind_speed_median'], marker='o', label='Vind')
    axes[1].set_title('Median')
    axes[1].set_xlabel('År')
    axes[1].grid(True, linestyle='--')
    axes[1].legend()

    # Standardavvik
    axes[2].plot(df['year'], df['mean_air_temperature_std'], marker='o', label='Temperatur')
    axes[2].plot(df['year'], df['total_precipitation_std'], marker='o', label='Nedbør')
    axes[2].plot(df['year'], df['mean_wind_speed_std'], marker='o', label='Vind')
    axes[2].set_title('Standardavvik')
    axes[2].set_xlabel('År')
    axes[2].grid(True, linestyle='--')
    axes[2].legend()

    # Justerer layout og viser figuren
    plt.tight_layout()
    plt.show()
