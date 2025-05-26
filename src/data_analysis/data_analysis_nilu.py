import pandas as pd
import numpy as np
import os

def get_season(month) -> str:
    """
    Returnerer navnet på årstiden basert på månedsnummer.
    Returnerer 'Unknown' hvis måneden er ugyldig.
    
    Parametre:
        month (int): Månedsnummer (1-12)
    Returnerer:
        str: Navn på årstid eller 'Unknown'
    """
    # Prøver å konvertere til int og sjekker at måneden er gyldig
    try:
        month = int(month)
        if not 1 <= month <= 12:
            return 'Unknown'
        # Definerer hvilke måneder som tilhører hver årstid
        seasons = {
            (12, 1, 2): 'Winter',
            (3, 4, 5): 'Spring',
            (6, 7, 8): 'Summer',
            (9, 10, 11): 'Fall'
        }
        # Finner riktig årstid for gitt måned
        return next((value for key, value in seasons.items() if month in key), 'Unknown')
    except (ValueError, TypeError):
        # Returnerer 'Unknown' hvis konvertering feiler
        return 'Unknown'

def load_and_prepare_data(file_path: str) -> pd.DataFrame:
    """
    Leser inn og forbereder luftkvalitetsdata fra en JSON-fil.
    
    Parametre:
        file_path (str): Filsti til JSON-filen
    Returnerer:
        pd.DataFrame: Klargjort DataFrame med ekstra kolonner for måned, årstid og år
    Kaster:
        ValueError: Hvis ingen gyldige data gjenstår etter prosessering
    """
    try:
        df = pd.read_json(file_path)  # Leser inn data fra JSON
        df['dateTime'] = pd.to_datetime(df['dateTime'])  # Konverterer til datetime
        df['month'] = df['dateTime'].dt.month  # Trekker ut måned
        df['season'] = df['month'].apply(get_season)  # Finner årstid
        df['year'] = df['dateTime'].dt.year  # Trekker ut år
        df = df[df['season'] != 'Unknown']  # Fjerner rader med ukjent årstid
        if df.empty:
            # Stopper hvis ingen gyldige data gjenstår
            raise ValueError("Ingen gyldige data igjen etter prosessering")
        return df
    except Exception as e:
        # Skriver ut feilmelding hvis noe går galt
        print(f"Feil ved lasting av data: {str(e)}")
        raise

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
    stats_ys.to_csv(os.path.join(output_dir, 'nilu_aggregated_stats_year_season.csv'))
    # Lagrer statistikk per år
    stats_y.to_csv(os.path.join(output_dir, 'nilu_aggregated_stats_year.csv'))
    # Lagrer korrelasjonsmatrise
    corr.to_csv(os.path.join(output_dir, 'nilu_correlation_matrix.csv'))

def main():
    """
    Hovedfunksjon som kjører analyse-pipelinen:
    - Leser inn data
    - Utfører statistiske analyser
    - Skriver ut og lagrer resultater
    """
    DATA_FILE = 'data/clean/cleaned_data_nilu.json'  # Filsti til NILU-data
    OUTPUT_DIR = 'data/analyses_results'  # Katalog for lagring av resultater
    COLUMNS_TO_ANALYZE = ['NO2', 'PM10', 'PM2.5']  # Kolonner som skal analyseres
    df = load_and_prepare_data(DATA_FILE)  # Leser og forbereder data
    year_season_stats, year_stats, correlations = calculate_statistics(
        df, COLUMNS_TO_ANALYZE
    )  # Beregner statistikk og korrelasjon
    print("\nStatistikk per år:")
    print(year_stats)  # Skriver ut statistikk per år
    save_results(year_season_stats, year_stats, correlations, OUTPUT_DIR)  # Lagrer resultater

if __name__ == "__main__":
    main()
