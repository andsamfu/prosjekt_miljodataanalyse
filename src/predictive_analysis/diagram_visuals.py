import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Sjekk og opprett mappen 'src/predictive_analyses/diagrams' hvis den ikke finnes
output_dir = os.path.join('src', 'predictive_analysis','diagrams')
os.makedirs(output_dir, exist_ok=True)

# Les inn data fra SQLite
conn = sqlite3.connect(os.path.join('data', 'clean', 'frost.db'))
df = pd.read_sql_query("SELECT * FROM weather_data", conn)
conn.close()

# Konverter dato
df['referenceTime'] = pd.to_datetime(df['referenceTime'])

# Fjern NaN verdier for de variablene vi trenger for visualiseringene
df_clean = df.dropna(subset=['mean_air_temperature', 'total_precipitation'])

# Vi legger til en ekstra kolonne for måned/år
df_clean['Year'] = df_clean['referenceTime'].dt.year
df_clean['Month'] = df_clean['referenceTime'].dt.month

# Sett Seaborn tema for bedre design
sns.set_theme(style="whitegrid")

# Visualisering 1: Søylediagram - Gjennomsnittstemperatur per måned
plt.figure(figsize=(12, 7))
sns.barplot(x='Month', y='mean_air_temperature', data=df_clean, estimator=np.mean, palette='coolwarm')
plt.title('Gjennomsnittstemperatur per Måned', fontsize=18)
plt.xlabel('Måned', fontsize=14)
plt.ylabel('Gjennomsnittstemperatur (°C)', fontsize=14)
plt.xticks(np.arange(12), ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Des'], fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
# Lagre diagrammet som en PNG-fil
plt.savefig(os.path.join(output_dir, 'average_temperature_per_month.png'))
plt.close()

# Visualisering 2: Linjediagram - Temperatur over tid
plt.figure(figsize=(14, 8))
sns.lineplot(x='referenceTime', y='mean_air_temperature', data=df_clean, color='royalblue', linewidth=2.5)
plt.title('Temperatur over Tid', fontsize=18)
plt.xlabel('Tid', fontsize=14)
plt.ylabel('Temperatur (°C)', fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)
plt.grid(True)
plt.tight_layout()
# Lagre diagrammet som en PNG-fil
plt.savefig(os.path.join(output_dir, 'temperature_over_time.png'))
plt.close()

# Visualisering 3: Scatterplot - Forhold mellom temperatur og nedbør
plt.figure(figsize=(12, 7))
sns.scatterplot(x='mean_air_temperature', y='total_precipitation', data=df_clean, color='darkorange', alpha=0.7, s=90)
plt.title('Sammenheng mellom Temperatur og Nedbør', fontsize=18)
plt.xlabel('Temperatur (°C)', fontsize=14)
plt.ylabel('Nedbør (mm)', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
# Lagre diagrammet som en PNG-fil
plt.savefig(os.path.join(output_dir, 'temperature_vs_precipitation.png'))
plt.close()
