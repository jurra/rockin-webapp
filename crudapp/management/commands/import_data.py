'''
Ussage example:
>>> column_mappings, data_mappings = load_mappings('path_to_mapping.yaml')
>>> apply_mappings('path_to_input.csv', column_mappings, data_mappings, 'target_data_column', 'path_to_output.csv')
'''
import os
import pandas as pd
import yaml
from datetime import datetime
import pytz

from django.core.management.base import BaseCommand

from django.contrib.auth.models import User
from crudapp import models as app_models
from crudapp.management.commands.mappings import load_mappings, apply_mappings
from django.utils import timezone

def get_well_by_name(well_name):
    '''Define a function that when it finds a well name, fetch the id of the well from the database,
    the Well object in django ORM style
    '''
    # Fetch the well from the database
    try:
        well = app_models.Well.objects.get(name=well_name)
        return well
    except app_models.Well.DoesNotExist:
        print(f"Well with name {well_name} not found.")
        return None

def insert_well_in_row(row, well_column, well_object):
    ''' Replace well column value with well object
    '''
    # Split the line into multiple lines using string concatenation
    row[well_column] = well_object

def convert_date_format(date_str):
    # Attempt to convert from 'MM/DD/YY HH:MM PM', 'MM/DD/YY', and 'DD/MM/YY HH:MM PM', 'DD/MM/YY' to 'YYYY-MM-DD HH:MM:SS+TZ' format
    formats = [
        '%m/%d/%y %I:%M %p',  # MM/DD/YY HH:MM PM
        '%m/%d/%y',           # MM/DD/YY
        '%d/%m/%y %I:%M %p',  # DD/MM/YY HH:MM PM
        '%d/%m/%y'            # DD/MM/YY
    ]
    for format_str in formats:
        try:
            # Attempt to parse the date string with the current format
            parsed_date = datetime.strptime(date_str, format_str)
            # Make the datetime object timezone aware
            aware_date = timezone.make_aware(parsed_date, timezone.get_default_timezone())
            # Return the date in the desired format with timezone information
            return aware_date.strftime('%Y-%m-%d %H:%M:%S%z')
        except ValueError:
            # If the current format does not match, continue to try the next format
            continue
    # If none of the formats matched, log an error message
    print(f"Error converting date: Date format not recognized for '{date_str}'")
    return None

def process_row(row, model):
    # Modify or set default values
    row = {k: v if pd.notnull(v) else None for k, v in row.items()}

    # Convert date fields to the appropriate format
    date_fields = [key for key in row.keys() if '_date' in key]  # Handles any field that ends with '_date'
    for field in date_fields:
        if row[field] is not None:
            formatted_date = convert_date_format(row[field])
            if formatted_date:
                row[field] = formatted_date
            else:
                print(f"Date format error for field {field} with value {row[field]}")

    # Foreign key handling for 'well' and 'registered_by' fields
    if 'well' in row and row['well']:
        try:
            row['well'] = get_well_by_name(row['well'])
            print(f"Well object: {row['well']}")
        except Exception as e:
            print(f"There was an issue with inserting the well object: {e}")
            row['well'] = None
    
    # Handle ForeignKey for 'registered_by'
    if 'registered_by' in row and row['registered_by']:
        try:
            row['registered_by'] = User.objects.get(username=row['registered_by'])
            print("User object: ", row['registered_by'])
        except User.DoesNotExist:
            print(f"User with username {row['registered_by']} not found.")
            row['registered_by'] = None
    # Create and yield a model instance
    try:
        instance = model(**row)
        yield instance
    except Exception as e:
        print(f"Error saving instance: {e}")

class Command(BaseCommand):
    """
    A Django management command to import data from a CSV file into a specified Django model.

    This command allows for the dynamic import of data into any specified model within
    the Django app. It requires a CSV file with the data, the name of the target model,
    and a YAML file that maps CSV column names to model field names.

    The command reads and transforms the data from the CSV file according to the provided
    mappings, and then it creates and saves instances of the specified model.

    Arguments:
        csv_file (str): Path to the CSV file containing the data to be imported.
        model_name (str): Name of the Django model into which data will be imported.
        mapping_file (str): Path to the YAML file that contains column-to-field mappings.

    Usage:
        python manage.py import_data path/to/csv.csv ModelName path/to/mappings.yaml

    Example:
        python manage.py import_data my_data.csv MyModel column_mappings.yaml

    The YAML file should contain mappings in the following format:
        csv_column_name1: model_field_name1
        csv_column_name2: model_field_name2
        ...
    """

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
        parser.add_argument('model_name', type=str, help='Model name to import data into')
        parser.add_argument('mapping_file', type=str, help='Path to the YAML mapping file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        model_name = kwargs['model_name']
        mapping_file = kwargs['mapping_file']

        mappings = self.load_column_mappings(mapping_file)
        
        df = pd.read_csv(csv_file, encoding='utf-8', delimiter=',')
        df.rename(columns=mappings.get('column_mappings'), inplace=True)
        
        print(f"Importing data from {csv_file} to {model_name} model...")

        model = getattr(app_models, model_name)
        self.import_data_to_model(df, model)

    def load_column_mappings(self, filename):
        """
        Load column mappings from a YAML file.

        Args:
            filename (str): Path to the YAML file.

        Returns:
            dict: A dictionary containing the column mappings.
        """
        print('Loading column mappings from YAML file...')
        with open(filename, 'r') as file:
            return yaml.safe_load(file)

    def import_data_to_model(self, dataframe, model):
        """
        Import data into the specified Django model using a generator to optimize memory usage and handle large datasets efficiently.
        
        Args:
            dataframe (pd.DataFrame): The DataFrame containing the data to import.
            model (django.db.models.Model): The Django model class to which the data will be imported.
        """
        for index, row in dataframe.iterrows():
            print(f"Processing row ...")
            print(row)
            instance_generator = process_row(row, model)
            for instance in instance_generator:
                try:
                    instance.save()
                    print(f"Saved: {instance}")
                except Exception as e:
                    print(f"Error saving instance: {e}")
