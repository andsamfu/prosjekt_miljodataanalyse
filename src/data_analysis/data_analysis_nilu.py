import pandas as pd
import sqlite3
import os
from sklearn.impute import KNNImputer

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


# 5. Beregn gjennomsnitt, median og standardavvik for hvert år og årstid
agg_stats_by_year_season = df.groupby(['year', 'season'])[columns_to_analyze].agg(['mean', 'median', 'std'])

# 6. Beregn gjennomsnitt, median og standardavvik for hvert år (uten å ta hensyn til sesongene)
agg_stats_by_year = df.groupby(['year'])[columns_to_analyze].agg(['mean', 'median', 'std'])

# 7. Beregn korrelasjonen mellom de relevante variablene
correlation_matrix = df[columns_to_analyze].corr()

# 8. Skriver ut resultatene
print("Statistikk for hvert år og årstid:")
print(agg_stats_by_year_season)

print("\nStatistikk for hvert år:")
print(agg_stats_by_year)

print("\nKorrelasjonsmatrise for NO2, PM10, og PM2.5:")
print(correlation_matrix)

# 9. Eksporter de aggregerte statistikkene og korrelasjonen til CSV-filer under data
output_directory = "data/analyses_results"
# Sjekk om mappen eksisterer, hvis ikke, opprett den
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

agg_stats_by_year_season.to_csv(f"{output_directory}/nilu_aggregated_stats_year_season.csv")
agg_stats_by_year.to_csv(f"{output_directory}/nilu_aggregated_stats_year.csv")  # Ny CSV for kun år
correlation_matrix.to_csv(f"{output_directory}/nilu_correlation_matrix.csv")
