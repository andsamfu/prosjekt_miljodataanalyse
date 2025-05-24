import pandas as pd
import matplotlib.pyplot as plt

def vis_nilu_statistikk_per_år(csv_path):
    # Leser filen og gir kolonnene riktige navn
    df = pd.read_csv(csv_path, skiprows=2)
    df = df.rename(columns={
        df.columns[0]: 'year',
        df.columns[1]: 'NO2_mean', df.columns[2]: 'NO2_median', df.columns[3]: 'NO2_std',
        df.columns[4]: 'PM10_mean', df.columns[5]: 'PM10_median', df.columns[6]: 'PM10_std',
        df.columns[7]: 'PM2.5_mean', df.columns[8]: 'PM2.5_median', df.columns[9]: 'PM2.5_std'
    })

    # Lager 3 plott – gjennomsnitt, median, std
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharex=True)

    # Gjennomsnitt
    axes[0].plot(df['year'], df['NO2_mean'], marker='o', label='NO₂')
    axes[0].plot(df['year'], df['PM10_mean'], marker='o', label='PM10')
    axes[0].plot(df['year'], df['PM2.5_mean'], marker='o', label='PM2.5')
    axes[0].set_title('Årlig Gjennomsnitt')
    axes[0].set_ylabel('µg/m³')
    axes[0].grid(True, linestyle='--')
    axes[0].legend()

    # Median
    axes[1].plot(df['year'], df['NO2_median'], marker='o', label='NO₂')
    axes[1].plot(df['year'], df['PM10_median'], marker='o', label='PM10')
    axes[1].plot(df['year'], df['PM2.5_median'], marker='o', label='PM2.5')
    axes[1].set_title('Årlig Median')
    axes[1].grid(True, linestyle='--')
    axes[1].legend()

    # Standardavvik
    axes[2].plot(df['year'], df['NO2_std'], marker='o', label='NO₂')
    axes[2].plot(df['year'], df['PM10_std'], marker='o', label='PM10')
    axes[2].plot(df['year'], df['PM2.5_std'], marker='o', label='PM2.5')
    axes[2].set_title('Årlig Standardavvik')
    axes[2].grid(True, linestyle='--')
    axes[2].legend()

    for ax in axes:
        ax.set_xlabel('År')

    plt.tight_layout()
    plt.show()
