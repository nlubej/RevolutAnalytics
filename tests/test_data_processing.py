# tests/test_data_processing.py
import unittest
from src.modules import data_processing
from src.utils import csv_parser

class TestDataProcessing(unittest.TestCase):
    def test_calculate_average_age(self):
        # Test with a sample CSV file
        sample_csv_file = 'data/input/account-statement_2023-09-01_2023-09-30_en_865466.csv'

        # Parse the CSV file
        csv_data = csv_parser.parse_csv(sample_csv_file)
        
        # Calculate the average age
        cardPayments = data_processing.getCardPayments(csv_data)

        # The expected average age is (25 + 30 + 22 + 28) / 4 = 26.25
        self.assertAlmostEqual(len(cardPayments), 21)

if __name__ == '__main__':
    unittest.main()
