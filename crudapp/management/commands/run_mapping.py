import re
import os

from mappings import *


import pandas as pd

def join_date_time(df):
    """Combine date and time columns into a standard ISO datetime format."""
    # Assumes that the dataframe has 'collection_date' and 'collection_time' columns
    df['collection_datetime'] = pd.to_datetime(
        df['collection_date'] + ' ' + df['collection_time'],
        format='mixed'
    )
    df['collection_datetime'] = df['collection_datetime'].dt.strftime('%Y-%m-%dT%H:%M:%S')
    return df.drop(columns=['collection_date', 'collection_time'])  # Optionally drop the original columns

def preprocess_csv(input_file, processing_function, output_file):
    """
    Load a CSV, process it using a provided function, and save the processed data to a new file.

    Parameters:
    - input_file (str): Path to the source CSV file.
    - processing_function (function): A function that takes a DataFrame and returns a processed DataFrame.
    - output_file (str): Path to save the processed CSV file.
    """
    # Load data from CSV
    df = pd.read_csv(input_file, encoding='utf-8')

    # Process data using the provided function
    processed_df = processing_function(df)

    # Save the processed DataFrame to a new CSV file
    processed_df.to_csv(output_file, index=False)

    print(f"Data successfully processed and saved to {output_file}")

def replace_tabs_with_spaces(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Replace tabs with four spaces (adjust the number of spaces as per your style guide)
    updated_content = re.sub('\t', '    ', content)
    
    with open(file_path, 'w') as file:
        file.write(updated_content)

def fill_remarks(df):
    """
    Fill null values in the 'remarks' column with a default value.

    Parameters:
    - df (DataFrame): The input DataFrame.

    Returns:
    - DataFrame: The processed DataFrame with null values in 'remarks' filled.
    """
    # Fill null values in the 'remarks' column with "No remarks"
    df['remarks'] = df['remarks'].fillna('No remarks')
    
    return df

base_path = './_no_data'
raw_csv = 'raw/cuttings/tb_cuttings.csv'
output_csv = ''
preprocessed_csv = 'processed/preprocessed_tb_cuttings'
mapping_file = 'raw/cuttings/mappings.yaml'
output_csv = 'processed/tb_cutting.csv'


replace_tabs_with_spaces(os.path.join(base_path, mapping_file))
preprocess_csv(os.path.join(base_path, raw_csv), join_date_time ,os.path.join(base_path, preprocessed_csv))
preprocess_csv(os.path.join(base_path, raw_csv), fill_remarks ,os.path.join(base_path, preprocessed_csv))
process_csv_data(base_path, preprocessed_csv, mapping_file, output_csv)