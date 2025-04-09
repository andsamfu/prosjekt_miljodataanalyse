import pandas as pd

# 1. Last inn datasettet
filsti = "data/clean/cleaned_data_nilu.json"
df = pd.read_json(filsti)

# 2. Konverter 'dateTime' til datetime-format
df['dateTime'] = pd.to_datetime(df['dateTime'])

# Definer årstider basert på måned
def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'

# Lag en ny kolonne som angir årstiden for hver rad
df['season'] = df['dateTime'].dt.month.apply(get_season)

# Ekstraher år og lagre i en ny kolonne
df['year'] = df['dateTime'].dt.year

# 3. Kolonnene for analyse
columns_to_analyze = ['NO2', 'PM10', 'PM2.5']

# 4. Håndtere manglende verdier (erstatte med median for hver kolonne)
df[columns_to_analyze] = df[columns_to_analyze].fillna(df[columns_to_analyze].median())

# 5. Beregn gjennomsnitt, median og standardavvik for hvert år og årstid
agg_stats = df.groupby(['year', 'season'])[columns_to_analyze].agg(['mean', 'median', 'std'])

# 6. Beregn korrelasjonen mellom de relevante variablene (kan også utvides til å inkludere år og årstid)
correlation_matrix = df[columns_to_analyze].corr()

# 7. Skriver ut resultatene
print("Statistikk for hvert år og årstid:")
print(agg_stats)

print("\nKorrelasjonsmatrise for NO2, PM10, og PM2.5:")
print(correlation_matrix)

# 8. Eksporter de aggregerte statistikkene og korrelasjonen til CSV-filer under data
agg_stats.to_csv("data/analyses_results/nilu_aggregated_stats_year_season.csv")
correlation_matrix.to_csv("data/analyses_results/nilu_correlation_matrix.csv")
