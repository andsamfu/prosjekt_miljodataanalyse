import pandas as pd
import numpy as np
from datetime import timedelta
from sklearn.impute import KNNImputer

# Juster Pandas' utskriftsinnstillinger
pd.set_option('display.max_columns', None)  # Vis alle kolonner
pd.set_option('display.width', 1000)       # Øk bredden på utskriften

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
        if not results:
            print("\nIngen manglende verdier oppdaget")
            return

        print("\nManglende verdier oppdaget:")
        
        all_data = []
        for attribute, missing_df in results.items():
            if not missing_df.empty and 'referenceTime' in missing_df.columns:
                # Ensure 'referenceTime' is in datetime format
                dates = pd.to_datetime(missing_df['referenceTime'])
                yearly_counts = dates.dt.year.value_counts()
                for year, count in yearly_counts.items():
                    all_data.append({'Attribute': attribute, 'Year': year, 'Count': count})
            elif not missing_df.empty:
                print(f"Advarsel: 'referenceTime'-kolonnen mangler for attributt '{attribute}' i missing_df.")

        if not all_data:
            # This case might occur if results is not empty, but all missing_df are empty or lack 'referenceTime'
            print("Ingen tellbare manglende verdier funnet med 'referenceTime'.")
            return

        report_df = pd.DataFrame(all_data)
        
        # Pivot to get Attributes as rows, Years as columns, and Count as values
        pivot_df = report_df.pivot_table(index='Attribute', columns='Year', values='Count', fill_value=0)
        
        # Ensure years are sorted in columns
        if not pivot_df.empty:
            pivot_df = pivot_df.sort_index(axis=1)
            
            # Convert counts to integer and replace 0 with "ok"
            for year_col in pivot_df.columns:
                pivot_df[year_col] = pivot_df[year_col].apply(lambda x: "ok" if int(x) == 0 else int(x))
        
        print(pivot_df)

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
        if not results:
            print("\nIngen outliers oppdaget")
            return

        print("\nOutliers oppdaget:")
        
        all_data = []
        for attribute, series_of_outliers in results.items():
            if not series_of_outliers.empty:
                # The index of the series is already datetime-like from the validate method
                yearly_counts = series_of_outliers.groupby(series_of_outliers.index.year).size()
                for year, count in yearly_counts.items():
                    all_data.append({'Attribute': attribute, 'Year': year, 'Count': count})
            # It's possible an attribute in results might have an empty series if all values were valid
            # or became NaN for other reasons before outlier check for that specific attribute.

        if not all_data:
            print("Ingen tellbare outliers funnet med årsdata.")
            return

        report_df = pd.DataFrame(all_data)
        
        # Pivot to get Attributes as rows, Years as columns, and Count as values
        pivot_df = report_df.pivot_table(index='Attribute', columns='Year', values='Count', fill_value=0)
        
        # Ensure years are sorted in columns and format output
        if not pivot_df.empty:
            pivot_df = pivot_df.sort_index(axis=1)
            for year_col in pivot_df.columns:
                pivot_df[year_col] = pivot_df[year_col].apply(lambda x: "ok" if int(x) == 0 else int(x))
        
        print(pivot_df)

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
            results (list): Liste over manglende datoer (som strenger).
        """
        if not results:
            print("\nIngen datohull oppdaget")
            return

        print("\nDatohull oppdaget:")
        
        gaps_by_year = {}
        for date_str in results:
            try:
                year = pd.to_datetime(date_str).year
                gaps_by_year[year] = gaps_by_year.get(year, 0) + 1
            except ValueError:
                print(f"Advarsel: Kunne ikke parse dato '{date_str}'")
                continue

        if not gaps_by_year:
            print("Ingen gyldige årsdata for datohull funnet.")
            return

        # Konverter til DataFrame med år som kolonner
        # Lag en liste av dictionaries for DataFrame-konstruksjon, der hver dict er en rad
        # Her vil vi ha en enkelt rad DataFrame der kolonnene er år.
        report_df = pd.DataFrame([gaps_by_year])
        
        if report_df.empty:
            # Dette burde ikke skje hvis gaps_by_year ikke er tomt, men som en sikkerhet
            print("Kunne ikke generere rapport for datohull.")
            return

        # Gi indeksen et meningsfylt navn
        report_df.index = ["Antall"]
        
        # Sorter kolonner (år) og formater verdier
        report_df = report_df.sort_index(axis=1)
        for year_col in report_df.columns:
            report_df[year_col] = report_df[year_col].apply(lambda x: "ok" if int(x) == 0 else int(x))
        
        print(report_df)

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
