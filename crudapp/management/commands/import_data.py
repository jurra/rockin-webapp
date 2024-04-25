'''
Ussage example:
>>> column_mappings, data_mappings = load_mappings('path_to_mapping.yaml')
>>> apply_mappings('path_to_input.csv', column_mappings, data_mappings, 'target_data_column', 'path_to_output.csv')
'''
import os
import pandas as pd
import yaml
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
        print(mappings.get('column_mappings'))
        df = pd.read_csv(csv_file, encoding='utf-8')
        df.rename(columns=mappings.get('column_mappings'), inplace=True)
        
        print(f"Importing data from {csv_file} to {model_name} model...")
        print(df)

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
        # Print current working directory
        with open(filename, 'r') as file:
            return yaml.safe_load(file)

    def import_data_to_model(self, dataframe, model):
        """
        Import data into the specified Django model.

        This function iterates over each row in the provided DataFrame, converting 
        it to a dictionary. It handles ForeignKey relationships, specifically for 
        the 'registered_by' field which is expected to be a ForeignKey to the User model.

        Args:
            dataframe (pd.DataFrame): The DataFrame containing the data to import.
            model (django.db.models.Model): The Django model class to which the data will be imported.
        """
        instances = []  # List to hold instances of the model for bulk creation
        print(dataframe)
        for row in dataframe.to_dict(orient='records'):
            # Set the date:time of login for Today
            row['last_login'] = timezone.now() # We need to set this field to a valid value, and it is not present in the CSV

            row.setdefault('last_login', ) # We don't have this data in the CSV, therefore we set it to None
            if 'well' in row and row['well'] is not None:
                try:
                    insert_well_in_row(row, 'well', get_well_by_name(row['well']))
                except e:
                    print('Thre was an issue with inserting the well object in the dataframe')

            # Handle ForeignKey for 'registered_by' field
            if 'registered_by' in row and row['registered_by'] is not None:
                try:
                    # Fetch the User instance associated with the ID in 'registered_by'
                    user_instance = User.objects.get(pk=row['registered_by'])
                    row['registered_by'] = user_instance  # Assign the User instance to the row
                except User.DoesNotExist:
                    # If a User with the given ID doesn't exist, handle the error
                    print(f"User with ID {row['registered_by']} not found.")
                    continue  # Skip this row and continue with the next one
            
            # Create an instance of the model using the row data
            instances.append(model(**row))
        
        try:
            # Bulk create instances in the database
            print(f"Creating {len(instances)} instances of {model.__name__}...")
            print (instances)
            model.objects.bulk_create(instances)
        except Exception as e:
            print(f"An error occurred: {e}")
            raise