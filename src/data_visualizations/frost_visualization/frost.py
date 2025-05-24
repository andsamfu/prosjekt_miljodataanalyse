import sqlite3
import pandas as pd
import plotly.graph_objects as go

def plot_weather_data(db_path="data/clean/frost.db"):
    # Koble til database og hent data
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("""
        SELECT referenceTime, mean_air_temperature, total_precipitation, mean_wind_speed
        FROM weather_data
        WHERE referenceTime IS NOT NULL
    """, conn)
    conn.close()

    # Konverter tid til datetime-format
    df['referenceTime'] = pd.to_datetime(df['referenceTime'])

    # Initialiser figur
    fig = go.Figure()

    # Temperatur - rød, myk linje
    fig.add_trace(go.Scatter(
        x=df['referenceTime'],
        y=df['mean_air_temperature'],
        mode='lines',
        name='Temperatur (°C)',
        line=dict(color='#E74C3C', shape='spline', smoothing=1.3),
        visible=True
    ))

    # Nedbør - blå, myk linje
    fig.add_trace(go.Scatter(
        x=df['referenceTime'],
        y=df['total_precipitation'],
        mode='lines',
        name='Nedbør (mm)',
        line=dict(color='#3498DB', shape='spline', smoothing=1.3),
        visible=False
    ))

    # Vindhastighet - grønn, myk linje
    fig.add_trace(go.Scatter(
        x=df['referenceTime'],
        y=df['mean_wind_speed'],
        mode='lines',
        name='Vindhastighet (m/s)',
        line=dict(color='#27AE60', shape='spline', smoothing=1.3),
        visible=False
    ))

    # Layout og interaktivitet
    fig.update_layout(
        title='Værdata i Trondheim',
        xaxis=dict(
            title='Tid',
            rangeselector=dict(
                buttons=[
                    dict(count=1, label="1 måned", step="month", stepmode="backward"),
                    dict(count=6, label="6 måneder", step="month", stepmode="backward"),
                    dict(count=1, label="1 år", step="year", stepmode="backward"),
                    dict(step="all", label="Alle")
                ]
            ),
            rangeslider=dict(visible=True),
            type="date"
        ),
        yaxis=dict(title='Temperatur (°C)'),
        legend=dict(title="Målinger", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        updatemenus=[dict(
            type="buttons",
            direction="right",
            showactive=True,
            x=1,
            xanchor="right",
            y=1.02,
            yanchor="bottom",
            pad={"r": 10, "t": 10},
            buttons=list([
                dict(label="Temperatur",
                     method="update",
                     args=[{"visible": [True, False, False]},
                           {"yaxis.title.text": "Temperatur (°C)"}]),
                dict(label="Nedbør",
                     method="update",
                     args=[{"visible": [False, True, False]},
                           {"yaxis.title.text": "Nedbør (mm)"}]),
                dict(label="Vindhastighet",
                     method="update",
                     args=[{"visible": [False, False, True]},
                           {"yaxis.title.text": "Vindhastighet (m/s)"}]),
            ])
        )]
    )

    return fig
