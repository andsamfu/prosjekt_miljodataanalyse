import json
import pandas as pd
import plotly.graph_objects as go
import os

# Returnerer filstien til JSON-filen
def get_file_path():
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'data', 'clean', 'cleaned_data_nilu.json'
    )

# Laster inn data fra JSON-filen og returnerer en Pandas DataFrame
def load_data(file_path):
    with open(file_path, 'r') as file:
        df = pd.DataFrame(json.load(file))

    # Konverterer 'dateTime' til datetime-format    
    df['dateTime'] = pd.to_datetime(df['dateTime'])  
    return df

# Oppretter og returnerer en Plotly-figur basert på DataFrame
def create_figure(df):
    fig = go.Figure([
        go.Scatter(x=df['dateTime'], y=df[column], mode='lines', name=column)
        for column in ['NO2', 'PM2.5', 'PM10']
    ])

    fig.update_layout(
        title='Luftkvalitetsdata Visualisering (NO2, PM2.5, PM10)',
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

        yaxis=dict(title='Konsentrasjon (µg/m³)'),
        legend=dict(title="Målinger", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

# Hovedfunksjon som kjører hele programmet
def main():
    file_path = get_file_path()
    df = load_data(file_path)
    fig = create_figure(df)
    fig.show()


if __name__ == "__main__":
    main()