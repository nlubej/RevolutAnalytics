# src/modules/data_processing.py
import pandas as pd
from api import chatgpt_api

def process_data(df, merchant_category):
    df = df[df['Type'] == 'CARD_PAYMENT']
    processed_df = df.apply(map_row, args=(merchant_category,), axis=1)
    return processed_df

def map_row(row, merchant_category):
    mapped_values = {
        'Type': row['Type'],
        'Description': row['Description'],
        'Category': get_category(row['Description'], merchant_category),
        'Amount': abs(row['Amount']),
        'Date': row['Date']
    }
    return pd.Series(mapped_values)

def get_category(decription, merchant_category):
    result = None

    if decription in merchant_category.keys() and merchant_category[decription] != None:
        return merchant_category[decription]
    try:
        response = chatgpt_api.chat_with_gpt(decription)
        result = None if response == 'None' else response
    except Exception as e:
        print('Error', e)
    finally:
        # Update merchant category
        merchant_category[decription] = result
        return result