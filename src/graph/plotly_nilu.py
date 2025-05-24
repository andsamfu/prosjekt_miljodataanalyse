import json
import pandas as pd
import plotly.graph_objects as go
import os

def get_file_path():
    """
    Genererer filstien til JSON-filen som inneholder renset NILU-data.

    Returns:
        str: Full filsti til JSON-filen.
    """
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'data', 'clean', 'cleaned_data_nilu.json'
    )

def load_data(file_path):
    """
    Leser inn NILU-data fra en JSON-fil og konverterer den til en Pandas DataFrame.

    Args:
        file_path (str): Filsti til JSON-filen.

    Returns:
        pd.DataFrame: DataFrame med NILU-data, inkludert konvertert 'dateTime'-kolonne.
    """
    with open(file_path, 'r') as file:
        df = pd.DataFrame(json.load(file))

    # Konverterer 'dateTime' til datetime-format for enklere håndtering
    df['dateTime'] = pd.to_datetime(df['dateTime'])  
    return df

def create_figure(df):
    """
    Oppretter en interaktiv Plotly-figur som visualiserer NILU-data (NO2, PM2.5, PM10).

    Args:
        df (pd.DataFrame): DataFrame med NILU-data.

    Returns:
        plotly.graph_objects.Figure: En interaktiv figur med linjediagrammer.
    """
    # Oppretter linjediagrammer for hver luftkvalitetsvariabel
    fig = go.Figure([
        go.Scatter(
            x=df['dateTime'], 
            y=df[column], 
            mode='lines', 
            name=column  # Navn på datasettet
        )
        for column in ['NO2', 'PM2.5', 'PM10']
    ])

    # Oppdaterer layout for figuren
    fig.update_layout(
        title='Luftkvalitetsdata Visualisering (NO2, PM2.5, PM10)',  # Tittel for figuren
        xaxis=dict(
            title='Tid',  # Tittel for x-aksen
            rangeselector=dict(  # Legger til knapper for tidsintervall
                buttons=[
                    dict(count=1, label="1 måned", step="month", stepmode="backward"),
                    dict(count=6, label="6 måneder", step="month", stepmode="backward"),
                    dict(count=1, label="1 år", step="year", stepmode="backward"),
                    dict(step="all", label="Alle")  # Viser hele datasettet
                ]
            ),
            rangeslider=dict(visible=True),  # Skyvebryter for tidsutvalg
            type="date"  # Angir at x-aksen viser datoer
        ),
        yaxis=dict(title='Konsentrasjon (µg/m³)'),  # Tittel for y-aksen
        legend=dict(
            title="Målinger",  # Tittel for forklaringen
            orientation="h",  # Horisontal orientering
            yanchor="bottom", y=1.02,  # Plassering over figuren
            xanchor="right", x=1  # Justering til høyre
        )
    )
    return fig

def main():
    """
    Hovedfunksjon som kjører hele programmet:
    - Leser inn NILU-data.
    - Oppretter en interaktiv figur.
    - Viser figuren i nettleseren.
    """
    file_path = get_file_path()  # Genererer filstien
    df = load_data(file_path)  # Leser inn data
    fig = create_figure(df)  # Oppretter figuren
    fig.show()  # Viser figuren

    # Oppdaterer layout for hover og dimensjoner
    fig.update_layout(
        hovermode="x unified",  # Samlet hover-informasjon
        legend_title_text='Variabel',  # Tittel for forklaringen
        height=None,  # Standard høyde
        width=None  # Standard bredde
    )

if __name__ == "__main__":
    main()