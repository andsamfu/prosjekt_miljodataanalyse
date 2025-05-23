import unittest
import pandas as pd
import numpy as np
import sys
import os
import json

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.data_cleaning.data_validators import MissingValueValidator, OutlierValidator, DateContinuityValidator, ImputationValidator

# Load mock data from JSON file
with open(os.path.join(os.path.dirname(__file__), 'mock_weather_data.json'), 'r') as f:
    MOCK_DATA = json.load(f)

def get_test_case(category, test_name):
    """Helper function to get test cases from the new nested structure"""
    for section in ["positive_tests", "date_sequence_tests", "value_tests", "format_type_tests", "imputation_tests"]:
        if test_name in MOCK_DATA.get(section, {}):
            return MOCK_DATA[section][test_name]
    return None

# Create a flat dictionary for backward compatibility
MOCK_WEATHER_DATA = {key: get_test_case(None, key) for key in MOCK_DATA["test_mappings"]["MissingValueValidator"] + 
                                                              MOCK_DATA["test_mappings"]["OutlierValidator"] + 
                                                              MOCK_DATA["test_mappings"]["DateContinuityValidator"] + 
                                                              MOCK_DATA["test_mappings"]["ImputationValidator"]}

class TestMissingValueValidator(unittest.TestCase):
    def setUp(self):
        self.validator = MissingValueValidator()

    def test_complete_data(self):
        """Test validation of complete data with no missing values"""
        # Arrange
        test_data = pd.DataFrame(MOCK_WEATHER_DATA["complete_data"]["data"])
        
        # Act
        missing_values, df_cleaned = self.validator.validate(test_data)
        
        # Assert
        self.assertEqual(len(missing_values), 0)
        self.assertTrue(df_cleaned.equals(test_data))

    def test_missing_values(self):
        """Test validation of data with missing values across different columns"""
        # Arrange
        test_data = pd.DataFrame(MOCK_WEATHER_DATA["missing_values"]["data"])
        
        # Act
        missing_values, df_cleaned = self.validator.validate(test_data)
        
        # Assert
        self.assertEqual(len(missing_values), 3)  # Should find missing values in all 3 columns
        self.assertIn('mean(air_temperature P1D)', missing_values)
        self.assertIn('sum(precipitation_amount P1D)', missing_values)
        self.assertIn('mean(wind_speed P1D)', missing_values)
        self.assertTrue(df_cleaned.equals(test_data))

    def test_missing_observation(self):
        """Test validation when an entire observation type is missing"""
        # Arrange
        test_data = pd.DataFrame(MOCK_WEATHER_DATA["missing_observation"]["data"])
        
        # Act
        missing_values, df_cleaned = self.validator.validate(test_data)
        
        # Assert
        self.assertEqual(len(missing_values), 0)
        self.assertTrue(df_cleaned.equals(test_data))

    def test_empty_dataframe(self):
        """Test validation with an empty DataFrame"""
        # Arrange
        test_data = pd.DataFrame(MOCK_WEATHER_DATA["empty_dataframe"]["data"])
        
        # Act
        missing_values, df_cleaned = self.validator.validate(test_data)
        
        # Assert
        self.assertEqual(len(missing_values), 0)
        self.assertTrue(df_cleaned.empty)

class TestOutlierValidator(unittest.TestCase):
    def setUp(self):
        """Set up test cases with valid ranges for each measurement type"""
        self.valid_ranges = MOCK_DATA["metadata"]["valid_ranges"]
        self.validator = OutlierValidator(self.valid_ranges)

    def test_complete_data_no_outliers(self):
        """Test validation of complete data with no outliers"""
        # Arrange
        test_data = pd.DataFrame(MOCK_WEATHER_DATA["complete_data"]["data"])
        
        # Act
        outliers, df_cleaned = self.validator.validate(test_data)
        
        # Assert
        self.assertEqual(len(outliers), 0)
        self.assertTrue(df_cleaned.equals(test_data))

    def test_extreme_values(self):
        """Test validation of data with extreme values that should be marked as outliers"""
        # Arrange
        test_data = pd.DataFrame(MOCK_WEATHER_DATA["extreme_values"]["data"])
        expected_outliers = MOCK_WEATHER_DATA["extreme_values"]["expected_outliers"]
        
        # Act
        outliers, df_cleaned = self.validator.validate(test_data)
        
        # Assert
        self.assertEqual(len(outliers), len(expected_outliers))
        for column, indices in expected_outliers.items():
            self.assertIn(column, outliers)
            self.assertEqual(len(outliers[column]), len(indices))

    def test_empty_dataframe(self):
        """Test validation with an empty DataFrame"""
        # Arrange
        test_data = pd.DataFrame(MOCK_WEATHER_DATA["empty_dataframe"]["data"])
        
        # Act
        outliers, df_cleaned = self.validator.validate(test_data)
        
        # Assert
        self.assertEqual(len(outliers), 0)
        self.assertTrue(df_cleaned.empty)

class TestDateContinuityValidator(unittest.TestCase):
    def setUp(self):
        self.validator = DateContinuityValidator()

    def test_complete_data(self):
        """Test validation of complete data with no date gaps"""
        # Arrange
        test_data = pd.DataFrame(MOCK_WEATHER_DATA["complete_data"]["data"])
        test_data['referenceTime'] = pd.to_datetime(test_data['referenceTime'])
        
        # Act
        missing_dates, df_cleaned = self.validator.validate(test_data)
        
        # Assert
        self.assertEqual(len(missing_dates), 0)
        self.assertEqual(len(df_cleaned), len(test_data))

    def test_simple_gaps(self):
        """Test validation of data with simple date gaps"""
        # Arrange
        test_data = pd.DataFrame({
            'referenceTime': ['2020-01-01', '2020-01-02', '2020-01-04', '2020-01-06'],
            'mean(air_temperature P1D)': [1.0, 2.0, 4.0, 6.0]
        })
        test_data['referenceTime'] = pd.to_datetime(test_data['referenceTime'])
        
        # Act
        missing_dates, df_cleaned = self.validator.validate(test_data)
        
        # Assert
        self.assertEqual(len(missing_dates), 2)
        self.assertIn('2020-01-03', missing_dates)
        self.assertIn('2020-01-05', missing_dates)
        self.assertEqual(len(df_cleaned), 6)  # Original dates + missing dates

    def test_empty_dataframe(self):
        """Test validation with an empty DataFrame"""
        # Arrange
        test_data = pd.DataFrame(MOCK_WEATHER_DATA["empty_dataframe"]["data"])
        test_data['referenceTime'] = pd.to_datetime(test_data['referenceTime'])
        
        # Act
        missing_dates, df_cleaned = self.validator.validate(test_data)
        
        # Assert
        self.assertEqual(len(missing_dates), 0)
        self.assertTrue(df_cleaned.empty)

    def test_month_boundary_gaps(self):
        """Test validation of data with gaps across month boundaries"""
        # Arrange
        test_data = pd.DataFrame(MOCK_WEATHER_DATA["date_gaps_month_boundary"]["data"])
        expected_missing = MOCK_WEATHER_DATA["date_gaps_month_boundary"]["expected_missing_dates"]
        
        # Act
        missing_dates, df_cleaned = self.validator.validate(test_data)
        
        # Assert
        self.assertEqual(len(missing_dates), len(expected_missing))
        self.assertListEqual(missing_dates, expected_missing)
        self.assertEqual(len(df_cleaned), len(test_data) + len(expected_missing))

    def test_year_boundary_gaps(self):
        """Test validation of data with gaps across year boundaries"""
        # Arrange
        test_data = pd.DataFrame(MOCK_WEATHER_DATA["year_boundary_gaps"]["data"])
        expected_missing = MOCK_WEATHER_DATA["year_boundary_gaps"]["expected_missing_dates"]
        
        # Act
        missing_dates, df_cleaned = self.validator.validate(test_data)
        
        # Assert
        self.assertEqual(len(missing_dates), len(expected_missing))
        self.assertListEqual(missing_dates, expected_missing)
        self.assertEqual(len(df_cleaned), len(test_data) + len(expected_missing))

    def test_duplicate_dates(self):
        """Test validation of data with duplicate dates"""
        # Arrange
        test_data = pd.DataFrame(MOCK_WEATHER_DATA["duplicate_dates"]["data"])
        
        # Act and Assert
        with self.assertRaises(ValueError) as context:
            missing_dates, df_cleaned = self.validator.validate(test_data)
        
        # Check that we got the expected error message
        self.assertTrue("cannot reindex on an axis with duplicate labels" in str(context.exception))

class TestImputationValidator(unittest.TestCase):
    def setUp(self):
        """Initialize the ImputationValidator with default settings"""
        self.validator = ImputationValidator(n_neighbors=3)
        # Get valid ranges from metadata
        self.valid_ranges = MOCK_DATA["metadata"]["valid_ranges"]

    def test_complete_data_no_imputation(self):
        """Test that no imputation is performed on complete data"""
        # Setup validators
        missing_validator = MissingValueValidator()
        outlier_validator = OutlierValidator(self.valid_ranges)
        continuity_validator = DateContinuityValidator()
        
        # Process data through validation chain
        test_data = pd.DataFrame(MOCK_WEATHER_DATA["complete_data"]["data"])
        _, df_cleaned = missing_validator.validate(test_data)
        _, df_cleaned = outlier_validator.validate(df_cleaned)
        _, df_cleaned = continuity_validator.validate(df_cleaned)
        
        # Now test imputation
        imputation_results, df_cleaned = self.validator.validate(df_cleaned)
        
        # Assert no values were marked for imputation
        for col_name, imputed_count in imputation_results.items():
            self.assertEqual(imputed_count, 0)
        
        # Check tracking columns were created but all marked as False
        numeric_cols = ['mean(air_temperature P1D)', 'sum(precipitation_amount P1D)', 'mean(wind_speed P1D)']
        for col in numeric_cols:
            tracking_col = f'generated_{col}'
            self.assertIn(tracking_col, df_cleaned.columns)
            self.assertTrue(all(df_cleaned[tracking_col] == False))
            
    def test_imputation_after_validation_chain(self):
        """Test imputation after data has gone through all previous validators"""
        # Setup validators
        missing_validator = MissingValueValidator()
        outlier_validator = OutlierValidator(self.valid_ranges)
        continuity_validator = DateContinuityValidator()

        # Get test data from mock file
        test_data = pd.DataFrame(MOCK_WEATHER_DATA["imputation_test_data"]["data"])
        
        # Convert referenceTime to datetime
        test_data['referenceTime'] = pd.to_datetime(test_data['referenceTime'])

        # Run through validation chain
        _, df_cleaned = missing_validator.validate(test_data)
        _, df_cleaned = outlier_validator.validate(df_cleaned)
        _, df_cleaned = continuity_validator.validate(df_cleaned)
        
        # Store data before imputation to compare
        nan_counts_before = df_cleaned.isna().sum()
        
        # Test imputation
        imputation_results, df_cleaned = self.validator.validate(df_cleaned)
        
        # Verify we got imputation counts matching our NaN counts
        for column in ['mean(air_temperature P1D)', 'sum(precipitation_amount P1D)', 'mean(wind_speed P1D)']:
            self.assertEqual(imputation_results[column], nan_counts_before[column])
        
        # Check tracking columns exist and have True values where values were imputed
        self.assertTrue('generated_mean(air_temperature P1D)' in df_cleaned.columns)
        self.assertTrue('generated_sum(precipitation_amount P1D)' in df_cleaned.columns)
        self.assertTrue('generated_mean(wind_speed P1D)' in df_cleaned.columns)
        
        # Check imputed values are within valid ranges
        self.assertTrue(all(-50 <= df_cleaned['mean(air_temperature P1D)']))
        self.assertTrue(all(df_cleaned['mean(air_temperature P1D)'] <= 50))
        self.assertTrue(all(0 <= df_cleaned['sum(precipitation_amount P1D)']))
        self.assertTrue(all(df_cleaned['sum(precipitation_amount P1D)'] <= 500))
        self.assertTrue(all(0 <= df_cleaned['mean(wind_speed P1D)']))
        self.assertTrue(all(df_cleaned['mean(wind_speed P1D)'] <= 100))
        
        # Check that all NaN values were filled
        self.assertTrue(not df_cleaned['mean(air_temperature P1D)'].isna().any())
        self.assertTrue(not df_cleaned['sum(precipitation_amount P1D)'].isna().any())
        self.assertTrue(not df_cleaned['mean(wind_speed P1D)'].isna().any())

if __name__ == '__main__':
    unittest.main()