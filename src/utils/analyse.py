
import pandas as pd
import matplotlib.pyplot as plt
from src.utils import csv_parser

def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i]+5, round(y[i]), ha = 'center')

def analyse_month(df, file_folder):
    # Group by 'Category' and sum 'Amount'
    category_sums = df.groupby('Category')['Amount'].sum().reset_index()

    # Create a bar plot
    plt.figure(figsize=(10, 6))
    plt.bar(category_sums['Category'], category_sums['Amount'])
    addlabels(category_sums['Category'], category_sums['Amount'])

    plt.xlabel('Category')
    plt.ylabel('Total Amount')
    total_sum = round(df['Amount'].sum())
    plt.title('Total Amount by Category. Total: ' +  str(total_sum))
    #plt.show()

    plt.savefig(f'{file_folder}/result_plot.png', dpi=300, bbox_inches='tight')

def analyse_year(category, df, file_folder):

    df = df[df['Category'] == category]

    # Group by 'Category' and sum 'Amount'
    category_sums = df.groupby('Date')['Amount'].sum().reset_index()

    # Create a bar plot
    plt.figure(figsize=(10, 6))
    plt.bar(category_sums['Date'], category_sums['Amount'])
    addlabels(category_sums['Date'], category_sums['Amount'])

    plt.xlabel('Date')
    plt.ylabel('Total Amount')
    plt.title(f'Total Amount by Date for {category}')
    #plt.show()

    plt.savefig(f'{file_folder}/result_plot_{category}.png', dpi=300, bbox_inches='tight')

    # Store processed statement to csv
    csv_parser.write_to_csv(df, f'{file_folder}/output_data{category}.csv')