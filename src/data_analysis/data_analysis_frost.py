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
    try:
        # Definerer hvilke måneder som tilhører hver årstid
        seasons = {
            (12, 1, 2): 'Winter',
            (3, 4, 5): 'Spring',
            (6, 7, 8): 'Summer',
            (9, 10, 11): 'Fall'
        }
        # Finner riktig årstid for gitt måned
        return next(value for key, value in seasons.items() if month in key)
    except Exception as e:
        print(f"Feil ved bestemmelse av årstid for måned {month}: {e}")
        return 'Unknown'

def load_and_prepare_data(db_path: str) -> pd.DataFrame:
    """
    Leser inn og forbereder værdata fra en SQLite-database.

    Parametre:
        db_path (str): Filsti til SQLite-databasen
    Returnerer:
        pd.DataFrame: Klargjort DataFrame med ekstra kolonner for årstid og år
    """
    try:
        # Leser data fra SQLite-databasen
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql('SELECT * FROM weather_data', conn)
    except FileNotFoundError:
        print(f"Feil: Databasen '{db_path}' ble ikke funnet.")
        return pd.DataFrame()
    except sqlite3.Error as e:
        print(f"Feil ved tilkobling til SQLite-databasen: {e}")
        return pd.DataFrame()

    try:
        # Konverterer og legger til kolonner for årstid og år
        df['referenceTime'] = pd.to_datetime(df['referenceTime'])
        df['season'] = df['referenceTime'].dt.month.apply(get_season)
        df['year'] = df['referenceTime'].dt.year
    except KeyError as e:
        print(f"Feil: Mangler forventet kolonne i dataene: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Feil ved behandling av data fra databasen: {e}")
        return pd.DataFrame()

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
    try:
        # Beregner korrelasjonsmatrise
        data = df[columns].to_numpy()
        correlations = np.corrcoef(data.T)
        correlation_df = pd.DataFrame(correlations, columns=columns, index=columns)

        # Beregner statistikk per år og årstid
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
    except KeyError as e:
        print(f"Feil: En eller flere kolonner mangler i DataFrame: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    except Exception as e:
        print(f"Feil under beregning av statistikk: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

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
    try:
        # Oppretter katalog hvis den ikke finnes
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Lagrer resultater til CSV-filer
        stats_ys.to_csv(os.path.join(output_dir, 'frost_aggregated_stats_year_season.csv'))
        stats_y.to_csv(os.path.join(output_dir, 'frost_aggregated_stats_year.csv'))
        corr.to_csv(os.path.join(output_dir, 'frost_correlation_matrix.csv'))
    except Exception as e:
        print(f"Feil ved lagring av resultater: {e}")

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
    ]

    try:
        # Leser og forbereder data
        df = load_and_prepare_data(DB_FILE)
        if df.empty:
            print("Ingen data å analysere. Avslutter.")
            return

        # Utfører statistiske analyser
        year_season_stats, year_stats, correlations = calculate_statistics(
            df, COLUMNS_TO_ANALYZE
        )

        # Skriver ut statistikk per år
        print("\nStatistikk per år:")
        print(year_stats)

        # Lagrer analyseresultater
        save_results(year_season_stats, year_stats, correlations, OUTPUT_DIR)
        print("Analyseresultater lagret.")
    except Exception as e:
        print(f"En uventet feil oppstod i hovedfunksjonen: {e}")

if __name__ == "__main__":
    main()

