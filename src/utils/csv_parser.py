import os
import pandas as pd

def parse_csv(file_path):
    df = pd.read_csv(file_path)

    # create column Category if not exists
    if 'Category' not in df.columns:
        df['Category'] = None
    
    # Map Started Date to year-month format
    if 'Started Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Started Date'])
        df['Date'] = df['Date'].dt.strftime('%Y-%m')

    return df[['Type', 'Description', 'Category', 'Amount', 'Date']]

def write_to_csv(dataframe, file_path, override = False):
    try:
        # Append data if file already exists
        if not override and os.path.exists(file_path):
            dataframe.to_csv(file_path, mode='a', header=False, index=False)
        else:
            dataframe.to_csv(file_path, index=False)

    except Exception as e:
        print(f"Error writing data to CSV file: {str(e)}")