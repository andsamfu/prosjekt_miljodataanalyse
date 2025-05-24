import pandas as pd
import matplotlib.pyplot as plt

def vis_frost_statistikk_per_år(csv_path):
    """
    Visualiserer årlige statistikker for værdata (gjennomsnitt, median og standardavvik)
    ved hjelp av linjediagrammer.

    Args:
        csv_path (str): Filsti til CSV-filen som inneholder værstatistikk per år.
    """
    # Leser inn data fra CSV-fil, hopper over de to første radene (metadata)
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
    axes[0].set_title('Gjennomsnitt')  # Tittel for delplott
    axes[0].set_xlabel('År')  # X-akse etikett
    axes[0].set_ylabel('Verdi')  # Y-akse etikett
    axes[0].grid(True, linestyle='--')  # Gridlinjer for bedre lesbarhet
    axes[0].legend()  # Legg til forklaring for linjene

    # Median
    axes[1].plot(df['year'], df['mean_air_temperature_median'], marker='o', label='Temperatur')
    axes[1].plot(df['year'], df['total_precipitation_median'], marker='o', label='Nedbør')
    axes[1].plot(df['year'], df['mean_wind_speed_median'], marker='o', label='Vind')
    axes[1].set_title('Median')  # Tittel for delplott
    axes[1].set_xlabel('År')  # X-akse etikett
    axes[1].grid(True, linestyle='--')  # Gridlinjer for bedre lesbarhet
    axes[1].legend()  # Legg til forklaring for linjene

    # Standardavvik
    axes[2].plot(df['year'], df['mean_air_temperature_std'], marker='o', label='Temperatur')
    axes[2].plot(df['year'], df['total_precipitation_std'], marker='o', label='Nedbør')
    axes[2].plot(df['year'], df['mean_wind_speed_std'], marker='o', label='Vind')
    axes[2].set_title('Standardavvik')  # Tittel for delplott
    axes[2].set_xlabel('År')  # X-akse etikett
    axes[2].grid(True, linestyle='--')  # Gridlinjer for bedre lesbarhet
    axes[2].legend()  # Legg til forklaring for linjene

    # Justerer layout og viser figuren
    plt.tight_layout()

    # Viser figuren
    plt.show()
