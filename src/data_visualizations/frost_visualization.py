import pandas as pd
import plotly.express as px
import sqlite3

# 1. Last inn data fra SQLite-databasen
db_file = 'data/clean/frost.db'
conn = sqlite3.connect(db_file)
df = pd.read_sql('SELECT * FROM weather_data', conn)

# 2. Konverter 'referenceTime' til datetime-format
df['referenceTime'] = pd.to_datetime(df['referenceTime'])

# 3. Definer årstider basert på måned
def get_season(month):
    if month in [12, 1, 2]:
        return 'Vinter'
    elif month in [3, 4, 5]:
        return 'Vår'
    elif month in [6, 7, 8]:
        return 'Sommer'
    else:
        return 'Høst'

# Lag en ny kolonne som angir årstiden for hver rad
df['season'] = df['referenceTime'].dt.month.apply(get_season)

# Ekstraher år og lagre i en ny kolonne
df['year'] = df['referenceTime'].dt.year

# 4. Kolonnene for analyse (Temperatur, nedbør, vindhastighet)
columns_to_analyze = ['mean_air_temperature', 'total_precipitation', 'mean_wind_speed']

# 5. Håndtere manglende verdier (erstatte med median for hver kolonne)
df[columns_to_analyze] = df[columns_to_analyze].fillna(df[columns_to_analyze].median())

# 6. Aggreger data: Gjennomsnitt per år og sesong
seasonal_avg = df.groupby(['year', 'season'])[columns_to_analyze].mean().reset_index()

# 7. Smelt (melt) data for Plotly (long format)
df_long = seasonal_avg.melt(id_vars=['year', 'season'], 
                            value_vars=columns_to_analyze, 
                            var_name='Pollutant', 
                            value_name='Average')

# 8. Interaktiv graf – Luftkvalitet per sesong over år
fig = px.line(df_long, 
              x='year', 
              y='Average', 
              color='Pollutant', 
              line_group='Pollutant',
              facet_col='season', 
              markers=True,
              title='Gjennomsnittlig temperatur, nedbør og vindhastighet per år og sesong (interaktiv)',
              labels={'Average': 'Verdi', 'year': 'År'},
              category_orders={"season": ["Vinter", "Vår", "Sommer", "Høst"]},
              template='plotly_dark')

# 9. Fjern "season=" fra titlene i subplotene
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

# 10. Layout tweaks: full width og høyde
fig.update_layout(
    hovermode="x unified",
    legend_title_text='Variabel',
    height=800,
    width=None  # lar den fylle tilgjengelig bredde automatisk
)

fig.show()
