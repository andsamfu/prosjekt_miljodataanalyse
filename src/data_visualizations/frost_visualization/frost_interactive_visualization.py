import pandas as pd
import plotly.express as px
import sqlite3

def vis_vaerdata_per_sesong(db_path):
    # 1. Last inn data fra SQLite-databasen
    conn = sqlite3.connect(db_path)
    df = pd.read_sql('SELECT * FROM weather_data', conn)
    conn.close()

    # 2. Konverter 'referenceTime' til datetime-format
    df['referenceTime'] = pd.to_datetime(df['referenceTime'])

    # 3. Definer årstider
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Vinter'
        elif month in [3, 4, 5]:
            return 'Vår'
        elif month in [6, 7, 8]:
            return 'Sommer'
        else:
            return 'Høst'

    df['season'] = df['referenceTime'].dt.month.apply(get_season)
    df['year'] = df['referenceTime'].dt.year

    # 4. Kolonner å analysere
    columns_to_analyze = ['mean_air_temperature', 'total_precipitation', 'mean_wind_speed']

    # 5. Manglende verdier → median
    df[columns_to_analyze] = df[columns_to_analyze].fillna(df[columns_to_analyze].median())

    # 6. Aggreger per år og sesong
    seasonal_avg = df.groupby(['year', 'season'])[columns_to_analyze].mean().reset_index()

    # 7. Smelt data for Plotly
    df_long = seasonal_avg.melt(id_vars=['year', 'season'], 
                                value_vars=columns_to_analyze, 
                                var_name='Variable', 
                                value_name='Average')

    # 8. Interaktiv graf
    fig = px.line(df_long, 
                  x='year', 
                  y='Average', 
                  color='Variable', 
                  line_group='Variable',
                  facet_col='season', 
                  markers=True,
                  title='Gjennomsnittlig temperatur, nedbør og vindhastighet per år og sesong (interaktiv)',
                  labels={'Average': 'Verdi', 'year': 'År'},
                  category_orders={"season": ["Vinter", "Vår", "Sommer", "Høst"]},
                  template='plotly_white')

    # 9. Fjern "season=" fra subplot-titler
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

    # 10. Layout
    fig.update_layout(
        hovermode="x unified",
        legend_title_text='Variabel',
        height=None,
        width=None
    )

    fig.show()
