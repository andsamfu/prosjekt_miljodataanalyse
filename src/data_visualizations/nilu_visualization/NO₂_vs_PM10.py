import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Last inn NILU-data og klargjør
nilu = pd.read_csv("data/analyses_results/nilu_aggregated_stats_year_season.csv", skiprows=2)
nilu.columns = [
    'year', 'season',
    'NO2_mean', 'NO2_median', 'NO2_std',
    'PM10_mean', 'PM10_median', 'PM10_std',
    'PM2.5_mean', 'PM2.5_median', 'PM2.5_std'
]

for col in nilu.columns[2:]:
    nilu[col] = pd.to_numeric(nilu[col], errors='coerce')

nilu = nilu.dropna(subset=['NO2_mean', 'PM10_mean'])

# 2. Fargevalg per sesong
season_colors = {
    "Winter": "steelblue",
    "Spring": "mediumseagreen",
    "Summer": "goldenrod",
    "Fall": "sienna"
}

# 3. Regresjonsplott per sesong
sns.set(style="whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("NILU – Sammenheng mellom NO₂ og PM₁₀ per sesong", fontsize=16, y=1.03)

seasons = ["Winter", "Spring", "Summer", "Fall"]
axes = axes.flatten()

for i, season in enumerate(seasons):
    data = nilu[nilu['season'] == season]

    # Regresjonsplott med farget linje OG skyggesone
    sns.regplot(
        data=data,
        x='PM10_mean',
        y='NO2_mean',
        ax=axes[i],
        scatter_kws={"s": 50, "alpha": 0.7, "color": season_colors[season]},
        line_kws={"color": season_colors[season], "lw": 2},
        ci=95
    )

    axes[i].set_title(f"{season}", fontsize=14)
    axes[i].set_xlabel("PM₁₀ (µg/m³)", fontsize=11)
    axes[i].set_ylabel("NO₂ (µg/m³)", fontsize=11)
    axes[i].grid(True)

# 4. Forklarende undertittel
plt.figtext(0.5, 0.965,
            "Regresjonsmodeller per sesong: Sammenheng mellom PM₁₀ og NO₂ (gjennomsnitt per år 2010–2024)\n smalere skygge = sterkere sammenheng",
            ha="center", fontsize=12, fontweight='bold')

plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.show()
