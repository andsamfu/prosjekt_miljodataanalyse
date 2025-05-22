import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3

def plot_temperature_vs_pm25(nilu_json_path, frost_db_path):
    # Last inn daglig NILU-data
    nilu = pd.read_json(nilu_json_path)
    nilu['dateTime'] = pd.to_datetime(nilu['dateTime'])

    # Last inn daglig FROST-data
    conn = sqlite3.connect(frost_db_path)
    frost = pd.read_sql("SELECT referenceTime, mean_air_temperature FROM weather_data", conn)
    conn.close()
    frost['referenceTime'] = pd.to_datetime(frost['referenceTime'])

    # Merge data på dato
    nilu['date'] = nilu['dateTime'].dt.date
    frost['date'] = frost['referenceTime'].dt.date
    merged = pd.merge(nilu, frost, on='date')

    # Legg til sesong
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'

    merged['season'] = pd.to_datetime(merged['date']).dt.month.apply(get_season)

    # Fjern manglende verdier
    merged = merged.dropna(subset=['mean_air_temperature', 'PM2.5'])

    # Sesongfarger og forklaringer
    season_colors = {
        "Winter": "steelblue",
        "Spring": "mediumseagreen",
        "Summer": "goldenrod",
        "Fall": "sienna"
    }

    explanations = {
        "Winter": "Negativ trend: Høyere PM2.5 ved lavere temperaturer",
        "Spring": "Svak positiv trend: Liten økning i PM2.5 ved økt temperatur",
        "Summer": "Lite mønster: Svak og usikker positiv sammenheng",
        "Fall":   "Negativ trend: PM2.5 synker svakt med høyere temperatur"
    }

    # Plotting
    sns.set(style="whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Daglig regresjon per sesong: Temperatur (FROST) vs PM2.5 (NILU)", fontsize=16, y=1.03)

    seasons = ["Winter", "Spring", "Summer", "Fall"]
    axes = axes.flatten()

    for i, season in enumerate(seasons):
        data = merged[merged['season'] == season]
        point_color = season_colors[season]

        sns.regplot(
            data=data,
            x='mean_air_temperature',
            y='PM2.5',
            ax=axes[i],
            scatter_kws={"s": 10, "alpha": 0.3, "color": point_color},
            line_kws={"color": "crimson", "lw": 2},
            color="crimson",
            ci=95
        )

        axes[i].set_title(season)
        axes[i].set_xlabel("Temperatur (°C)")
        axes[i].set_ylabel("PM₂.₅ (µg/m³)")
        axes[i].grid(True)

        axes[i].text(0.05, 0.9, explanations[season],
                     transform=axes[i].transAxes,
                     fontsize=10, color="black",
                     bbox=dict(facecolor="lightgrey", edgecolor="none", boxstyle="round,pad=0.4"))

    plt.figtext(0.5, 0.965,
                "Regresjonsanalyse av daglige verdier: Sammenheng mellom temperatur (FROST) og PM2.5 (NILU) per sesong",
                ha="center", fontsize=12, fontweight='bold')

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.show()


