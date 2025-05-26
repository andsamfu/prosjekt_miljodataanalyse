import os
import json
import pandas as pd
import plotly.graph_objects as go

def get_cleaned_data_path(filename):
    """
    Genererer filstien til en renset datafil i 'data/clean'-mappen.

    Args:
        filename (str): Navnet på filen.

    Returns:
        str: Full filsti til den rensede datafilen.
    """
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'data', 'clean', filename
    )

def nilu_plotly(json_file_path):
    """
    Visualiserer NILU-luftkvalitetsdata (NO2, PM2.5, PM10) ved hjelp av Plotly.

    Args:
        json_file_path (str): Filsti til JSON-filen som inneholder NILU-data.

    Returns:
        plotly.graph_objects.Figure: En interaktiv figur med luftkvalitetsdata.
    """
    # Laster inn data fra JSON-filen
    with open(json_file_path, 'r') as file:
        df = pd.DataFrame(json.load(file))
    
    # Konverterer 'dateTime' til datetime-format for enklere håndtering
    df['dateTime'] = pd.to_datetime(df['dateTime'])
    
    # Oppretter en Plotly-figur med linjediagrammer for NO2, PM2.5 og PM10
    fig = go.Figure([
        go.Scatter(
            x=df['dateTime'], 
            y=df[column], 
            mode='lines', 
            name=column  # Navn på datasettet
        )
        for column in ['NO2', 'PM2.5', 'PM10']  # Itererer over luftkvalitetskomponenter
    ])
    
    # Oppdaterer layout for figuren
    fig.update_layout(
        title='Luftkvalitetsdata Visualisering (NO2, PM2.5, PM10)',  # Tittel for figuren
        xaxis=dict(
            title='Tid',  # Tittel for x-aksen
            rangeselector=dict(  # Legger til knapper for å velge tidsintervall
                buttons=[
                    dict(count=1, label="1 måned", step="month", stepmode="backward"),
                    dict(count=6, label="6 måneder", step="month", stepmode="backward"),
                    dict(count=1, label="1 år", step="year", stepmode="backward"),
                    dict(step="all", label="Alle")  # Viser hele datasettet
                ]
            ),
            rangeslider=dict(visible=True),  # Legger til en skyvebryter for tidsutvalg
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
    
    return fig  # Returnerer den interaktive figuren
