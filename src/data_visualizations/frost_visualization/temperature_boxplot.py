import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3

def vis_middeltemp_per_måned(db_path):
    # Kobler til databasen og henter temperaturdata
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT referenceTime, mean_air_temperature FROM weather_data", conn)
    conn.close()

    # Gjør om tid og sorter etter måned
    df['referenceTime'] = pd.to_datetime(df['referenceTime'])
    df['month'] = df['referenceTime'].dt.strftime('%b')       # Jan, Feb, ...
    df['month_num'] = df['referenceTime'].dt.month            # 1–12
    df = df.sort_values('month_num')

    # Lager boxplot for middeltemperatur per måned
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x='month', y='mean_air_temperature', palette='coolwarm')
    plt.title("Boxplot av daglig middeltemperatur per måned")
    plt.xlabel("Måned")
    plt.ylabel("Temperatur (°C)")
    plt.tight_layout()
    plt.show()
