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

# Bruke hele datasettet
df_clean = df.copy()

# Lage boxplot
plt.figure(figsize=(12, 6))
sns.boxplot(data=df_clean, x='month', y='NO2', palette='YlOrBr')
plt.title("Boxplot av måndelige NO₂-nivå (μg/m³)")
plt.xlabel("Month")
plt.ylabel("NO₂ (μg/m³)")
plt.tight_layout()
plt.show()
