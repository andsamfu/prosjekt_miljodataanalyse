import pandas as pd
import plotly.express as px
import sqlite3

def plot_seasonal_weather_from_sqlite(db_path: str, table_name: str = "weather_data"):
    """
    Leser værdata fra SQLite og visualiserer sesongvis utvikling av temperatur, nedbør og vindhastighet.

    Parametre:
    - db_path (str): Filsti til SQLite-database (f.eks. 'data/clean/cleaned_data_frost.db')
    - table_name (str): Navn på tabellen i databasen (default: 'weather_data')
    """

    # Hent data
    conn = sqlite3.connect(db_path)
    df = pd.read_sql(f'SELECT * FROM {table_name}', conn)
    conn.close()

    # Konverter dato
    df['referenceTime'] = pd.to_datetime(df['referenceTime'])
    df['year'] = df['referenceTime'].dt.year

    # Legg til sesong
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

    # Aggreger sesongvis (uten å fylle ut manglende)
    columns_to_analyze = ['mean_air_temperature', 'total_precipitation', 'mean_wind_speed']
    seasonal_avg = df.groupby(['year', 'season'])[columns_to_analyze].mean(numeric_only=True).reset_index()

    # Langformat for plot
    df_long = seasonal_avg.melt(
        id_vars=['year', 'season'],
        value_vars=columns_to_analyze,
        var_name='Variabel',
        value_name='Average'
    )

    # Plot
    fig = px.line(
        df_long,
        x='year',
        y='Average',
        color='Variabel',
        line_group='Variabel',
        facet_col='season',
        markers=True,
        line_shape='spline',
        title='Gjennomsnittlig temperatur, nedbør og vindhastighet per år og sesong (interaktiv)',
        labels={'Average': 'Verdi', 'year': 'År'},
        category_orders={"season": ["Vinter", "Vår", "Sommer", "Høst"]},
        template='plotly_white'
    )

    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

    # Juster x-aksene
    years = sorted(df_long['year'].unique())
    for axis in fig.layout:
        if axis.startswith('xaxis'):
            fig.layout[axis].update(
                tickmode='array',
                tickvals=years,
                tickangle=45,
                tickfont=dict(size=9)
            )

    # Layout
    fig.update_layout(
        plot_bgcolor='#e0e0e0',
        paper_bgcolor='#e0e0e0',
        hovermode="x unified",
        legend_title_text='Variabel',
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

    fig.show()
