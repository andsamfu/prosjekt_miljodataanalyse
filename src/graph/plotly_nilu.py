import json
import pandas as pd
import plotly.graph_objects as go
import os

# Filsti til JSON-filen
file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data', 'clean', 'cleaned_data_nilu.json')

# Les inn data og opprett DataFrame
with open(file_path, 'r') as file:
    df = pd.DataFrame(json.load(file))

# Konverter 'dateTime' til datetime-format
df['dateTime'] = pd.to_datetime(df['dateTime'])

# Opprett graf
fig = go.Figure([
    go.Scatter(x=df['dateTime'], y=df[column], mode='lines', name=column)
    for column in ['NO2', 'PM2.5', 'PM10']
])

# Konfigurer layout
fig.update_layout(
    title='Luftkvalitetsdata visualisering (NO2, PM2.5, PM10)',
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
    yaxis=dict(title='Konsentrasjon'),
    legend=dict(title="Målinger", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

fig.show()