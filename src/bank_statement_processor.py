import os
import pandas as pd
from src.merchant_category_manager import MerchantCategoryManager

class BankStatementProcessor:
    def __init__(self):
        self.merchant_mng = MerchantCategoryManager()

    def process_bank_statement(self, statement_file):
        # Parse account from statement full path.
        account = statement_file.rsplit(os.sep, 2)[-2]

        df = pd.read_csv(statement_file)
        df = df[df['Type'] == 'CARD_PAYMENT']
        df = df.apply(self.__map_statement, args=(account,), axis=1)

        self.merchant_mng.save_merchant_data()


        # Save data to output file
        output_path = 'data/output/transactions.csv'
        include_header = False if os.path.exists(output_path) else True
        mode =  'a' if os.path.exists(output_path) else 'w'
        df.to_csv(output_path, mode=mode, header=include_header, index=False)
    
    def __map_statement(self, row, account):
        mapped_values = {
            'Account': account,
            'Merchant': row['Description'],
            'Category': self.merchant_mng.determine_category(row['Description']),
            'Amount': abs(row['Amount']),
            'Date': pd.to_datetime(row['Started Date']).strftime('%Y-%m')
        }
        return pd.Series(mapped_values)