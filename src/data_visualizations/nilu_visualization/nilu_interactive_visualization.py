import pandas as pd
import plotly.express as px

def vis_luftkvalitet_per_sesong(json_path):
    # 1. Last inn datasettet
    df = pd.read_json(json_path)

    # 2. Konverter dato og legg til år og sesong
    df['dateTime'] = pd.to_datetime(df['dateTime'])
    df['year'] = df['dateTime'].dt.year

    def get_season(month):
        if month in [12, 1, 2]:
            return "Vinter"
        elif month in [3, 4, 5]:
            return "Vår"
        elif month in [6, 7, 8]:
            return "Sommer"
        elif month in [9, 10, 11]:
            return "Høst"

    df['season'] = df['dateTime'].dt.month.apply(get_season)

    # 3. Håndter manglende verdier
    columns_to_analyze = ['NO2', 'PM10', 'PM2.5']
    df[columns_to_analyze] = df[columns_to_analyze].fillna(df[columns_to_analyze].median())

    # 4. Aggreger data: Gjennomsnitt per år og sesong
    seasonal_avg = df.groupby(['year', 'season'])[columns_to_analyze].mean().reset_index()

    # 5. Smelt (melt) data for Plotly (long format)
    df_long = seasonal_avg.melt(id_vars=['year', 'season'], 
                                value_vars=columns_to_analyze, 
                                var_name='Pollutant', 
                                value_name='Average')

    # 6. Interaktiv graf – luftkvalitet per sesong over år
    fig = px.line(df_long, 
                  x='year', 
                  y='Average', 
                  color='Pollutant', 
                  line_group='Pollutant',
                  facet_col='season', 
                  markers=True,
                  title='Gjennomsnittlig luftkvalitet per år og sesong (interaktiv)',
                  labels={'Average': 'Konsentrasjon (µg/m³)', 'year': 'År'},
                  category_orders={"season": ["Vinter", "Vår", "Sommer", "Høst"]},
                  template='plotly_white')

    # 7. Fjern "season=" fra titlene i subplotene
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

    # 8. Layout tweaks: full width og høyde
    fig.update_layout(
        hovermode="x unified",
        legend_title_text='Stoff',
        height=None,
        width=None
    )

    fig.show()
