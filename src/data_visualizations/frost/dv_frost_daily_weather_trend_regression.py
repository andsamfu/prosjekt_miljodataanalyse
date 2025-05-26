import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3

def plot_weather_components(db_path="data/clean/cleaned_data_frost.db"):
    """
    Leser inn værdata fra cleaned_data_frost.db og visualiserer utviklingen i temperatur, nedbør og vindhastighet.
    
    Parametere:
    -----------
    db_path : str
        Filsti til SQLite-databasen som inneholder værdataene.
    """
    # Last inn data
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM weather_data", conn)
    conn.close()

    df['referenceTime'] = pd.to_datetime(df['referenceTime'])

    # Velg komponenter og tilhørende titler
    components = ['mean_air_temperature', 'total_precipitation', 'mean_wind_speed']
    titles = {
        'mean_air_temperature': "Utvikling i temperatur (daglig)",
        'total_precipitation': "Utvikling i nedbør (daglig)",
        'mean_wind_speed': "Utvikling i vindhastighet (daglig)"
    }

    # Sett opp figuren
    sns.set(style="whitegrid")
    fig, axes = plt.subplots(len(components), 1, figsize=(14, 12), sharex=True)
    fig.subplots_adjust(hspace=0.4)

    # Plott hver komponent med regresjonslinje
    for i, comp in enumerate(components):
        data = df[['referenceTime', comp]].dropna().copy()
        data['x_temp'] = (data['referenceTime'] - data['referenceTime'].min()).dt.days

        sns.regplot(
            data=data, x='x_temp', y=comp, ax=axes[i],
            scatter_kws={"s": 12, "alpha": 0.6},
            line_kws={"color": "crimson"},
            lowess=True
        )

        tick_step = max(1, int(len(data) / 8))
        tick_pos = data['x_temp'][::tick_step]
        tick_labels = data['referenceTime'][::tick_step].dt.strftime('%b %Y')
        axes[i].set_xticks(tick_pos)
        axes[i].set_xticklabels(tick_labels, rotation=45)

        axes[i].set_title(titles[comp], fontsize=13)
        axes[i].set_ylabel(comp.replace('_', ' ').capitalize())
        axes[i].set_xlabel("")

    plt.suptitle("Daglig utvikling i værdata med regresjonsmodell (FROST)", fontsize=15, y=0.95)
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.show()
