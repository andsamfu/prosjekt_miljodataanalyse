import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3

# Koble til lokal frost.db
conn = sqlite3.connect("data/clean/frost.db")
# Henter kun nødvendige kolonner
df = pd.read_sql("SELECT referenceTime, total_precipitation FROM weather_data", conn)
conn.close()

# Konverter til datetime
df['referenceTime'] = pd.to_datetime(df['referenceTime'])


df['year'] = df['referenceTime'].dt.year 
df['month'] = df['referenceTime'].dt.strftime('%b')
df['month_num'] = df['referenceTime'].dt.month

# Grupper dataen per år og måned, og beregn gjennomsnittlig nedbør
grouped = df.groupby(['year', 'month_num', 'month'])['total_precipitation'].mean().reset_index()

# Sorter for riktig månedrekkefølge på x-aksen
# Vi må sørge for at månedene vises i kronologisk rekkefølge (Jan, Feb, Mar, etc.)
grouped = grouped.sort_values('month_num')

# Definer rekkefølgen på månedene for plottet
month_order = grouped['month'].unique().tolist()

# Plot
plt.figure(figsize=(12, 6)) # Justert figurstørrelse for 12 måneder
sns.boxplot(data=grouped, x='month', y='total_precipitation', order=month_order, palette='Blues', fliersize=0)
plt.title("Gjennomsnittlig daglig nedbør per måned")
plt.xlabel("Måned")
plt.ylabel("Snitt-nedbør (mm per dag)")
plt.tight_layout()
plt.show()