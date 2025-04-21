import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Last inn FROST-data
frost = pd.read_csv("data/analyses_results/frost_aggregated_stats_year_season.csv", skiprows=2)
frost.columns = [
    'year', 'season',
    'temperature_mean', 'temperature_median', 'temperature_std',
    'precipitation_mean', 'precipitation_median', 'precipitation_std',
    'wind_mean', 'wind_median', 'wind_std'
]

# Konverter verdier til numerisk
for col in frost.columns[2:]:
    frost[col] = pd.to_numeric(frost[col], errors='coerce')

# Farger per sesong
season_colors = {
    "Winter": "steelblue",
    "Spring": "mediumseagreen",
    "Summer": "goldenrod",
    "Fall": "sienna"
}

#  Regresjon per sesong
sns.set(style="whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Forklarende hovedtittel
fig.suptitle("FROST – Temperatur vs Nedbør per sesong", fontsize=16, y=1.05)

seasons = ["Winter", "Spring", "Summer", "Fall"]
axes = axes.flatten()

for i, season in enumerate(seasons):
    data = frost[frost['season'] == season]
    sns.regplot(data=data,
                x='temperature_mean',
                y='precipitation_mean',
                ax=axes[i],
                color=season_colors[season],
                scatter_kws={"s": 50})
    
    axes[i].set_title(f"{season}", fontsize=14)
    axes[i].set_xlabel("Temperatur (°C)")
    axes[i].set_ylabel("Nedbør (mm)")


plt.figtext(0.5, 0.97,
            "Regresjonsmodeller per sesong: Temperatur vs nedbør (gjennomsnitt per år 2010 - 2019)",
            ha="center", fontsize=12, fontweight='bold')

plt.tight_layout(rect=[0, 0, 1, 0.95]) 
plt.show()
