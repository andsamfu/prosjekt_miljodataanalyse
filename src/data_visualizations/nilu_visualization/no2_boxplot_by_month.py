import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json

def vis_no2_per_måned(json_path):
    """
    Visualiserer månedlige NO2-nivåer ved hjelp av et boxplot.

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

    # Oppretter boxplot for å vise fordelingen av NO2-nivåer per måned
    plt.figure(figsize=(12, 6))  # Setter figurstørrelse
    sns.boxplot(data=df, x='month', y='NO2', palette='Blues', fliersize=3)  # Boxplot med fargepalett
    plt.title("Boxplot av månedlige NO2-nivå (μg/m³)", fontsize=14)  # Tittel for plottet
    plt.xlabel("Måned", fontsize=12)  # Etikett for x-aksen
    plt.ylabel("NO2 (μg/m³)", fontsize=12)  # Etikett for y-aksen
    plt.tight_layout()  # Justerer layout for å unngå overlapp mellom elementer
    plt.show()  # Viser plottet