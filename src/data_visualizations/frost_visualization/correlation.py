import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def vis_frost_korrelasjon(csv_filsti):
    """
    Visualiserer korrelasjonsmatrisen for værdata ved hjelp av et heatmap.

    Args:
        csv_filsti (str): Filsti til CSV-filen som inneholder korrelasjonsmatrisen.
    """
    # Leser inn korrelasjonsmatrise fra CSV-fil
    df = pd.read_csv(csv_filsti, index_col=0)
    
    # Lager et heatmap for å vise korrelasjon mellom variabler
    plt.figure(figsize=(8, 6))
    sns.heatmap(df, annot=True, cmap='OrRd', vmin=0, vmax=1, fmt='.2f', linewidths=0.5, linecolor='gray')
    
    # Legger til tittel og justerer layout
    plt.title('Korrelasjon mellom temperatur, nedbør og vind')  # Tittel for heatmap
    plt.tight_layout()  # Justerer layout for å unngå overlapp
    plt.show()  # Viser heatmap
