import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import calendar
import numpy as np

def show_percipitation(db_path="data/clean/frost.db"):
    """
    Visualiserer gjennomsnittlig daglig nedbør per måned med standardavvik som feilmarginer.

    Args:
        db_path (str): Filsti til SQLite-databasen som inneholder værdata.
    """
    # Koble til databasen og hent data
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("""
        SELECT referenceTime, total_precipitation
        FROM weather_data
        WHERE total_precipitation IS NOT NULL
    """, conn)
    conn.close()  # Lukk tilkoblingen til databasen

    # Konverter 'referenceTime' til datetime-format og grupper data per dag
    df['referenceTime'] = pd.to_datetime(df['referenceTime'])
    daily_precip = (
        df.groupby(df['referenceTime'].dt.date)['total_precipitation']
        .sum()
        .reset_index(name='daily_precipitation')
    )
    daily_precip['date'] = pd.to_datetime(daily_precip['referenceTime'])  # Konverter til datetime
    daily_precip['month'] = daily_precip['date'].dt.month  # Ekstraher måned

    # Beregn gjennomsnitt og standardavvik for daglig nedbør per måned
    monthly_stats = daily_precip.groupby('month')['daily_precipitation'].agg(['mean', 'std'])

    # Månednavn for x-aksen
    months = [calendar.month_abbr[m] for m in range(1, 13)]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.bar(monthly_stats.index, monthly_stats['mean'],
        yerr=monthly_stats['std'], capsize=5, color='#4A90E2', edgecolor='black', alpha=0.85)

    # Legg til tittel og akseetiketter
    plt.title('Gjennomsnittlig daglig nedbør per måned (med standardavvik)', fontsize=14)
    plt.xlabel('Måned', fontsize=12)
    plt.ylabel('Nedbør (mm)', fontsize=12)

    # Tilpass x-aksen med månednavn og roter etikettene
    plt.xticks(range(1, 13), months, rotation=45)

    # Sett y-aksens grense for å gi plass til feilmarginer
    plt.ylim(0, monthly_stats['mean'].max() + monthly_stats['std'].max() + 1)

    # Legg til horisontale gridlinjer for bedre lesbarhet
    plt.grid(axis='y', linestyle='--', alpha=0.5)

    # Legg til verdier over hver stolpe
    for month, mean_val in monthly_stats['mean'].items():
        plt.text(month, mean_val + 0.1, f'{mean_val:.2f}', ha='center', va='bottom', fontsize=10)

    # Juster layout for å unngå overlapp mellom elementer
    plt.tight_layout()

    # Vis figuren
    plt.show()
