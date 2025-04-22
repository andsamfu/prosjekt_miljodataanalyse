import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Last inn data
filsti = "data/clean/cleaned_data_nilu.json"
df = pd.read_json(filsti)

# Dato og tid
df['dateTime'] = pd.to_datetime(df['dateTime'])
df['year'] = df['dateTime'].dt.year
df['month'] = df['dateTime'].dt.month

# Lag sesongkolonne
def get_season(month):
    if month in [3, 4, 5]:
        return 'Vår'
    elif month in [6, 7, 8]:
        return 'Sommer'
    elif month in [9, 10, 11]:
        return 'Høst'
    else:
        return 'Vinter'

df['season'] = df['month'].apply(get_season)

# Kolonner
columns_to_analyze = ['NO2', 'PM10', 'PM2.5']
df[columns_to_analyze] = df[columns_to_analyze].fillna(df[columns_to_analyze].median())

# --- 1. Gjennomsnitt per sesong og år ---
seasonal_avg = df.groupby(['year', 'season'])[columns_to_analyze].mean().reset_index()
seasonal_avg = pd.melt(seasonal_avg, id_vars=['year', 'season'], value_vars=columns_to_analyze)

fig_avg = px.line(seasonal_avg,
                  x='year', y='value', color='season', facet_col='variable',
                  category_orders={"season": ['Vinter', 'Vår', 'Sommer', 'Høst']},
                  title="Gjennomsnittlig luftkvalitet per sesong og år",
                  labels={'value': 'µg/m³', 'season': '', 'year': 'År', 'variable': 'Stoff'})

fig_avg.update_layout(height=600, template='plotly_dark')
fig_avg.show()

# --- 2. Median per sesong og år ---
seasonal_median = df.groupby(['year', 'season'])[columns_to_analyze].median().reset_index()
seasonal_median = pd.melt(seasonal_median, id_vars=['year', 'season'], value_vars=columns_to_analyze)

fig_median = px.line(seasonal_median,
                     x='year', y='value', color='season', facet_col='variable',
                     category_orders={"season": ['Vinter', 'Vår', 'Sommer', 'Høst']},
                     title="Median luftkvalitet per sesong og år",
                     labels={'value': 'µg/m³', 'season': '', 'year': 'År', 'variable': 'Stoff'})

fig_median.update_layout(height=600, template='plotly_dark')
fig_median.show()

# --- 3. Fordeling (Histogram) ---
for col in columns_to_analyze:
    fig_hist = px.histogram(df, x=col, nbins=60, marginal='violin', color='season',
                            title=f"Fordeling av {col} etter sesong")
    fig_hist.show()

# --- 4. Heatmap for månedlig NO2 ---
monthly_avg = df.groupby(['year', 'month'])['NO2'].mean().unstack()
fig_heatmap = px.imshow(monthly_avg,
                        labels=dict(x="Måned", y="År", color="NO2 (µg/m³)"),
                        title="Månedlig gjennomsnitt NO2",
                        color_continuous_scale='Viridis')
fig_heatmap.update_layout(yaxis_autorange="reversed")
fig_heatmap.show()

# --- 5. Korrelasjonsmatrise ---
corr = df[columns_to_analyze].corr()
fig_corr = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r",
                     title="Korrelasjon mellom luftforurensningskomponenter")
fig_corr.update_layout(template="plotly_dark")
fig_corr.show()

# --- 6. Total forurensning per sesong og år ---
df['total_pollution'] = df[columns_to_analyze].sum(axis=1)
seasonal_total = df.groupby(['year', 'season'])['total_pollution'].mean().reset_index()

fig_total = px.bar(seasonal_total, x='year', y='total_pollution', color='season',
                   barmode='group',
                   title='Total luftforurensning per år og sesong',
                   labels={'total_pollution': 'Total µg/m³', 'season': '', 'year': 'År'})
fig_total.show()
