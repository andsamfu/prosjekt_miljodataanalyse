import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3

# Koble til lokal frost.db
conn = sqlite3.connect("data/clean/frost.db")
df = pd.read_sql("SELECT referenceTime, total_precipitation FROM weather_data", conn)
conn.close()

# Konverter til datetime og legg til sesong + år
df['referenceTime'] = pd.to_datetime(df['referenceTime'])
df['month'] = df['referenceTime'].dt.month
df['year'] = df['referenceTime'].dt.year

def month_to_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Fall"

df['season'] = df['month'].apply(month_to_season)

# Fjern rader med manglende verdier
df_clean = df.dropna(subset=['total_precipitation'])

# Beregn snitt per sesong per år
grouped = df_clean.groupby(['year', 'season'])['total_precipitation'].mean().reset_index()

# Plot
plt.figure(figsize=(10, 6))
sns.boxplot(data=grouped, x='season', y='total_precipitation', order=["Winter", "Spring", "Summer", "Fall"], palette='Blues')
plt.title("Gjennomsnittlig daglig nedbør per sesong")
plt.xlabel("Sesong")
plt.ylabel("Snitt-nedbør (mm per dag)")
plt.tight_layout()
plt.show()
