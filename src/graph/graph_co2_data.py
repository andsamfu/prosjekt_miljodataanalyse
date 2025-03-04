import pandas as pd
import plotly.graph_objects as go

# 1. Les CSV-filen inn i en Pandas DataFrame
df = pd.read_csv('data/raw/raw_download_globalcarbonatlas_co2_world_1960_to_2023.csv')

# 2. Hent landene fra kolonnene
countries = df.columns[1:]

# 3. Hent årene fra den første kolonnen
years = df.iloc[:, 0].tolist()

# 4. Lag en liste for å lagre alle punktene
data = []

# 5. Iterer gjennom landene og legg til punkter for hvert år
for country in countries:
    emissions = df[country].tolist()
    data.append(go.Scatter(x=years, y=emissions, mode='markers', name=country))

# 6. Lag grafen
fig = go.Figure(data=data)

# 7. Legg til tittel og aksetitler
fig.update_layout(title='CO2-utslipp per land', xaxis_title='År', yaxis_title='CO2-utslipp')

# 8. Vis grafen
fig.show()