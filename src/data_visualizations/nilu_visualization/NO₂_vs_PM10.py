import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Last inn renset NILU-dagligdata
df = pd.read_json("data/clean/cleaned_data_nilu.json")
df['dateTime'] = pd.to_datetime(df['dateTime'])

# 2. Legg til sesong
def get_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Fall"

df['season'] = df['dateTime'].dt.month.apply(get_season)

# 3. Fjern rader med manglende verdier
df = df.dropna(subset=['NO2', 'PM10'])

# 4. Fargevalg for punkter per sesong 
season_colors = {
    "Winter": "steelblue",
    "Spring": "mediumseagreen",
    "Summer": "goldenrod",
    "Fall": "sienna"
}

# 5. Lag regresjonsplott per sesong med rød linje
sns.set(style="whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("NILU – Daglig sammenheng mellom NO2 og PM10 per sesong", fontsize=16, y=1.03)

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

# 6. Undertittel
plt.figtext(0.5, 0.965,
            "Daglig regresjon per sesong: Sammenheng mellom PM10 og NO2",
            ha="center", fontsize=12, fontweight='bold')

plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.show()
