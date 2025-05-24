import pandas as pd
import numpy as np
from datetime import timedelta
from sklearn.impute import KNNImputer

class MissingValueValidator:
    """
    Klasse for å validere og håndtere manglende verdier i en DataFrame.
    """
    def validate(self, df: pd.DataFrame) -> tuple[dict, pd.DataFrame]:
        """
        Identifiserer manglende verdier i DataFrame og returnerer en kopi av DataFrame.

        Args:
            df (pd.DataFrame): DataFrame som skal valideres.

        Returns:
            tuple[dict, pd.DataFrame]: Ordbok med kolonner og deres manglende verdier, og en kopi av DataFrame.
        """
        missing_values = {}
        df_cleaned = df.copy()
        
        for column in df.columns:
            if column != 'referenceTime':  # Ignorerer tidskolonnen
                missing = df[df[column].isnull()]
                if len(missing) > 0:
                    missing_values[column] = missing
        
        return missing_values, df_cleaned
    
    def report(self, results: dict):
        """
        Genererer en rapport over manglende verdier.

        Args:
            results (dict): Ordbok med kolonner og deres manglende verdier.
        """
        if results:
            print("\nManglende verdier oppdaget:")
            for column, missing_df in results.items():
                print(f"{column}:")
                dates = pd.to_datetime(missing_df['referenceTime'])
                yearly_counts = dates.dt.year.value_counts().sort_index()
                for year, count in yearly_counts.items():
                    print(f"- {year}: {count}")
        else:
            print("\nIngen manglende verdier oppdaget")

class OutlierValidator:
    """
    Klasse for å validere og håndtere uteliggere i en DataFrame.
    """
    def __init__(self, valid_ranges: dict):
        """
        Initialiserer validatoren med gyldige verdier for hver kolonne.

        Args:
            valid_ranges (dict): Ordbok med kolonner og deres gyldige verdier (min, maks).
        """
        self.valid_ranges = valid_ranges
    
    def validate(self, df: pd.DataFrame) -> tuple[dict, pd.DataFrame]:
        """
        Identifiserer uteliggere i DataFrame og returnerer en kopi med uteliggere satt til NaN.

        Args:
            df (pd.DataFrame): DataFrame som skal valideres.

        Returns:
            tuple[dict, pd.DataFrame]: Ordbok med uteliggere og en kopi av DataFrame.
        """
        outliers = {}
        df_cleaned = df.copy()
        
        for column, (min_val, max_val) in self.valid_ranges.items():
            if column in df.columns:
                valid_data = df[~df[column].isnull()]
                mask = ~valid_data[column].between(min_val, max_val)
                invalid = valid_data[mask][column]
                if len(invalid) > 0:
                    outliers[column] = pd.Series(
                        invalid.values,
                        index=pd.to_datetime(valid_data[mask]['referenceTime'])
                    )
                    df_cleaned.loc[df_cleaned[column].notna() & ~df_cleaned[column].between(min_val, max_val), column] = np.nan
        
        return outliers, df_cleaned

    def report(self, results: dict):
        """
        Genererer en rapport over outliers.

        Args:
            results (dict): Ordbok med outliers.
        """
        if results:
            print("\nOutliers oppdaget:")
            for column, values in results.items():
                print(f"{column}:")
                yearly_counts = values.groupby(values.index.year).size()
                for year, count in sorted(yearly_counts.items()):
                    print(f"- {year}: {count}")
        else:
            print("\nIngen outliers oppdaget")

class DateContinuityValidator:
    """
    Klasse for å validere og håndtere datokontinuitet i en DataFrame.
    """
    def validate(self, df: pd.DataFrame, date_column='referenceTime') -> tuple[list, pd.DataFrame]:
        """
        Identifiserer manglende datoer og returnerer en DataFrame med kontinuerlige datoer.

        Args:
            df (pd.DataFrame): DataFrame som skal valideres.
            date_column (str): Kolonnenavn for datoer.

        Returns:
            tuple[list, pd.DataFrame]: Liste over manglende datoer og en DataFrame med kontinuerlige datoer.
        """
        df = df.sort_values(date_column)
        dates = pd.to_datetime(df[date_column]).dt.strftime('%Y-%m-%d')
        date_gaps = []
        
        if len(dates) < 2:
            return date_gaps, df
            
        start_date = pd.to_datetime(dates.iloc[0])
        end_date = pd.to_datetime(dates.iloc[-1])
        date_range = pd.date_range(start=start_date, end=end_date, freq='D').strftime('%Y-%m-%d')
        missing_dates = sorted(list(set(date_range) - set(dates)))
        
        df_cleaned = df.copy()
        df_cleaned[date_column] = dates
        df_cleaned = df_cleaned.set_index(date_column).reindex(date_range).reset_index()
        df_cleaned.rename(columns={'index': date_column}, inplace=True)
        
        return missing_dates, df_cleaned

    def report(self, results: list):
        """
        Genererer en rapport over manglende datoer.

        Args:
            results (list): Liste over manglende datoer.
        """
        if not results:
            print("\nIngen datohull oppdaget")
            return

        print("\nDatohull oppdaget:")
        gaps_by_year = {}
        for date in results:
            year = pd.to_datetime(date).year
            gaps_by_year[year] = gaps_by_year.get(year, 0) + 1
        
        for year, count in sorted(gaps_by_year.items()):
            print(f"- {year}: {count}")

class ImputationValidator:
    """
    Klasse for å implantere manglende verdier i en DataFrame.
    """
    def __init__(self, n_neighbors=5):
        """
        Initialiserer validatoren med antall naboer for KNN-imputasjon.

        Args:
            n_neighbors (int): Antall naboer for KNN-imputasjon.
        """
        self.n_neighbors = n_neighbors
    
    def validate(self, df: pd.DataFrame) -> tuple[dict, pd.DataFrame]:
        """
        Imputerer manglende verdier i DataFrame.

        Args:
            df (pd.DataFrame): DataFrame som skal valideres.

        Returns:
            tuple[dict, pd.DataFrame]: Ordbok med antall imputasjoner og en kopi av DataFrame.
        """
        df_cleaned = df.copy()
        imputation_info = {}
        
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for column in numeric_columns:
            tracking_column = f'generated_{column}'
            df_cleaned[tracking_column] = df[column].isna()
            imputation_info[column] = df_cleaned[tracking_column].sum()
        
        dates = pd.to_datetime(df_cleaned['referenceTime'])
        df_cleaned['day_of_year'] = dates.dt.dayofyear
        
        for column in numeric_columns:
            seasonal_avg = df_cleaned.groupby('day_of_year')[column].transform('mean')
            mask = df_cleaned[column].isna()
            df_cleaned.loc[mask, column] = seasonal_avg[mask]
            
            still_missing = df_cleaned[column].isna()
            if still_missing.any():
                imputer = KNNImputer(n_neighbors=self.n_neighbors)
                imputation_data = df_cleaned[['day_of_year', column]].copy()
                imputation_data[column] = imputation_data[column].fillna(0)
                imputed_values = imputer.fit_transform(imputation_data)
                df_cleaned.loc[still_missing, column] = imputed_values[still_missing, 1]
        
        df_cleaned = df_cleaned.drop(['day_of_year'], axis=1)
        df_cleaned[numeric_columns] = df_cleaned[numeric_columns].round(1)
        
        return imputation_info, df_cleaned
    
    def report(self, results: dict):
        """
        Genererer en rapport over imputasjoner.

        Args:
            results (dict): Ordbok med antall imputasjoner per kolonne.
        """
        if not any(count > 0 for count in results.values()):
            print("\nIngen verdier generert")
            return
        
        print("\nGenererte verdier:")
        for column, count in results.items():
            if count > 0:
                print(f"- {column}: {count}")
