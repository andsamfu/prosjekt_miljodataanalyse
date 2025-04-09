import pandas as pd

# 1. Last inn datasettet
filsti = "data/clean/cleaned_data_nilu.json"
df = pd.read_json(filsti)

# 2. Konverter 'dateTime' til datetime-format og ekstrakt år
df['dateTime'] = pd.to_datetime(df['dateTime'])
df['year'] = df['dateTime'].dt.year

# 3. kolonnene for analyse
columns_to_analyze = ['NO2', 'PM10', 'PM2.5']

# 4. Håndtere manglende verdier (erstatte med median for hver kolonne)
df[columns_to_analyze] = df[columns_to_analyze].fillna(df[columns_to_analyze].median())

# 5. Beregn gjennomsnitt, median og standardavvik for hvert år
agg_stats = df.groupby('year')[columns_to_analyze].agg(['mean', 'median', 'std'])

# 6. Beregn korrelasjonen mellom de relevante variablene
correlation_matrix = df[columns_to_analyze].corr()

# 7. Skriver ut resultatene
print("Statistikk for hvert år:")
print(agg_stats)

print("\nKorrelasjonsmatrise for NO2, PM10, og PM2.5:")
print(correlation_matrix)

# 8. Eksporter de aggregerte statistikkene og korrelasjonen til CSV-filer under data
agg_stats.to_csv("data/analyses_results/nilu_aggregated_stats_yearly.csv")
correlation_matrix.to_csv("data/analyses_results/nilu_correlation_matrix.csv")
