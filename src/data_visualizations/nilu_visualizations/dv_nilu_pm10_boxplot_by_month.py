import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json

def show_pm10(json_path):
    """
    Visualiserer månedlige PM10-nivåer ved hjelp av et boxplot.

    Args:
        json_path (str): Filsti til JSON-filen som inneholder NILU-data.
    """
    # Laster inn renset NILU-data fra JSON-fil
    with open(json_path, "r") as f:
        data = json.load(f)

    # Konverterer data til en DataFrame
    df = pd.DataFrame(data)
    df['dateTime'] = pd.to_datetime(df['dateTime'])  # Konverterer 'dateTime' til datetime-format

    # Legger til kolonner for månednavn og månednummer
    df['month'] = df['dateTime'].dt.strftime('%b')  # Månednavn (kort format, f.eks. Jan)
    df['month_num'] = df['dateTime'].dt.month  # Måned som tall

    # Sorterer DataFrame for riktig månedrekkefølge
    df = df.sort_values('month_num')

    # Oppretter boxplot for å vise fordelingen av PM10-nivåer per måned
    plt.figure(figsize=(12, 6))  # Setter figurstørrelse
    sns.boxplot(data=df, x='month', y='PM10', palette='Blues', fliersize=3)  # Boxplot med fargepalett
    plt.title("Boxplot av månedlige PM10-nivå (μg/m³)", fontsize=14)  # Tittel for plottet
    plt.xlabel("Måned", fontsize=12)  # Etikett for x-aksen
    plt.ylabel("PM10-nivå (μg/m³)", fontsize=12)  # Etikett for y-aksen
    plt.tight_layout()  # Justerer layout for å unngå overlapp mellom elementer
    plt.show()  # Viser plottet