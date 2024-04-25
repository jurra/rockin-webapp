'''
The mappings process is designed to transform both the column names and specific data values within a given column based on mappings defined in a YAML file. The script does two main types of mappings:

1. **Column Name Mappings** (`column_mappings`): This mapping is applied to rename the columns of the DataFrame. These mappings are taken directly from the CSV file's column names and are matched against keys in the `column_mappings` section of the YAML file.

2. **Data Value Mappings** (`data_mappings`): This mapping is applied to transform the data values in a specific column (`column_to_modify`). The keys for these mappings would be the original values from the specified column in the CSV file, and the values would be what these original data points should be transformed into, as defined in the `data_mappings` section of the YAML file.

Here's how you might define these mappings in a YAML file to make it clear which mappings are for column names (input from the CSV) and which are for specific data values within a column:

```yaml
column_mappings:
  CSVColumnName1: ModelFieldName1
  CSVColumnName2: ModelFieldName2
  CSVColumnName3: ModelFieldName3
  ...

data_mappings:
  OriginalDataValue1: NewDataValue1
  OriginalDataValue2: NewDataValue2
  OriginalDataValue3: NewDataValue3
  ...
```

- `column_mappings` are applied globally across the entire DataFrame to rename columns based on how they match up with your model fields or how you want them to be named in the output.
- `data_mappings` are specifically applied to transform values within the `column_to_modify` that you specify when running the script.

To indicate in your YAML file which mappings are the target and which are input from the CSV file, you might structure your YAML file as shown above, where:
- `column_mappings` dictate the input from the CSV file and how each should be renamed (or targeted) in the DataFrame.
- `data_mappings` show the transformation of specific values within a targeted column.

In your script, the `column_to_modify` argument you pass to the `apply_mappings` function specifies which column's data values should be mapped according to `data_mappings` in the YAML file. This column should exist in the CSV file after column name mappings have been applied, if any.

Remember, the actual transformation and application of these mappings depend on correctly specifying them in the YAML file and ensuring your CSV contains the expected columns and data values.

'''
import pandas as pd
import yaml
import csv

def load_mappings(yaml_file):
    """Load column name and data value mappings from a YAML file.
    """
    with open(yaml_file, 'r') as file:
        mappings = yaml.safe_load(file)
    return mappings.get('column_mappings', {}), mappings.get('data_mappings', {}), mappings.get('ignore_columns', [])

def validate_csv_delimiter(csv_file):
    """
    Validates that the CSV file uses commas as delimiters. Raises a ValueError
    if the delimiter is not a comma.

    Args:
        csv_file (str): Path to the CSV file.
    """
    with open(csv_file, 'r', encoding='utf-8') as file:
        # Read the first line and infer the delimiter
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(file.readline(), delimiters=",")
        
        if dialect.delimiter != ',':
            raise ValueError(f"The CSV file is not delimited with commas but with '{dialect.delimiter}'.")


def apply_mappings(csv_file, column_mappings, data_mappings, column_to_modify, output_file, ignore_columns):
    """
    Apply mappings to column names and a specific data column in a CSV file, optionally ignoring specified columns.

    Parameters:
    - csv_file (str): Path to the source CSV file.
    - column_mappings (dict): A dictionary mapping existing column names to new column names.
    - data_mappings (dict): A dictionary mapping existing data values to new data values for a specific column.
    - column_to_modify (str): The name of the column whose data values are to be modified according to data_mappings. Pass None if no data mappings should be applied.
    - output_file (str): Path to the output CSV file where the modified data will be saved.
    - ignore_columns (list): A list of column names to be ignored (i.e., removed) from the source CSV file.

    Returns:
    None. The function will print the modified DataFrame to the console and save it to the specified output file.

    Raises:
    ValueError: If `column_to_modify` is specified but does not exist in the DataFrame after applying column name mappings.

    Example:
    Suppose we have a CSV file 'data.csv' with the following columns: ['ID', 'User Name', 'Signup Date'].
    We want to rename 'User Name' to 'username', remove the 'Signup Date' column, and transform all usernames to lowercase in the 'username' column.

    >>> column_mappings = {'User Name': 'username'}
    >>> data_mappings = {'JohnDoe': 'johndoe', 'JaneDoe': 'janedoe'}
    >>> ignore_columns = ['Signup Date']
    >>> apply_mappings('data.csv', column_mappings, data_mappings, 'username', 'modified_data.csv', ignore_columns)

    This will create 'modified_data.csv' with columns ['ID', 'username'], where 'username' values are transformed according to `data_mappings`, and 'Signup Date' column is removed.
    """
    # Validate the CSV delimiter
    try:
        validate_csv_delimiter(csv_file)
    except ValueError as e:
        print("Please ensure the CSV file is delimited with commas.")
        print(e)
        return  # Stop execution if the delimiter is not valid

    # Proceed with loading the data
    df = pd.read_csv(csv_file, encoding='utf-8')

    # Drop the columns that are to be ignored
    df.drop(columns=ignore_columns, errors='ignore', inplace=True)

    # Apply column name mappings
    df.rename(columns=column_mappings, inplace=True)

    # Apply data mappings if a specific column is specified
    if column_to_modify:
        if column_to_modify not in df.columns:
            raise ValueError(f"Column '{column_to_modify}' not found in the CSV file.")
        # Apply mapping, defaulting to original value if not found in data_mappings
        df[column_to_modify] = df[column_to_modify].apply(lambda x: data_mappings.get(x, x))

    # Save the modified DataFrame to a new CSV file
    df.to_csv(output_file, index=False)    
    print(f"Data successfully processed and saved to {output_file}")



def main():
    """
    Apply mappings from a YAML file to a CSV and output the modified data.
    
    Example:
    >>> python your_script_name.py path/to/your/data.csv path/to/your/mappings.yaml column_name_to_modify path/to/your/output.csv
    """
    parser = argparse.ArgumentParser(description='Apply mappings from a YAML file to a CSV and output the modified data.')
    parser.add_argument('csv_file', type=str, help='Path to the CSV file.')
    parser.add_argument('yaml_file', type=str, help='Path to the YAML mapping file.')
    parser.add_argument('column_to_modify', type=str, help='The specific column to apply data value mappings to.')
    parser.add_argument('output_file', type=str, help='Path where the modified CSV will be saved.')

    args = parser.parse_args()

    # Load mappings from the YAML file
    column_mappings, data_mappings = load_mappings(args.yaml_file)

    # Apply mappings and save the modified CSV
    apply_mappings(args.csv_file, column_mappings, data_mappings, args.column_to_modify, args.output_file)

    print("Data mapping complete. The modified data is saved to:", args.output_file)

if __name__ == '__main__':
    main()
