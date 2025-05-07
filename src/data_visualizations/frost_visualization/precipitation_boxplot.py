import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3

def vis_nedbør_per_sesong(db_path):
    # Leser inn dato og nedbør fra databasen
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT referenceTime, total_precipitation FROM weather_data", conn)
    conn.close()

    # Gjør datoen om til datetime og legg til måned og år
    df['referenceTime'] = pd.to_datetime(df['referenceTime'])
    df['month'] = df['referenceTime'].dt.month
    df['year'] = df['referenceTime'].dt.year

    # Finner sesong basert på måned
    def month_to_season(month):
        if month in [12, 1, 2]: return "Winter"
        if month in [3, 4, 5]: return "Spring"
        if month in [6, 7, 8]: return "Summer"
        return "Fall"

    df['season'] = df['month'].apply(month_to_season)

    # Fjerner rader uten verdier
    df = df.dropna(subset=['total_precipitation'])

    # Beregner snitt-nedbør per sesong per år
    grouped = df.groupby(['year', 'season'])['total_precipitation'].mean().reset_index()

    # Lager boxplot
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=grouped, x='season', y='total_precipitation', hue='season',
            order=["Winter", "Spring", "Summer", "Fall"],
            palette='Blues', legend=False)


    plt.title("Gjennomsnittlig daglig nedbør per sesong")
    plt.xlabel("Sesong")
    plt.ylabel("Snitt-nedbør (mm per dag)")
    plt.tight_layout()
    plt.show()
