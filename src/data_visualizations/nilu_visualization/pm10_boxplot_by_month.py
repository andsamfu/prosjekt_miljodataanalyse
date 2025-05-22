import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json

# 1. Last inn renset NILU-data
with open("data/clean/cleaned_data_nilu.json", "r") as f:
    data = json.load(f)

# 2. Bygg DataFrame
df = pd.DataFrame(data)
df['dateTime'] = pd.to_datetime(df['dateTime'])

# Kontroller at PM10 finnes i datasettet
if "PM10" not in df.columns:
    raise ValueError("PM10-kolonnen finnes ikke i data")

# 3. Legg til månedskolonne og månednummer for sortering
df['month'] = df['dateTime'].dt.strftime('%b') # Månedens forkortede navn (Jan, Feb, etc.)
df['month_num'] = df['dateTime'].dt.month     # Månedens nummer (1, 2, etc.)

# 4. Sortér for riktig månedrekkefølge på x-aksen
df = df.sort_values('month_num')

# 5. Lag boxplot for PM10 månedsvis
plt.figure(figsize=(12, 6)) # Justert figurstørrelse for bedre lesbarhet med flere måneder
sns.boxplot(data=df, x='month', y='PM10', palette='Blues', fliersize=0) # Bruker 'Blues' og skjuler outliers
plt.title("Boxplot av månedlige PM10-nivå (μg/m³)")
plt.xlabel("Måned")
plt.ylabel("PM10-nivå (μg/m³)")
plt.tight_layout()
plt.show()