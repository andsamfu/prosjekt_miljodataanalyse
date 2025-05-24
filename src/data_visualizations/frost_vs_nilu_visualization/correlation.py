import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def vis_korrelasjoner_sammen(frost_csv, nilu_csv):
    """
    Visualiserer korrelasjonsmatriser for FROST- og NILU-data ved hjelp av heatmaps.

    Args:
        frost_csv (str): Filsti til CSV-filen som inneholder korrelasjonsmatrisen for FROST-data.
        nilu_csv (str): Filsti til CSV-filen som inneholder korrelasjonsmatrisen for NILU-data.
    """
    # Les inn korrelasjonsmatriser fra CSV-filer
    frost_df = pd.read_csv(frost_csv, index_col=0)  # FROST-data
    nilu_df = pd.read_csv(nilu_csv, index_col=0)  # NILU-data

    # Opprett en figur med to subplot (side ved side)
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))  # 1 rad, 2 kolonner

    # Heatmap for FROST-data
    sns.heatmap(
        frost_df, 
        annot=True,  # Vis verdier i cellene
        cmap='OrRd',  # Fargekart (oransje-rød)
        vmin=0, vmax=1,  # Verdiskala fra 0 til 1
        fmt='.2f',  # Format for verdier (to desimaler)
        linewidths=0.5,  # Linjetykkelse mellom celler
        linecolor='gray',  # Farge på linjene
        ax=axes[0]  # Plasser heatmap i første subplot
    )
    axes[0].set_title('Korrelasjon mellom temperatur, nedbør og vind')  # Tittel for første plot

    # Heatmap for NILU-data
    sns.heatmap(
        nilu_df, 
        annot=True,  
        cmap='OrRd',  
        vmin=0, vmax=1,  
        fmt='.2f',  
        ax=axes[1]  
    )
    axes[1].set_title('Korrelasjon mellom NO2, PM10 og PM2.5')  # Tittel for andre bplot

    # Juster layout for å unngå overlapp mellom elementer
    plt.tight_layout()

    # Vis figuren
    plt.show()