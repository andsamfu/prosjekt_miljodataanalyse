import pandas as pd
from datetime import timedelta

class MissingValueValidator:
    def validate(self, df: pd.DataFrame) -> dict:
        missing_values = {}
        for column in df.columns:
            missing = df[column].isnull().sum()
            if missing > 0:
                missing_values[column] = missing
        return missing_values

class ValueRangeValidator:
    def __init__(self, valid_ranges: dict):
        self.valid_ranges = valid_ranges
    
    def validate(self, df: pd.DataFrame) -> dict:
        out_of_range = {}
        for column, (min_val, max_val) in self.valid_ranges.items():
            if column in df.columns:
                mask = ~df[column].between(min_val, max_val)
                invalid = df[mask][column]
                if len(invalid) > 0:
                    out_of_range[column] = invalid
        return out_of_range

class DateContinuityValidator:
    def validate(self, df: pd.DataFrame, date_column='referenceTime') -> list:
        df = df.sort_values(date_column)
        dates = pd.to_datetime(df[date_column])
        date_gaps = []
        
        if len(dates) < 2:
            return date_gaps
            
        # Create complete date range
        date_range = pd.date_range(start=dates.iloc[0], end=dates.iloc[-1], freq='D')
        
        # Find missing dates
        missing_dates = set(date_range) - set(dates)
        
        # Group consecutive missing dates into gaps
        if missing_dates:
            missing_dates = sorted(list(missing_dates))
            gap_start = missing_dates[0]
            prev_date = gap_start
            
            for date in missing_dates[1:] + [missing_dates[-1] + pd.Timedelta(days=1)]:
                if date - prev_date > timedelta(days=1):
                    date_gaps.append((gap_start, prev_date))
                    gap_start = date
                prev_date = date
            date_gaps.append((gap_start, prev_date))
            
        return date_gaps
