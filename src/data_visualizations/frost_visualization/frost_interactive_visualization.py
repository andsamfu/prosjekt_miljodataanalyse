import pandas as pd
import plotly.express as px
import sqlite3

# Koble til SQLite-database og les inn data
conn = sqlite3.connect('data/clean/frost.db')
df = pd.read_sql('SELECT * FROM weather_data', conn)
conn.close()

# Konverterer 'referenceTime' til datetime-format
df['referenceTime'] = pd.to_datetime(df['referenceTime'])

# Definer årstid basert på måned
def get_season(month):
    if month in [12, 1, 2]:
        return 'Vinter'
    elif month in [3, 4, 5]:
        return 'Vår'
    elif month in [6, 7, 8]:
        return 'Sommer'
    else:
        return 'Høst'

# Legg til sesong og år
df['season'] = df['referenceTime'].dt.month.apply(get_season)
df['year'] = df['referenceTime'].dt.year

# Relevante kolonner
columns_to_analyze = ['mean_air_temperature', 'total_precipitation', 'mean_wind_speed']

# Fyll manglende verdier med median
df[columns_to_analyze] = df[columns_to_analyze].fillna(df[columns_to_analyze].median())

# Beregn snitt per sesong og år
seasonal_avg = df.groupby(['year', 'season'])[columns_to_analyze].mean().reset_index()

# Gjør data langformat for plotting
df_long = seasonal_avg.melt(id_vars=['year', 'season'], 
                            value_vars=columns_to_analyze, 
                            var_name='Pollutant', 
                            value_name='Average')

# Lag graf
fig = px.line(df_long, 
              x='year', 
              y='Average', 
              color='Pollutant', 
              line_group='Pollutant',
              facet_col='season', 
              markers=True,
              line_shape='spline',
              title='Gjennomsnittlig temperatur, nedbør og vindhastighet per år og sesong (interaktiv)',
              labels={'Average': 'Verdi', 'year': 'År'},
              category_orders={"season": ["Vinter", "Vår", "Sommer", "Høst"]},
              template='plotly_white')

fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

# Juster x-akse for alle subplot
years = sorted(df_long['year'].unique())
for axis in fig.layout:
    if axis.startswith('xaxis'):
        fig.layout[axis].update(
            tickmode='array',
            tickvals=years,
            tickangle=45,
            tickfont=dict(size=9)
        )

# Oppsett og layout
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
