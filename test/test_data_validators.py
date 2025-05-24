import unittest
import pandas as pd
import numpy as np
import sys
import os
import json

# Legger til prosjektets rotmappe i Python-path for å kunne importere moduler
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.data_cleaning.data_validators import MissingValueValidator, OutlierValidator, DateContinuityValidator, ImputationValidator

# Laster inn mock-data fra en JSON-fil
with open(os.path.join(os.path.dirname(__file__), 'mock_weather_data.json'), 'r') as f:
    MOCK_DATA = json.load(f)

def get_test_case(category, test_name):
    """
    Hjelpefunksjon for å hente testdata fra en strukturert JSON-fil.

    Args:
        category (str): Kategori av testen (ikke brukt her, men kan utvides).
        test_name (str): Navnet på testen som skal hentes.

    Returns:
        dict: Testdata for den spesifikke testen, eller None hvis ikke funnet.
    """
    for section in ["positive_tests", "date_sequence_tests", "value_tests", "format_type_tests", "imputation_tests"]:
        if test_name in MOCK_DATA.get(section, {}):
            return MOCK_DATA[section][test_name]
    return None

# Oppretter en flat struktur for testdata for bakoverkompatibilitet
MOCK_WEATHER_DATA = {key: get_test_case(None, key) for key in MOCK_DATA["test_mappings"]["MissingValueValidator"] + 
                                                              MOCK_DATA["test_mappings"]["OutlierValidator"] + 
                                                              MOCK_DATA["test_mappings"]["DateContinuityValidator"] + 
                                                              MOCK_DATA["test_mappings"]["ImputationValidator"]}

class TestMissingValueValidator(unittest.TestCase):
    """
    Tester for MissingValueValidator-klassen, som håndterer manglende verdier i datasett.
    """

    def setUp(self):
        """
        Initialiserer MissingValueValidator for hver test.
        """
        self.validator = MissingValueValidator()

    def test_complete_data(self):
        """
        Tester validering av komplett data uten manglende verdier.
        """
        # Setter opp testdata
        test_data = pd.DataFrame(MOCK_WEATHER_DATA["complete_data"]["data"])
        
        # Kjører validering
        missing_values, df_cleaned = self.validator.validate(test_data)
        
        # Sjekker at ingen manglende verdier ble funnet
        self.assertEqual(len(missing_values), 0)
        self.assertTrue(df_cleaned.equals(test_data))

    def test_missing_values(self):
        """
        Tester validering av data med manglende verdier i flere kolonner.
        """
        # Setter opp testdata
        test_data = pd.DataFrame(MOCK_WEATHER_DATA["missing_values"]["data"])
        
        # Kjører validering
        missing_values, df_cleaned = self.validator.validate(test_data)
        
        # Sjekker at manglende verdier ble funnet i de forventede kolonnene
        self.assertEqual(len(missing_values), 3)
        self.assertIn('mean(air_temperature P1D)', missing_values)
        self.assertIn('sum(precipitation_amount P1D)', missing_values)
        self.assertIn('mean(wind_speed P1D)', missing_values)
        self.assertTrue(df_cleaned.equals(test_data))

    def test_missing_observation(self):
        """
        Tester validering når en hel observasjonstype mangler.
        """
        # Setter opp testdata
        test_data = pd.DataFrame(MOCK_WEATHER_DATA["missing_observation"]["data"])
        
        # Kjører validering
        missing_values, df_cleaned = self.validator.validate(test_data)
        
        # Sjekker at ingen manglende verdier ble funnet
        self.assertEqual(len(missing_values), 0)
        self.assertTrue(df_cleaned.equals(test_data))

    def test_empty_dataframe(self):
        """
        Tester validering med en tom DataFrame.
        """
        # Setter opp testdata
        test_data = pd.DataFrame(MOCK_WEATHER_DATA["empty_dataframe"]["data"])
        
        # Kjører validering
        missing_values, df_cleaned = self.validator.validate(test_data)
        
        # Sjekker at ingen manglende verdier ble funnet og at DataFrame er tom
        self.assertEqual(len(missing_values), 0)
        self.assertTrue(df_cleaned.empty)

class TestOutlierValidator(unittest.TestCase):
    """
    Tester for OutlierValidator-klassen, som håndterer ekstreme verdier i datasett.
    """

    def setUp(self):
        """
        Initialiserer OutlierValidator med gyldige verdier for hver målingstype.
        """
        self.valid_ranges = MOCK_DATA["metadata"]["valid_ranges"]
        self.validator = OutlierValidator(self.valid_ranges)

    def test_complete_data_no_outliers(self):
        """
        Tester validering av komplett data uten ekstreme verdier.
        """
        # Setter opp testdata
        test_data = pd.DataFrame(MOCK_WEATHER_DATA["complete_data"]["data"])
        
        # Kjører validering
        outliers, df_cleaned = self.validator.validate(test_data)
        
        # Sjekker at ingen ekstreme verdier ble funnet
        self.assertEqual(len(outliers), 0)
        self.assertTrue(df_cleaned.equals(test_data))

    def test_extreme_values(self):
        """
        Tester validering av data med ekstreme verdier som skal markeres som outliers.
        """
        # Setter opp testdata
        test_data = pd.DataFrame(MOCK_WEATHER_DATA["extreme_values"]["data"])
        expected_outliers = MOCK_WEATHER_DATA["extreme_values"]["expected_outliers"]
        
        # Kjører validering
        outliers, df_cleaned = self.validator.validate(test_data)
        
        # Sjekker at de forventede outliers ble funnet
        self.assertEqual(len(outliers), len(expected_outliers))
        for column, indices in expected_outliers.items():
            self.assertIn(column, outliers)
            self.assertEqual(len(outliers[column]), len(indices))

    def test_empty_dataframe(self):
        """
        Tester validering med en tom DataFrame.
        """
        # Setter opp testdata
        test_data = pd.DataFrame(MOCK_WEATHER_DATA["empty_dataframe"]["data"])
        
        # Kjører validering
        outliers, df_cleaned = self.validator.validate(test_data)
        
        # Sjekker at ingen outliers ble funnet og at DataFrame er tom
        self.assertEqual(len(outliers), 0)
        self.assertTrue(df_cleaned.empty)

class TestDateContinuityValidator(unittest.TestCase):
    """
    Tester for DateContinuityValidator-klassen, som håndterer datokontinuitet i tidsserier.
    """

    def setUp(self):
        """
        Initialiserer DateContinuityValidator for hver test.
        """
        self.validator = DateContinuityValidator()

    def test_complete_data(self):
        """
        Tester validering av komplett data uten datogap.
        """
        # Setter opp testdata
        test_data = pd.DataFrame(MOCK_WEATHER_DATA["complete_data"]["data"])
        test_data['referenceTime'] = pd.to_datetime(test_data['referenceTime'])
        
        # Kjører validering
        missing_dates, df_cleaned = self.validator.validate(test_data)
        
        # Sjekker at det ikke er noen manglende datoer
        self.assertEqual(len(missing_dates), 0)
        self.assertEqual(len(df_cleaned), len(test_data))

    def test_simple_gaps(self):
        """
        Tester validering av data med enkle datogap.
        """
        # Setter opp testdata
        test_data = pd.DataFrame({
            'referenceTime': ['2020-01-01', '2020-01-02', '2020-01-04', '2020-01-06'],
            'mean(air_temperature P1D)': [1.0, 2.0, 4.0, 6.0]
        })
        test_data['referenceTime'] = pd.to_datetime(test_data['referenceTime'])
        
        # Kjører validering
        missing_dates, df_cleaned = self.validator.validate(test_data)
        
        # Sjekker at de manglende datoene ble korrekt identifisert
        self.assertEqual(len(missing_dates), 2)
        self.assertIn('2020-01-03', missing_dates)
        self.assertIn('2020-01-05', missing_dates)
        self.assertEqual(len(df_cleaned), 6)  # Originaldatoer + manglende datoer

    def test_empty_dataframe(self):
        """
        Tester validering med en tom DataFrame.
        """
        # Arrange
        test_data = pd.DataFrame(MOCK_WEATHER_DATA["empty_dataframe"]["data"])
        test_data['referenceTime'] = pd.to_datetime(test_data['referenceTime'])
        
        # Act
        missing_dates, df_cleaned = self.validator.validate(test_data)
        
        # Assert
        self.assertEqual(len(missing_dates), 0)
        self.assertTrue(df_cleaned.empty)

    def test_month_boundary_gaps(self):
        """
        Tester validering av data med datogap over månedsskifter.
        """
        # Setter opp testdata
        test_data = pd.DataFrame(MOCK_WEATHER_DATA["date_gaps_month_boundary"]["data"])
        expected_missing = MOCK_WEATHER_DATA["date_gaps_month_boundary"]["expected_missing_dates"]
        
        # Kjører validering
        missing_dates, df_cleaned = self.validator.validate(test_data)
        
        # Sjekker at de manglende datoene ble korrekt identifisert
        self.assertEqual(len(missing_dates), len(expected_missing))
        self.assertListEqual(missing_dates, expected_missing)
        self.assertEqual(len(df_cleaned), len(test_data) + len(expected_missing))

    def test_year_boundary_gaps(self):
        """
        Tester validering av data med datogap over årsskifter.
        """
        # Setter opp testdata
        test_data = pd.DataFrame(MOCK_WEATHER_DATA["year_boundary_gaps"]["data"])
        expected_missing = MOCK_WEATHER_DATA["year_boundary_gaps"]["expected_missing_dates"]
        
        # Kjører validering
        missing_dates, df_cleaned = self.validator.validate(test_data)
        
        # Sjekker at de manglende datoene ble korrekt identifisert
        self.assertEqual(len(missing_dates), len(expected_missing))
        self.assertListEqual(missing_dates, expected_missing)
        self.assertEqual(len(df_cleaned), len(test_data) + len(expected_missing))

    def test_duplicate_dates(self):
        """
        Tester validering av data med dupliserte datoer.
        """
        # Arrange
        test_data = pd.DataFrame(MOCK_WEATHER_DATA["duplicate_dates"]["data"])
        
        # Act and Assert
        with self.assertRaises(ValueError) as context:
            missing_dates, df_cleaned = self.validator.validate(test_data)
        
        # Sjekker at vi fikk den forventede feilmeldingen
        self.assertTrue("cannot reindex on an axis with duplicate labels" in str(context.exception))

class TestImputationValidator(unittest.TestCase):
    """
    Tester for ImputationValidator-klassen, som håndterer imputering av manglende verdier.
    """

    def setUp(self):
        """
        Initialiserer ImputationValidator med standardinnstillinger.
        """
        self.validator = ImputationValidator(n_neighbors=3)
        # Henter gyldige verdier fra metadata
        self.valid_ranges = MOCK_DATA["metadata"]["valid_ranges"]

    def test_complete_data_no_imputation(self):
        """
        Tester at ingen imputering skjer på komplett data.
        """
        # Setter opp validatorer
        missing_validator = MissingValueValidator()
        outlier_validator = OutlierValidator(self.valid_ranges)
        continuity_validator = DateContinuityValidator()
        
        # Behandler data gjennom valideringskjeden
        test_data = pd.DataFrame(MOCK_WEATHER_DATA["complete_data"]["data"])
        _, df_cleaned = missing_validator.validate(test_data)
        _, df_cleaned = outlier_validator.validate(df_cleaned)
        _, df_cleaned = continuity_validator.validate(df_cleaned)
        
        # Nå tester vi imputering
        imputation_results, df_cleaned = self.validator.validate(df_cleaned)
        
        # Sjekker at ingen verdier ble markert for imputering
        for col_name, imputed_count in imputation_results.items():
            self.assertEqual(imputed_count, 0)
        
        # Sjekker at sporingskolonner ble opprettet, men alle merket som False
        numeric_cols = ['mean(air_temperature P1D)', 'sum(precipitation_amount P1D)', 'mean(wind_speed P1D)']
        for col in numeric_cols:
            tracking_col = f'generated_{col}'
            self.assertIn(tracking_col, df_cleaned.columns)
            self.assertTrue(all(df_cleaned[tracking_col] == False))
            
    def test_imputation_after_validation_chain(self):
        """
        Tester imputering etter at data har gått gjennom alle tidligere validatorer.
        """
        # Setter opp validatorer
        missing_validator = MissingValueValidator()
        outlier_validator = OutlierValidator(self.valid_ranges)
        continuity_validator = DateContinuityValidator()

        # Henter testdata fra mock-fil
        test_data = pd.DataFrame(MOCK_WEATHER_DATA["imputation_test_data"]["data"])
        
        # Konverterer referenceTime til datetime
        test_data['referenceTime'] = pd.to_datetime(test_data['referenceTime'])

        # Kjører gjennom valideringskjeden
        _, df_cleaned = missing_validator.validate(test_data)
        _, df_cleaned = outlier_validator.validate(df_cleaned)
        _, df_cleaned = continuity_validator.validate(df_cleaned)
        
        # Lagrer data før imputering for sammenligning
        nan_counts_before = df_cleaned.isna().sum()
        
        # Tester imputering
        imputation_results, df_cleaned = self.validator.validate(df_cleaned)
        
        # Verifiserer at vi fikk imputeringstall som samsvarer med NaN-tallene våre
        for column in ['mean(air_temperature P1D)', 'sum(precipitation_amount P1D)', 'mean(wind_speed P1D)']:
            self.assertEqual(imputation_results[column], nan_counts_before[column])
        
        # Sjekker at sporingskolonner eksisterer og har True-verdier der verdier ble imputert
        self.assertTrue('generated_mean(air_temperature P1D)' in df_cleaned.columns)
        self.assertTrue('generated_sum(precipitation_amount P1D)' in df_cleaned.columns)
        self.assertTrue('generated_mean(wind_speed P1D)' in df_cleaned.columns)
        
        # Sjekker at imputerte verdier er innenfor gyldige områder
        self.assertTrue(all(-50 <= df_cleaned['mean(air_temperature P1D)']))
        self.assertTrue(all(df_cleaned['mean(air_temperature P1D)'] <= 50))
        self.assertTrue(all(0 <= df_cleaned['sum(precipitation_amount P1D)']))
        self.assertTrue(all(df_cleaned['sum(precipitation_amount P1D)'] <= 500))
        self.assertTrue(all(0 <= df_cleaned['mean(wind_speed P1D)']))
        self.assertTrue(all(df_cleaned['mean(wind_speed P1D)'] <= 100))
        
        # Sjekker at alle NaN-verdier ble fylt ut
        self.assertTrue(not df_cleaned['mean(air_temperature P1D)'].isna().any())
        self.assertTrue(not df_cleaned['sum(precipitation_amount P1D)'].isna().any())
        self.assertTrue(not df_cleaned['mean(wind_speed P1D)'].isna().any())

if __name__ == '__main__':
    unittest.main()