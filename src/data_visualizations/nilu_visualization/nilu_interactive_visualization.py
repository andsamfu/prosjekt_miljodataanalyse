import pandas as pd
import plotly.express as px

# Last inn datasettet
df = pd.read_json('data/clean/cleaned_data_nilu.json')  # riktig måte å lese en JSON-fil

# Konverter dato og legg til år og sesong
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

# Kolonner å analysere
columns_to_analyze = ['NO2', 'PM10', 'PM2.5']
df[columns_to_analyze] = df[columns_to_analyze].fillna(df[columns_to_analyze].median())

# Aggreger per år og sesong
seasonal_avg = df.groupby(['year', 'season'])[columns_to_analyze].mean().reset_index()

# Melt til long format
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
              title='Gjennomsnittlig luftkvalitet per år og sesong (interaktiv)',
              labels={'Average': 'Konsentrasjon (µg/m³)', 'year': 'År'},
              category_orders={"season": ["Vinter", "Vår", "Sommer", "Høst"]},
              template='plotly_white')

fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

# Juster x-akse ticks
years = sorted(df_long['year'].unique())[::2]
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

fig.show()
