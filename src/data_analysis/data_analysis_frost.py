import pandas as pd
import sqlite3
from sklearn.impute import KNNImputer

# 1. Last inn data fra SQLite
db_file = 'data/clean/frost.db'
conn = sqlite3.connect(db_file)
df = pd.read_sql('SELECT * FROM weather_data', conn)

# 2. Konverter 'referenceTime' til datetime-format
df['referenceTime'] = pd.to_datetime(df['referenceTime'])

# 3. Definer årstider basert på måned
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
df['season'] = df['referenceTime'].dt.month.apply(get_season)

# Ekstraher år og lagre i en ny kolonne
df['year'] = df['referenceTime'].dt.year

# 4. Kolonnene for analyse (Temperatur, nedbør, vindhastighet)
columns_to_analyze = ['mean_air_temperature', 'total_precipitation', 'mean_wind_speed']

# 5. Bruk KNN-imputasjon for å håndtere manglende verdier
imputer = KNNImputer(n_neighbors=100)  # Velger 100 naboer for imputasjon
df[columns_to_analyze] = imputer.fit_transform(df[columns_to_analyze])

# 6. Beregn gjennomsnitt, median og standardavvik for hvert år og årstid
agg_stats = df.groupby(['year', 'season'])[columns_to_analyze].agg(['mean', 'median', 'std'])

# NYTT: Beregn statistikk per år (uavhengig av sesong)
agg_stats_by_year = df.groupby('year')[columns_to_analyze].agg(['mean', 'median', 'std'])


# 7. Beregn korrelasjonen mellom de relevante variablene
correlation_matrix = df[columns_to_analyze].corr()

# 8. Skriver ut resultatene
print("Statistikk for hvert år og årstid:")
print(agg_stats)

print("\nKorrelasjonsmatrise for temperatur, nedbør og vindhastighet:")
print(correlation_matrix)

# 9. Eksporter de aggregerte statistikkene og korrelasjonen til CSV-filer under data
agg_stats.to_csv('data/analyses_results/frost_aggregated_stats_year_season.csv')
correlation_matrix.to_csv('data/analyses_results/frost_correlation_matrix.csv')
agg_stats_by_year.to_csv('data/analyses_results/frost_aggregated_stats_year.csv')

