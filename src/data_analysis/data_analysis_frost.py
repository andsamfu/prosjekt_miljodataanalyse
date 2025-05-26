import pandas as pd
import numpy as np
import sqlite3
import os

def get_season(month: int) -> str:
    """
    Returnerer navnet på årstiden basert på månedsnummer.
    Returnerer 'Unknown' hvis måneden er ugyldig.

    Parametre:
        month (int): Månedsnummer (1-12)
    Returnerer:
        str: Navn på årstid eller 'Unknown'
    """
    # Definerer hvilke måneder som tilhører hver årstid
    seasons = {
        (12, 1, 2): 'Winter',
        (3, 4, 5): 'Spring',
        (6, 7, 8): 'Summer',
        (9, 10, 11): 'Fall'
    }
    # Finner riktig årstid for gitt måned
    return next(value for key, value in seasons.items() if month in key)

def load_and_prepare_data(db_path: str) -> pd.DataFrame:
    """
    Leser inn og forbereder værdata fra en SQLite-database.

    Parametre:
        db_path (str): Filsti til SQLite-databasen
    Returnerer:
        pd.DataFrame: Klargjort DataFrame med ekstra kolonner for årstid og år
    """
    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql('SELECT * FROM weather_data', conn)  # Leser inn data fra databasen

    df['referenceTime'] = pd.to_datetime(df['referenceTime'])  # Konverterer til datetime
    df['season'] = df['referenceTime'].dt.month.apply(get_season)  # Finner årstid
    df['year'] = df['referenceTime'].dt.year  # Trekker ut år

    return df

def calculate_statistics(df: pd.DataFrame, columns: list) -> tuple:
    """
    Beregner statistikk ved bruk av NumPy-operasjoner.

    Parametre:
        df (pd.DataFrame): Inndata-DataFrame
        columns (list): Kolonner som skal analyseres
    Returnerer:
        tuple: (statistikk per år og årstid, statistikk per år, korrelasjonsmatrise)
    """
    # Konverterer utvalgte kolonner til numpy-array for effektiv beregning
    data = df[columns].to_numpy()
    # Beregner korrelasjonsmatrise mellom variablene
    correlations = np.corrcoef(data.T)
    correlation_df = pd.DataFrame(correlations, columns=columns, index=columns)
    # Beregner statistikk (gjennomsnitt, median, std) per år og årstid
    year_season_stats = df.groupby(['year', 'season'])[columns].agg([
        ('mean', np.mean),
        ('median', np.median),
        ('std', np.std)
    ])
    # Beregner statistikk per år
    year_stats = df.groupby('year')[columns].agg([
        ('mean', np.mean),
        ('median', np.median),
        ('std', np.std)
    ])
    return year_season_stats, year_stats, correlation_df

def save_results(stats_ys: pd.DataFrame, stats_y: pd.DataFrame, 
                corr: pd.DataFrame, output_dir: str):
    """
    Lagrer analyseresultater til CSV-filer.

    Parametre:
        stats_ys (pd.DataFrame): Statistikk per år og årstid
        stats_y (pd.DataFrame): Statistikk per år
        corr (pd.DataFrame): Korrelasjonsmatrise
        output_dir (str): Katalog for lagring av resultater
    """
    # Oppretter katalogen hvis den ikke finnes
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Lagrer statistikk per år og årstid
    stats_ys.to_csv(os.path.join(output_dir, 'frost_aggregated_stats_year_season.csv'))
    # Lagrer statistikk per år
    stats_y.to_csv(os.path.join(output_dir, 'frost_aggregated_stats_year.csv'))
    # Lagrer korrelasjonsmatrise
    corr.to_csv(os.path.join(output_dir, 'frost_correlation_matrix.csv'))

def main():
    """
    Hovedfunksjon som kjører analyse-pipelinen:
    - Leser inn data
    - Utfører statistiske analyser
    - Skriver ut og lagrer resultater
    """
    DB_FILE = 'data/clean/cleaned_data_frost.db'  # Filsti til frost-database
    OUTPUT_DIR = 'data/analyses_results'  # Katalog for lagring av resultater
    COLUMNS_TO_ANALYZE = [
        'mean_air_temperature',
        'total_precipitation',
        'mean_wind_speed'
    ]  # Kolonner som skal analyseres

    # Leser og forbereder data
    df = load_and_prepare_data(DB_FILE)
    # Beregner statistikk og korrelasjon
    year_season_stats, year_stats, correlations = calculate_statistics(
        df, COLUMNS_TO_ANALYZE
    )
    # Skriver ut statistikk per år
    print("\nStatistikk per år:")
    print(year_stats)
    # Lagrer resultater
    save_results(year_season_stats, year_stats, correlations, OUTPUT_DIR)

if __name__ == "__main__":
    main()

