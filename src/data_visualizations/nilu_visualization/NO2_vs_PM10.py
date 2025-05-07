import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json

def vis_pm10_vs_no2_per_sesong(json_path):
    # Leser inn NILU-data
    with open(json_path, "r") as f:
        data = json.load(f)

    nilu = pd.DataFrame(data)
    nilu['dateTime'] = pd.to_datetime(nilu['dateTime'])
    nilu['date'] = nilu['dateTime'].dt.date

    # Legger til sesong
    def get_season(month):
        if month in [12, 1, 2]: return 'Winter'
        if month in [3, 4, 5]: return 'Spring'
        if month in [6, 7, 8]: return 'Summer'
        return 'Fall'

    nilu['season'] = nilu['dateTime'].dt.month.apply(get_season)

    # Filtrer nødvendige kolonner og dropp manglende verdier
    df = nilu[['date', 'PM10', 'NO2', 'season']].dropna()

    # Farger og forklaringstekster
    season_colors = {
        "Winter": "steelblue",
        "Spring": "mediumseagreen",
        "Summer": "goldenrod",
        "Fall": "sienna"
    }

    explanations = {
        "Winter": "Tydelig positiv trend: PM10 og NO2 øker sammen",
        "Spring": "Positiv sammenheng: Høyere PM10 → mer NO2",
        "Summer": "Klar økning i NO2 med økt PM10",
        "Fall":   "Sterk korrelasjon: PM10 og NO2 beveger seg likt"
    }

    # Plot
    sns.set(style="whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Daglig regresjon per sesong: Sammenheng mellom PM10 og NO2", fontsize=16, y=1.03)

    seasons = ["Winter", "Spring", "Summer", "Fall"]
    axes = axes.flatten()

    for i, season in enumerate(seasons):
        data = df[df['season'] == season]

        sns.regplot(
            data=data,
            x='PM10',
            y='NO2',
            ax=axes[i],
            scatter_kws={"s": 12, "alpha": 0.3, "color": season_colors[season]},
            line_kws={"color": "crimson", "lw": 2},
            ci=95,
            color="crimson"
        )

        axes[i].set_title(season, fontsize=14)
        axes[i].set_xlabel("PM10 (µg/m³)")
        axes[i].set_ylabel("NO2 (µg/m³)")
        axes[i].grid(True)

        axes[i].text(0.05, 0.9, explanations[season],
                     transform=axes[i].transAxes,
                     fontsize=10, color="black",
                     bbox=dict(facecolor="lightgrey", edgecolor="none", boxstyle="round,pad=0.4"))

    # Undertittel
    plt.figtext(0.5, 0.965,
                "Daglig regresjon per sesong: Sammenheng mellom PM10 og NO2",
                ha="center", fontsize=12, fontweight='bold')

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.show()
