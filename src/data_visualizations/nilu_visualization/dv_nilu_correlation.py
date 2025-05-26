import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def vis_korrelasjon_nilu(csv_path):
    """
    Visualiserer korrelasjonsmatrisen for NILU-data ved hjelp av et heatmap.

    Args:
        csv_path (str): Filsti til CSV-filen som inneholder korrelasjonsmatrisen for NILU-data.
    """
    # Leser inn korrelasjonsmatrise fra CSV-fil
    corr_df = pd.read_csv(csv_path, index_col=0)  # Bruk første kolonne som indeks

    # Opprett en figur og lag et heatmap
    plt.figure(figsize=(8, 6))  # Sett figurstørrelse
    sns.heatmap(
        corr_df, 
        annot=True,  # Vis verdier i cellene
        cmap='OrRd',  # Fargekart (oransje-rød)
        vmin=0, vmax=1,  # Verdiskala fra 0 til 1
        fmt='.2f'  # Format for verdier (to desimaler)
    )

    # Legg til tittel og juster layout
    plt.title('Korrelasjon mellom NO₂, PM10 og PM2.5', fontsize=14)  # Tittel for heatmap
    plt.tight_layout()  # Juster layout for å unngå overlapp mellom elementer

    # Vis figuren
    plt.show()
