import pandas as pd
import numpy as np
from datetime import timedelta
from sklearn.impute import KNNImputer

class MissingValueValidator:
    def validate(self, df: pd.DataFrame) -> tuple[dict, pd.DataFrame]:
        missing_values = {}
        df_cleaned = df.copy()
        
        for column in df.columns:
            if column != 'referenceTime':
                missing = df[df[column].isnull()]
                if len(missing) > 0:
                    missing_values[column] = missing
                    # Already NaN, no need to modify
        
        return missing_values, df_cleaned
    
    def report(self, results: dict):
        if results:
            print("\nMissing values detected:")
            for column, missing_df in results.items():
                print(f"{column}:")
                # Convert to datetime if not already datetime
                dates = pd.to_datetime(missing_df['referenceTime'])
                yearly_counts = dates.dt.year.value_counts().sort_index()
                for year, count in yearly_counts.items():
                    print(f"- {year}: {count}")
        else:
            print("\nNo missing values detected")

class OutlierValidator:
    def __init__(self, valid_ranges: dict):
        self.valid_ranges = valid_ranges
    
    def validate(self, df: pd.DataFrame) -> tuple[dict, pd.DataFrame]:
        outliers = {}
        df_cleaned = df.copy()
        
        for column, (min_val, max_val) in self.valid_ranges.items():
            if column in df.columns:
                # Only check non-null values for outliers
                valid_data = df[~df[column].isnull()]
                mask = ~valid_data[column].between(min_val, max_val)
                invalid = valid_data[mask][column]
                if len(invalid) > 0:
                    outliers[column] = pd.Series(
                        invalid.values,
                        index=pd.to_datetime(valid_data[mask]['referenceTime'])
                    )
                    # Convert outliers to NaN
                    df_cleaned.loc[df_cleaned[column].notna() & ~df_cleaned[column].between(min_val, max_val), column] = np.nan
        
        return outliers, df_cleaned

    def report(self, results: dict):
        if results:
            print("\nOutliers detected:")
            for column, values in results.items():
                print(f"{column}:")
                yearly_counts = values.groupby(values.index.year).size()
                for year, count in sorted(yearly_counts.items()):
                    print(f"- {year}: {count}")
        else:
            print("\nNo outliers detected")

class DateContinuityValidator:
    def validate(self, df: pd.DataFrame, date_column='referenceTime') -> tuple[list, pd.DataFrame]:
        df = df.sort_values(date_column)
        # Convert to datetime first, then to date string
        dates = pd.to_datetime(df[date_column]).dt.strftime('%Y-%m-%d')
        date_gaps = []
        
        if len(dates) < 2:
            return date_gaps, df
            
        # Create complete date range
        start_date = pd.to_datetime(dates.iloc[0])
        end_date = pd.to_datetime(dates.iloc[-1])
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        date_range = date_range.strftime('%Y-%m-%d')
        
        # Find missing dates
        missing_dates = sorted(list(set(date_range) - set(dates)))
        
        # Create DataFrame with all dates
        df_cleaned = df.copy()
        df_cleaned[date_column] = dates  # Use consistent date format
        df_cleaned = df_cleaned.set_index(date_column)
        df_cleaned = df_cleaned.reindex(date_range)
        df_cleaned.index.name = date_column
        df_cleaned = df_cleaned.reset_index()
        
        return missing_dates, df_cleaned

    def report(self, results: list):
        if not results:
            print("\nNo date gaps detected")
            return

        print("\nDate gaps detected:")
        gaps_by_year = {}
        for date in results:
            year = pd.to_datetime(date).year
            gaps_by_year[year] = gaps_by_year.get(year, 0) + 1
        
        for year, count in sorted(gaps_by_year.items()):
            print(f"- {year}: {count}")

class ImputationValidator:
    def __init__(self, n_neighbors=5):
        self.n_neighbors = n_neighbors
    
    def validate(self, df: pd.DataFrame) -> tuple[dict, pd.DataFrame]:
        df_cleaned = df.copy()
        imputation_info = {}
        
        # Store original NaN state before imputation
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for column in numeric_columns:
            tracking_column = f'generated_{column}'
            df_cleaned[tracking_column] = df[column].isna()
            imputation_info[column] = df_cleaned[tracking_column].sum()
        
        # Perform KNN imputation on numeric columns
        if len(numeric_columns) > 0:
            imputer = KNNImputer(n_neighbors=self.n_neighbors)
            df_cleaned[numeric_columns] = imputer.fit_transform(df_cleaned[numeric_columns])
            # Round numeric values to 1 decimal
            df_cleaned[numeric_columns] = df_cleaned[numeric_columns].round(1)
        
        return imputation_info, df_cleaned
    
    def report(self, results: dict):
        if not any(count > 0 for count in results.values()):
            print("\nNo values generated")
            return
        
        print("\nGenerated values:")
        for column, count in results.items():
            if count > 0:
                print(f"- {column}: {count}")
