import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3

def vis_temp_per_måned(db_path):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT referenceTime, mean_air_temperature FROM weather_data", conn)
    conn.close()

    # Forbered data
    df['referenceTime'] = pd.to_datetime(df['referenceTime'])
    df['month'] = df['referenceTime'].dt.strftime('%b')
    df['month_num'] = df['referenceTime'].dt.month
    df = df.sort_values('month_num')

    # Lag boxplot
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x='month', y='mean_air_temperature', palette='coolwarm')
    plt.title("Boxplot av daglig middeltemperatur per måned")
    plt.xlabel("Måned")
    plt.ylabel("Temperatur (°C)")
    plt.tight_layout()
    plt.show()

