import pandas as pd
from src.merchant_category_manager import MerchantCategoryManager

class TransactionHandler:
    def __init__(self):
        self.merchant_mng = MerchantCategoryManager()

    def modify_transaction_category(self):
        output_file = 'data/output/transactions.csv'
        df = pd.read_csv(output_file)

        # Update Category based on the new values
        df['Category'] = df.apply(lambda row: self.merchant_mng.determine_category(row['Merchant']), axis=1)

        # Save data to output file
        df.to_csv(output_file, mode='w', header=True, index=False)

    def clear_transactions(self, year, month):
        output_file = 'data/output/transactions.csv'
        df = pd.read_csv(output_file)

        if year and month:
           condition = (df['Date'].str.split('-').str[0] == year) & (df['Date'].str.split('-').str[1] == month.zfill(2))
        elif year:
           condition = df['Date'].str.split('-').str[0] == year
        elif month:
            condition = df['Date'].str.split('-').str[1] == month.zfill(2)
        else:
            # Always false
            condition = df['Account'] == None

        #df = df[condition]
        df = df.drop(df[condition].index)
        print(df)

        # Save data to output file
        df.to_csv(output_file, mode='w', header=True, index=False)