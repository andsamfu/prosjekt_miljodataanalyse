import sqlite3
import pandas as pd
import plotly.graph_objects as go

# Definerer stien til databasen
database_file = 'data/raw/raw_frost_weather_trondheim_2010_to_2019.db'

# Opprett en tilkobling til databasen
conn = sqlite3.connect(database_file)

# Les data fra databasen
query = "SELECT * FROM weather_data"
df = pd.read_sql_query(query, conn)

# Lukk tilkoblingen
conn.close()

# Konverter 'date' kolonnen til datetime-format
df['date'] = pd.to_datetime(df['date'])

# Sett 'date' som indeks
df.set_index('date', inplace=True)

# Funksjon for å resample data
def resample_data(df, freq):
    return df.resample(freq).mean()

# Opprett en figur
fig = go.Figure()

# Legg til spor for hver type data
fig.add_trace(go.Scatter(x=df.index, y=df['mean_air_temperature'], mode='lines', name='°C', visible=True))
fig.add_trace(go.Scatter(x=df.index, y=df['total_precipitation'], mode='lines', name='mm', visible=False))
fig.add_trace(go.Scatter(x=df.index, y=df['mean_wind_speed'], mode='lines', name='m/s', visible=False))

# Opprett knapper for å velge mellom temperatur, nedbør og vindhastighet
fig.update_layout(
    updatemenus=[
        {
            'type': 'buttons',
            'buttons': [
                {
                    'label': 'Temperatur',
                    'method': 'update',
                    'args': [{'visible': [True, False, False]},
                              {'title': 'Temperatur (Daglig)'}]
                },
                {
                    'label': 'Nedbør',
                    'method': 'update',
                    'args': [{'visible': [False, True, False]},
                              {'title': 'Nedbør (Daglig)'}]
                },
                {
                    'label': 'Vindhastighet',
                    'method': 'update',
                    'args': [{'visible': [False, False, True]},
                              {'title': 'Vindhastighet (Daglig)'}]
                }
            ],
            'direction': 'right',  # Endret til horisontal
            'showactive': True,
            'x': 0.5,  # Plassering av knappene
            'xanchor': 'center',
            'y': 1.2,
            'yanchor': 'top'
        }
    ]
)

# Legg til range slider
fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(label="1y", step="year", stepmode="backward"),
                dict(label="All", step="all")
            ])
        ),
        rangeslider=dict(visible=True),
        type="date"
    )
)

# Legg til slider for å velge mellom daglig, ukentlig og månedlig data
fig.update_layout(
    sliders=[{
        'active': 0,
        'currentvalue': {'prefix': 'Vis data som: '},
        'pad': {'b': 10},
        'len': 0.9,
        'x': 0.1,
        'y': -0.2,
        'steps': [
            {
                'label': 'Dag',
                'method': 'update',
                'args': [{'x': [df.index, df.index, df.index],
                           'y': [df['mean_air_temperature'], df['total_precipitation'], df['mean_wind_speed']]},
                          {'title': 'Temperatur (Daglig)'}]
            },
            {
                'label': 'Uke',
                'method': 'update',
                'args': [{'x': [resample_data(df, 'W').index, resample_data(df, 'W').index, resample_data(df, 'W').index],
                           'y': [resample_data(df, 'W')['mean_air_temperature'], resample_data(df, 'W')['total_precipitation'], resample_data(df, 'W')['mean_wind_speed']]},
                          {'title': 'Temperatur (Ukentlig)'}]
            },
            {
                'label': 'Måned',
                'method': 'update',
                'args': [{'x': [resample_data(df, 'ME').index, resample_data(df, 'ME').index, resample_data(df, 'ME').index],
                           'y': [resample_data(df, 'ME')['mean_air_temperature'], resample_data(df, 'ME')['total_precipitation'], resample_data(df, 'ME')['mean_wind_speed']]},
                          {'title': 'Temperatur (Månedlig)'}]
            }
        ]
    }]
)

# Oppdater layout
fig.update_layout(title='Værdata i Trondheim (2010-2019)', xaxis_title='Dato', yaxis_title='Verdi')

# Vis grafen
fig.show()
