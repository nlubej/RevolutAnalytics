# tests/test_csv_parser.py
import unittest
from src.utils import csv_parser

class TestCsvParser(unittest.TestCase):
    def test_parse_csv(self):
        # Test with a sample CSV file
        sample_csv_file = 'data/input/account-statement_2023-09-01_2023-09-30_en_865466.csv'

        # Parse the CSV file
        csv_data = csv_parser.parse_csv(sample_csv_file)

        # Assert that the parsed data matches the expected data
        self.assertEqual(len(csv_data), 121)
        self.assertEqual(len(csv_data.columns), 3)

if __name__ == '__main__':
    unittest.main()
