import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json

# Laste inn renset NILU-data fra JSON
with open("data/clean/cleaned_data_nilu.json", "r") as f:
    data = json.load(f)

# Bygge DataFrame
df = pd.DataFrame(data)
df['dateTime'] = pd.to_datetime(df['dateTime'])

# Kontroller at NO2 finnes i datasettet
if "NO2" not in df.columns:
    raise ValueError("NO2-kolonnen finnes ikke i data")

# Legge til månedskolonne
df['month'] = df['dateTime'].dt.strftime('%b')
df['month_num'] = df['dateTime'].dt.month

# Sortere for riktig månedrekkefølge
df = df.sort_values('month_num')

# Lage boxplot
plt.figure(figsize=(12, 6))
# Bruk fliersize=0 for å ikke vise outliers i plottet
# Endret palette til 'Blues' for kun blå farger
sns.boxplot(data=df, x='month', y='NO2', palette='Blues', fliersize=0)
plt.title("Boxplot av månedlige NO₂-nivå (μg/m³)")
plt.xlabel("Måned")
plt.ylabel("NO₂ (μg/m³)")
plt.tight_layout()
plt.show()