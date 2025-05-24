import sqlite3
import pandas as pd
import plotly.graph_objects as go

def plot_weather_data(db_path="data/clean/frost.db"):
    """
    Visualiserer værdata fra en SQLite-database ved hjelp av Plotly.

    Args:
        db_path (str): Filsti til SQLite-databasen som inneholder værdata.

    Returns:
        plotly.graph_objects.Figure: En interaktiv figur med værdata.
    """
    # Koble til databasen og hent data
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("""
        SELECT referenceTime, mean_air_temperature, total_precipitation, mean_wind_speed
        FROM weather_data
        WHERE referenceTime IS NOT NULL
    """, conn)
    conn.close()  # Lukk tilkoblingen til databasen

    # Konverter 'referenceTime' til datetime-format
    df['referenceTime'] = pd.to_datetime(df['referenceTime'])

    # Initialiser figuren
    fig = go.Figure()

    # Legg til temperaturdata som en rød linje
    fig.add_trace(go.Scatter(
        x=df['referenceTime'],
        y=df['mean_air_temperature'],
        mode='lines',
        name='Temperatur (°C)', 
        line=dict(color='#E74C3C', shape='spline', smoothing=1.3), 
        visible=True  # Gjør denne linjen synlig som standard
    ))

    # Legg til nedbørsdata som en blå linje
    fig.add_trace(go.Scatter(
        x=df['referenceTime'],
        y=df['total_precipitation'],
        mode='lines',
        name='Nedbør (mm)',  
        line=dict(color='#3498DB', shape='spline', smoothing=1.3),  
        visible=False  # Skjul denne linjen som standard
    ))

    # Legg til vindhastighetsdata som en grønn linje
    fig.add_trace(go.Scatter(
        x=df['referenceTime'],
        y=df['mean_wind_speed'],
        mode='lines',
        name='Vindhastighet (m/s)', 
        line=dict(color='#27AE60', shape='spline', smoothing=1.3),  
        visible=False  # Skjul denne linjen som standard
    ))

    # Oppdater layout og legg til interaktivitet
    fig.update_layout(
        title='Værdata i Trondheim',  
        xaxis=dict(
            title='Tid', 
            rangeselector=dict(  # Legg til knapper for å velge tidsintervall
                buttons=[
                    dict(count=1, label="1 måned", step="month", stepmode="backward"),
                    dict(count=6, label="6 måneder", step="month", stepmode="backward"),
                    dict(count=1, label="1 år", step="year", stepmode="backward"),
                    dict(step="all", label="Alle") 
                ]
            ),
            rangeslider=dict(visible=True),  # Legg til en glider for tidsutvalg
            type="date"  # Angi at x-aksen viser datoer
        ),
        yaxis=dict(title='Temperatur (°C)'), 
        legend=dict(
            title="Målinger", 
            orientation="h",  
            yanchor="bottom", y=1.02,  
            xanchor="right", x=1  
        ),
        updatemenus=[dict(  # Legg til knapper for å bytte mellom datasett
            type="buttons",
            direction="right",  # Knappene vises horisontalt
            showactive=True,  # Marker aktiv knapp
            x=1, xanchor="right",  # Plassering til høyre
            y=1.02, yanchor="bottom",  # Plassering over figuren
            pad={"r": 10, "t": 10},  # Justering av avstand
            buttons=list([
                dict(label="Temperatur",
                     method="update",
                     args=[{"visible": [True, False, False]},  # Vis kun temperatur
                           {"yaxis.title.text": "Temperatur (°C)"}]),
                dict(label="Nedbør",
                     method="update",
                     args=[{"visible": [False, True, False]},  # Vis kun nedbør
                           {"yaxis.title.text": "Nedbør (mm)"}]),
                dict(label="Vindhastighet",
                     method="update",
                     args=[{"visible": [False, False, True]},  # Vis kun vindhastighet
                           {"yaxis.title.text": "Vindhastighet (m/s)"}]),
            ])
        )]
    )
    # Returnerer figuren
    return fig  
