import pandas as pd
import matplotlib.pyplot as plt

def vis_nilu_statistikk_per_år(csv_path):
    """
    Visualiserer årlige statistikker for NILU-data (gjennomsnitt, median og standardavvik)
    ved hjelp av linjediagrammer.

    Args:
        csv_path (str): Filsti til CSV-filen som inneholder NILU-statistikk per år.
    """
    # Leser inn data fra CSV-fil og gir kolonnene beskrivende navn
    df = pd.read_csv(csv_path, skiprows=2)
    df = df.rename(columns={
        df.columns[0]: 'year',
        df.columns[1]: 'NO2_mean', df.columns[2]: 'NO2_median', df.columns[3]: 'NO2_std',
        df.columns[4]: 'PM10_mean', df.columns[5]: 'PM10_median', df.columns[6]: 'PM10_std',
        df.columns[7]: 'PM2.5_mean', df.columns[8]: 'PM2.5_median', df.columns[9]: 'PM2.5_std'
    })

    # Oppretter 3 delplott: gjennomsnitt, median og standardavvik
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharex=True)

    # Gjennomsnitt
    axes[0].plot(df['year'], df['NO2_mean'], marker='o', label='NO₂')
    axes[0].plot(df['year'], df['PM10_mean'], marker='o', label='PM10')
    axes[0].plot(df['year'], df['PM2.5_mean'], marker='o', label='PM2.5')
    axes[0].set_title('Årlig Gjennomsnitt')  # Tittel for delplott
    axes[0].set_ylabel('µg/m³')  # Y-akse etikett
    axes[0].grid(True, linestyle='--')  # Legg til gridlinjer
    axes[0].legend()  # Legg til forklaring

    # Median
    axes[1].plot(df['year'], df['NO2_median'], marker='o', label='NO₂')
    axes[1].plot(df['year'], df['PM10_median'], marker='o', label='PM10')
    axes[1].plot(df['year'], df['PM2.5_median'], marker='o', label='PM2.5')
    axes[1].set_title('Årlig Median')  # Tittel for delplott
    axes[1].grid(True, linestyle='--')  # Legg til gridlinjer
    axes[1].legend()  # Legg til forklaring

    # Standardavvik
    axes[2].plot(df['year'], df['NO2_std'], marker='o', label='NO₂')
    axes[2].plot(df['year'], df['PM10_std'], marker='o', label='PM10')
    axes[2].plot(df['year'], df['PM2.5_std'], marker='o', label='PM2.5')
    axes[2].set_title('Årlig Standardavvik')  # Tittel for delplott
    axes[2].grid(True, linestyle='--')  # Legg til gridlinjer
    axes[2].legend()  # Legg til forklaring

    # Legg til etikett for x-aksen for alle delplott
    for ax in axes:
        ax.set_xlabel('År')

    # Juster layout for å unngå overlapp mellom elementer
    plt.tight_layout()

    # Vis figuren
    plt.show()
