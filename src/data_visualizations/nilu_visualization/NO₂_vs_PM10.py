import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ✅ Last inn NILU-data
nilu = pd.read_csv("data/analyses_results/nilu_aggregated_stats_year_season.csv", skiprows=2)
nilu.columns = [
    'year', 'season',
    'NO2_mean', 'NO2_median', 'NO2_std',
    'PM10_mean', 'PM10_median', 'PM10_std',
    'PM2.5_mean', 'PM2.5_median', 'PM2.5_std'
]
for col in nilu.columns[2:]:
    nilu[col] = pd.to_numeric(nilu[col], errors='coerce')

# ✅ Regresjon per sesong med farger
sns.set(style="whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("NILU – Sammenheng mellom NO₂ og PM10 per sesong", fontsize=16, y=1.03)

seasons = ["Winter", "Spring", "Summer", "Fall"]
season_colors = {
    "Winter": "steelblue",
    "Spring": "mediumseagreen",
    "Summer": "goldenrod",
    "Fall": "sienna"
}

axes = axes.flatten()

for i, season in enumerate(seasons):
    data = nilu[nilu['season'] == season]
    sns.regplot(data=data, x='PM10_mean', y='NO2_mean', ax=axes[i],
                color=season_colors[season], scatter_kws={"s": 50})
    axes[i].set_title(f"{season}")
    axes[i].set_xlabel("PM10 (µg/m³)")
    axes[i].set_ylabel("NO₂ (µg/m³)")

plt.tight_layout()
plt.show()
