import pandas as pd
import json
import plotly.graph_objects as go
import plotly.offline as pyo

# Les JSON-data fra fil
with open('data/raw/download_ssb_climate_gasses.json', 'r') as f:
    data = json.load(f)

# Hent dimensjonsinformasjon
dimensions = data['dataset']['dimension']

# Hent kategorier og verdier
categories = dimensions['UtslpTilLuft']['category']['label']
values = data['dataset']['value']
years = [str(year) for year in dimensions['Tid']['category']['index'].keys()]

# Opprett en DataFrame for dataene
emission_data = {}
for i, category_index in enumerate(dimensions['UtslpTilLuft']['category']['index']):
    category_label = categories[str(category_index)]
    category_values = values[i * len(years):(i + 1) * len(years)]
    emission_data[category_label] = category_values

df = pd.DataFrame(emission_data, index=years)

# Fjern "Alle kilder" fra diagrammet
df = df.drop('Alle kilder', axis=1)

# Lag en liste med farger for kategoriene (bruker Plotly fargepaletter)
colors = [
    'rgb(56, 114, 178)',  # Blå
    'rgb(232, 89, 86)',   # Rød
    'rgb(118, 179, 97)',  # Grønn
    'rgb(249, 199, 73)',  # Gul
    'rgb(126, 110, 175)', # Lilla
    'rgb(255, 159, 28)',  # Oransje
    'rgb(106, 179, 211)'  # Lyseblå
]

# Lag stablet stolpediagram med plotly
fig = go.Figure()

for i, column in enumerate(df.columns):
    fig.add_trace(go.Bar(
        x=df.index,
        y=df[column],
        name=column,
        marker=dict(color=colors[i % len(colors)]),
        visible=True  # Alle spor er synlige som standard
    ))

# Oppdater layout for interaktivitet og design
fig.update_layout(
    barmode='stack',
    title=dict(
        text='CO2-utslipp etter kilde i Norge (diagram)',
        x=0.5,
        y=0.98,
        xanchor='center',
        yanchor='top',
        font=dict(size=24, color='rgb(33, 33, 33)')
    ),
    xaxis_title='År',
    yaxis_title='Utslipp (1000 tonn CO2-ekvivalenter)',
    xaxis=dict(
        tickangle=-90,
        tickmode='linear',
        tickfont=dict(size=12, color='rgb(75, 75, 75)'),
        showgrid=False
    ),
    yaxis=dict(
        title_font=dict(size=14),
        tickfont=dict(size=12, color='rgb(75, 75, 75)'),
        showgrid=True,
        gridcolor='rgb(240, 240, 240)',
    ),
    
    updatemenus=[
        dict(
            type='buttons',
            direction='left',
            buttons=list([
                dict(
                    args=["type", "bar"],
                    label="Stablet",
                    method="restyle"
                ),
                dict(
                    args=["type", "relative"],
                    label="Graf",
                    method="restyle"
                )
            ]),
            showactive=True,
            x=0.65,
            xanchor="center",
            y=1.03,
            yanchor="bottom",
            pad=dict(t=10)
        )
    ],
   
    plot_bgcolor='rgb(255, 255, 255)',
    margin=dict(l=50, r=200, t=100, b=100)
)

fig.show()