# main.py
import os
import glob
import shutil
import json
import sys
import pandas as pd
from pathlib import Path
from src.utils import csv_parser
from src.modules import data_processing
from src.utils import analyse

def get_param(param): 
    # Check if the desired parameter is provided
    if param in sys.argv:
        # Find the index of the desired parameter in sys.argv
        index = sys.argv.index(param)

        # Get the value of the parameter from the next argument
        if index + 1 < len(sys.argv):
            parameter_value = sys.argv[index + 1]
            return parameter_value
    return None

def get_action():
    if '-refresh' in sys.argv:
        year = get_param('-year')
        month = get_param('-month')
        return {
            'action': 'Refresh',
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

def process_file(csv_file, merchant_category):
    df = csv_parser.parse_csv(csv_file)
    df = data_processing.process_data(df, merchant_category)
    return df

def process_csv_files(csv_files, merchant_category):
    for csv_file in csv_files:
        # Process bank statement
        df = process_file(csv_file, merchant_category)
        grouped_df = df.groupby('Date')

        # for each date group, analyse the data
        for group_name, group_data in grouped_df:
            year, month = group_name.split('-')
            data_folder = f'files/data/{year}/{month}'      
            
            if not os.path.exists(data_folder):
                os.makedirs(data_folder, exist_ok=True)     

            analyse.analyse_month(group_data, data_folder)

            # Store data to csv
            csv_parser.write_to_csv(group_data, f'{data_folder}/output_data.csv')

        # Move file to processed folder
        shutil.move(csv_file, f'files/archive/{os.path.basename(csv_file)}')

def get_param_value(params, name, default):
    value = params.get(name)
    return default if value == None else value

def refresh_categories(params, merchant_category):
    year = get_param_value(params, 'year', '*')
    month = get_param_value(params,'month', '*')
    csv_files = glob.glob(f'files/data/{year}/{month}/output_data.csv')
    
    for csv_file in csv_files:
        file_folder = os.path.dirname(csv_file)
        df = process_file(csv_file, merchant_category)

        # Store data to csv
        csv_parser.write_to_csv(df, f'{file_folder}/output_data.csv', True)

        analyse.analyse_month(df, file_folder)

def clear_data(params):
    directory = Path('files/data')
    year = get_param_value(params, 'year', '*')
    month = get_param_value(params,'month', '*')
    subdirectories = list(directory.glob(f'{year}/{month}'))
    print(subdirectories)
    for subdirectory in subdirectories:
        shutil.rmtree(subdirectory, ignore_errors=True)

def main():
    statements_folder = 'files/statements'
    csv_files = glob.glob(f'{statements_folder}/*.csv')
    
    mode = get_action()

    # Load merchant category data
    with open('merchantCategory.json', 'r', encoding='utf-8') as json_file:
        merchant_category = json.load(json_file)

    if (mode['action'] == 'Refresh'):
        refresh_categories(mode['params'] , merchant_category)
    if (mode['action'] == 'Clear'):
        clear_data(mode['params'])
    else:
        process_csv_files(csv_files, merchant_category)

    if mode['action'] != 'Clear':
        output_files = glob.glob(f'files/data/*/*/output_data.csv')
        df_all = pd.DataFrame()
        for output_file in output_files:
            df = csv_parser.parse_csv(output_file)
            df_all = pd.concat([df_all, df], axis=0)
        
        analyse.analyse_year('Groceries', df_all, 'files/charts')
        analyse.analyse_year('Shopping', df_all, 'files/charts')
        analyse.analyse_year('Restaurants', df_all, 'files/charts')

    # Update mercant categories
    with open('merchantCategory.json', 'w', encoding='utf-8') as json_file:
        json.dump(merchant_category, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()