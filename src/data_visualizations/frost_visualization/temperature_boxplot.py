import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3

# Kobler til databasen
conn = sqlite3.connect("data/clean/frost.db")
df = pd.read_sql("SELECT referenceTime, mean_air_temperature FROM weather_data", conn)
conn.close()

# Forbereder data
df['referenceTime'] = pd.to_datetime(df['referenceTime'])
df['month'] = df['referenceTime'].dt.strftime('%b')
df['month_num'] = df['referenceTime'].dt.month
df = df.sort_values('month_num')

# Lager boxplot
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='month', y='mean_air_temperature', palette='coolwarm')
plt.title("Boxplot av daglig middeltemperatur per måned")
plt.xlabel("Måned")
plt.ylabel("Temperatur (°C)")
plt.tight_layout()
plt.show()

