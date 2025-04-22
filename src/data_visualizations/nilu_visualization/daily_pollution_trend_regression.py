import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Last inn og klargjør NILU-data
df = pd.read_json("data/clean/cleaned_data_nilu.json")
df['dateTime'] = pd.to_datetime(df['dateTime'])

# 2. Velg luftkomponenter
components = ['NO2', 'PM10', 'PM2.5']
titles = {
    'NO2': "Utvikling i NO2-nivåer (daglig)",
    'PM10': "Utvikling i PM10-nivåer (daglig)",
    'PM2.5': "Utvikling i PM2.5-nivåer (daglig)"
}

# 3. Sett opp figuren
sns.set(style="whitegrid")
fig, axes = plt.subplots(3, 1, figsize=(14, 12), sharex=True)
fig.subplots_adjust(hspace=0.4)

# 4. Plott hver komponent
for i, comp in enumerate(components):
    data = df[['dateTime', comp]].dropna().copy()

    # Bruk numerisk X kun til å kjøre regresjon
    x_numeric = (data['dateTime'] - data['dateTime'].min()).dt.days
    data['x_temp'] = x_numeric

    # Plot med regresjonslinje
    sns.regplot(data=data, x='x_temp', y=comp, ax=axes[i],
                scatter_kws={"s": 12, "alpha": 0.6},
                line_kws={"color": "crimson"})

    # Datoetiketter i stedet for x_temp
    tick_step = max(1, int(len(data) / 8))
    tick_pos = data['x_temp'][::tick_step]
    tick_labels = data['dateTime'][::tick_step].dt.strftime('%b %Y')
    axes[i].set_xticks(tick_pos)
    axes[i].set_xticklabels(tick_labels, rotation=45)

    # Aksetitler
    axes[i].set_title(titles[comp], fontsize=13)
    axes[i].set_ylabel(f"{comp} (µg/m³)")
    axes[i].set_xlabel("") 

# 5. Hovedtittel
plt.suptitle("Daglig utvikling i luftforurensningsnivåer med regresjonsmodell (NILU)", fontsize=15, y=0.95)
plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.show()
