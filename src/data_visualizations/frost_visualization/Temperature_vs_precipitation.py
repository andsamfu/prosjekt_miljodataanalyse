import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3

def vis_regresjon_temp_vs_nedbør_per_sesong(db_path):
    # Leser data fra databasen
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT referenceTime, mean_air_temperature, total_precipitation FROM weather_data", conn)
    conn.close()

    df['referenceTime'] = pd.to_datetime(df['referenceTime'])

    # Legger til sesong
    def get_season(month):
        if month in [12, 1, 2]: return 'Winter'
        if month in [3, 4, 5]: return 'Spring'
        if month in [6, 7, 8]: return 'Summer'
        return 'Fall'

    df['season'] = df['referenceTime'].dt.month.apply(get_season)
    df = df.dropna(subset=['mean_air_temperature', 'total_precipitation'])

    # Farger
    season_colors = {
        "Winter": "steelblue",
        "Spring": "mediumseagreen",
        "Summer": "goldenrod",
        "Fall": "sienna"
    }

    # Forklaringer
    explenation = {
        "Winter": "Stigende linje = mer nedbør ved høyere temperatur",
        "Spring": "Synkende linje = mindre nedbør ved høyere temperatur",
        "Summer": "Synkende linje = mindre nedbør ved høyere temperatur",
        "Fall": "Flat linje = ingen klar sammenheng"
    }

    # Regresjonsplot per sesong
    sns.set(style="whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Daglig sammenheng mellom temperatur og nedbør per sesong (FROST)", fontsize=16, y=1.03)
    axes = axes.flatten()
    seasons = ["Winter", "Spring", "Summer", "Fall"]

    for i, season in enumerate(seasons):
        data = df[df['season'] == season]

        sns.regplot(data=data,
                    x='mean_air_temperature',
                    y='total_precipitation',
                    ax=axes[i],
                    scatter_kws={"s": 10, "alpha": 0.3},
                    line_kws={"color": season_colors[season], "lw": 2},
                    ci=95,
                    color=season_colors[season])

        axes[i].set_title(season, fontsize=14)
        axes[i].set_xlabel("Temperatur (°C)")
        axes[i].set_ylabel("Nedbør (mm)")
        axes[i].grid(True)

        axes[i].text(0.05, 0.9, explenation[season],
                     transform=axes[i].transAxes,
                     fontsize=10, color="black",
                     bbox=dict(facecolor="lightgrey", edgecolor="none", boxstyle="round,pad=0.4"))

    # Undertittel
    plt.figtext(0.5, 0.965,
                "Regresjonsmodeller basert på daglige verdier – temperatur vs nedbør per sesong",
                ha="center", fontsize=12, fontweight='bold')

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.show()
