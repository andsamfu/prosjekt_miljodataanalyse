import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3

def plot_temperature_vs_pm25(nilu_json_path, frost_db_path):
    """
    Visualiserer sammenhengen mellom daglig middeltemperatur (FROST) og PM2.5 (NILU) per sesong
    ved hjelp av regresjonsplot.

    Args:
        nilu_json_path (str): Filsti til JSON-filen som inneholder NILU-data.
        frost_db_path (str): Filsti til SQLite-databasen som inneholder FROST-data.
    """
    # Last inn daglig NILU-data
    nilu = pd.read_json(nilu_json_path)
    nilu['dateTime'] = pd.to_datetime(nilu['dateTime'])  # Konverter til datetime-format

    # Last inn daglig FROST-data
    conn = sqlite3.connect(frost_db_path)
    frost = pd.read_sql("SELECT referenceTime, mean_air_temperature FROM weather_data", conn)
    conn.close()  # Lukk tilkoblingen til databasen
    frost['referenceTime'] = pd.to_datetime(frost['referenceTime'])  # Konverter til datetime-format

    # Merge data på dato
    nilu['date'] = nilu['dateTime'].dt.date  # Ekstraher dato fra NILU-data
    frost['date'] = frost['referenceTime'].dt.date  # Ekstraher dato fra FROST-data
    merged = pd.merge(nilu, frost, on='date')  # Slå sammen datasettene basert på dato

    # Legg til sesong basert på måned
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'

    merged['season'] = pd.to_datetime(merged['date']).dt.month.apply(get_season)

    # Fjern manglende verdier
    merged = merged.dropna(subset=['mean_air_temperature', 'PM2.5'])

    # Definer farger for hver sesong
    season_colors = {
        "Winter": "steelblue",
        "Spring": "mediumseagreen",
        "Summer": "goldenrod",
        "Fall": "sienna"
    }

    # Forklaringer for hver sesong
    explanations = {
        "Winter": "Negativ trend: Høyere PM2.5 ved lavere temperaturer",
        "Spring": "Svak positiv trend: Liten økning i PM2.5 ved økt temperatur",
        "Summer": "Lite mønster: Svak og usikker positiv sammenheng",
        "Fall":   "Negativ trend: PM2.5 synker svakt med høyere temperatur"
    }

    # Opprett regresjonsplot for hver sesong
    sns.set(style="whitegrid")  # Sett stil for plottet
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))  # Opprett 2x2 plot
    fig.suptitle("Daglig regresjon per sesong: Temperatur (FROST) vs PM2.5 (NILU)", fontsize=16, y=1.03)

    seasons = ["Winter", "Spring", "Summer", "Fall"]
    axes = axes.flatten()

    for i, season in enumerate(seasons):
        # Filtrer data for gjeldende sesong
        data = merged[merged['season'] == season]
        point_color = season_colors[season]

        # Opprett regresjonsplot
        sns.regplot(
            data=data,
            x='mean_air_temperature',
            y='PM2.5',
            ax=axes[i],
            scatter_kws={"s": 10, "alpha": 0.3, "color": point_color},  # Stil for datapunkter
            line_kws={"color": "crimson", "lw": 2},  # Stil for regresjonslinjen
            color="crimson",
            ci=95  # Konfidensintervall
        )

        # Legg til tittel og akseetiketter
        axes[i].set_title(season, fontsize=14)
        axes[i].set_xlabel("Temperatur (°C)")
        axes[i].set_ylabel("PM₂.₅ (µg/m³)")
        axes[i].grid(True)  # Legg til gridlinjer

        # Legg til forklaring for sesongen
        axes[i].text(
            0.05, 0.9, explanations[season],
            transform=axes[i].transAxes,
            fontsize=10, color="black",
            bbox=dict(facecolor="lightgrey", edgecolor="none", boxstyle="round,pad=0.4")
        )

    # Undertittel for hele figuren
    plt.figtext(
        0.5, 0.965,
        "Regresjonsanalyse av daglige verdier: Sammenheng mellom temperatur (FROST) og PM2.5 (NILU) per sesong",
        ha="center", fontsize=12, fontweight='bold'
    )

    # Juster layout for å unngå overlapp mellom elementer
    plt.tight_layout(rect=[0, 0, 1, 0.94])

    # Vis figuren
    plt.show()


