import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ✅ 1. Last inn NILU-data
nilu = pd.read_csv("data/analyses_results/nilu_aggregated_stats_year_season.csv", skiprows=2)
nilu.columns = [
    'year', 'season',
    'NO2_mean', 'NO2_median', 'NO2_std',
    'PM10_mean', 'PM10_median', 'PM10_std',
    'PM2.5_mean', 'PM2.5_median', 'PM2.5_std'
]
for col in nilu.columns[2:]:
    nilu[col] = pd.to_numeric(nilu[col], errors='coerce')

# ✅ 2. Last inn FROST-data
frost = pd.read_csv("data/analyses_results/frost_aggregated_stats_year_season.csv", skiprows=2)
frost.columns = [
    'year', 'season',
    'temperature_mean', 'temperature_median', 'temperature_std',
    'precipitation_mean', 'precipitation_median', 'precipitation_std',
    'wind_mean', 'wind_median', 'wind_std'
]
for col in frost.columns[2:]:
    frost[col] = pd.to_numeric(frost[col], errors='coerce')

# ✅ 3. Slå sammen datasett
merged = pd.merge(nilu, frost, on=['year', 'season'])

# ✅ 4. Fargepalett (samme som NILU og FROST)
season_colors = {
    "Winter": "steelblue",
    "Spring": "mediumseagreen",
    "Summer": "goldenrod",
    "Fall": "sienna"
}

# ✅ 5. Regresjon per sesong: Temperatur vs NO₂
sns.set(style="whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("FROST + NILU – Temperatur vs NO₂ per sesong", fontsize=16, y=1.03)

seasons = ["Winter", "Spring", "Summer", "Fall"]
axes = axes.flatten()

for i, season in enumerate(seasons):
    data = merged[merged['season'] == season]
    sns.regplot(data=data, x='temperature_mean', y='NO2_mean', ax=axes[i],
                color=season_colors[season], scatter_kws={"s": 50})
    axes[i].set_title(f"{season}")
    axes[i].set_xlabel("Temperatur (°C)")
    axes[i].set_ylabel("NO₂ (µg/m³)")

plt.tight_layout()
plt.show()
