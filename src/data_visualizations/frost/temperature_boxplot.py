import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3

def show_temp(db_path):
    """
    Visualiserer daglig middeltemperatur per måned ved hjelp av et boxplot.

    Args:
        db_path (str): Filsti til SQLite-databasen som inneholder værdata.
    """
    # Koble til databasen og hent data
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT referenceTime, mean_air_temperature FROM weather_data", conn)
    conn.close()  # Lukk tilkoblingen til databasen

    # Forbered data for visualisering
    df['referenceTime'] = pd.to_datetime(df['referenceTime'])  # Konverter til datetime-format
    df['month'] = df['referenceTime'].dt.strftime('%b')  # Ekstraher månednavn
    df['month_num'] = df['referenceTime'].dt.month  # Ekstraher måned som tall
    df = df.sort_values('month_num')  # Sorter etter måned for korrekt rekkefølge

    # Lag boxplot for å vise temperaturfordeling per måned
    plt.figure(figsize=(12, 6)) 
    sns.boxplot(
        data=df, 
        x='month', 
        y='mean_air_temperature', 
        palette='coolwarm'  # Fargepalett for bedre visualisering
    )
    plt.title("Boxplot av daglig middeltemperatur per måned", fontsize=14)  # Tittel for plottet
    plt.xlabel("Måned", fontsize=12)  # Etikett for x-aksen
    plt.ylabel("Temperatur (°C)", fontsize=12)  # Etikett for y-aksen
    plt.tight_layout()  # Juster layout for å unngå overlapp 
    plt.show()  # Vis plottet

