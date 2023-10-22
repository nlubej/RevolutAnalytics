# main.py
import os
import glob
import shutil
import sys
from src.bank_statement_processor import BankStatementProcessor
from src.transaction_handler import TransactionHandler

def get_param(param, default = None): 
    # Check if the desired parameter is provided
    if param in sys.argv:
        # Find the index of the desired parameter in sys.argv
        index = sys.argv.index(param)

        # Get the value of the parameter from the next argument
        if index + 1 < len(sys.argv):
            value = sys.argv[index + 1]
            return value

    return default

def get_action():
    if '-update' in sys.argv:
        year = get_param('-year', '*')
        month = get_param('-month', '*')
        return {
            'action': 'Update',
            'params': {
                'year': year,
                'month': month
            }
        }
    elif '-clear' in sys.argv:
        year = get_param('-year')
        month = get_param('-month')
        return {
            'action': 'Clear',
            'params': {
                'year': year,
                'month': month
            }
        }
    
    return {
        'action': None
    }

def process_statements():
    processor = BankStatementProcessor()

    for statement_file in glob.glob(f'data/input/statements/*/*.csv'):
        processor.process_bank_statement(statement_file)   
        
        # Archive statement_file
        shutil.move(statement_file, f'data/archive/{statement_file.split(os.sep, 2)[2]}')

def refresh_merchant_category():
    TransactionHandler().modify_transaction_category()

def clear_data(params):
    year = params.get('year')
    month = params.get('month')
    TransactionHandler().clear_transactions(year, month)

def main():
    mode = get_action()

    if (mode['action'] == 'Update'):
        refresh_merchant_category()
    elif (mode['action'] == 'Clear'):
        clear_data(mode['params'])
    else:
        process_statements()
        
if __name__ == "__main__":
    main()