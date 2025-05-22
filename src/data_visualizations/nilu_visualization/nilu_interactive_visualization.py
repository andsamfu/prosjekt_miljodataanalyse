import pandas as pd
import plotly.express as px
import json

def plot_seasonal_air_quality(json_path: str):
    """
    Leser inn NILU-data fra en JSON-fil, beregner sesongbaserte luftforurensningsgjennomsnitt,
    og viser en interaktiv linjegraf delt på sesong.

    Parametre:
    - json_path (str): Filsti til renset NILU-JSON (f.eks. 'data/clean/cleaned_data_nilu.json')
    """

    # 1. Last inn JSON manuelt
    with open(json_path, "r") as f:
        data = json.load(f)

    # 2. Lag DataFrame
    df = pd.DataFrame(data)
    df['dateTime'] = pd.to_datetime(df['dateTime'])
    df['year'] = df['dateTime'].dt.year

    # 3. Legg til sesong
    def get_season(month):
        if month in [12, 1, 2]:
            return "Vinter"
        elif month in [3, 4, 5]:
            return "Vår"
        elif month in [6, 7, 8]:
            return "Sommer"
        else:
            return "Høst"

    df['season'] = df['dateTime'].dt.month.apply(get_season)

    # 4. Kolonner å analysere (forutsetter at data er ferdigrenset)
    columns_to_analyze = ['NO2', 'PM10', 'PM2.5']

    # 5. Aggregering
    seasonal_avg = df.groupby(['year', 'season'])[columns_to_analyze].mean(numeric_only=True).reset_index()

    # 6. Melt til long-format
    df_long = seasonal_avg.melt(
        id_vars=['year', 'season'],
        value_vars=columns_to_analyze,
        var_name='Pollutant',
        value_name='Average'
    )

    # 7. Lag interaktiv graf
    fig = px.line(
        df_long,
        x='year',
        y='Average',
        color='Pollutant',
        line_group='Pollutant',
        facet_col='season',
        markers=True,
        line_shape='spline',
        title='Gjennomsnittlig luftkvalitet per år og sesong (interaktiv)',
        labels={'Average': 'Konsentrasjon (µg/m³)', 'year': 'År'},
        category_orders={"season": ["Vinter", "Vår", "Sommer", "Høst"]},
        template='plotly_white'
    )

    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

    # 8. Tilpass x-aksene
    years = sorted(df_long['year'].unique())[::2]
    for axis in fig.layout:
        if axis.startswith('xaxis'):
            fig.layout[axis].update(
                tickmode='array',
                tickvals=years,
                tickangle=45,
                tickfont=dict(size=9)
            )

    # 9. Layout-tilpasninger
    fig.update_layout(
        plot_bgcolor='#e0e0e0',
        paper_bgcolor='#e0e0e0',
        hovermode="x unified",
        legend_title_text='Stoff',
        height=500,
        width=None,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.05,
            xanchor='center',
            x=0.5
        ),
        title_x=0.5
    )

    # 10. Vis graf
    fig.show()
