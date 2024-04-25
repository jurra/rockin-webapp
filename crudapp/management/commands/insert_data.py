import sys
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from django.db import transaction

class Command(BaseCommand):
    ''' Usage of the command:
    python manage.py insert_data crudapp.Well
    
    '''
    help = 'Dynamically inserts data into any specified model. Usage: python manage.py insert_data crudapp.Well'

    def add_arguments(self, parser):
        parser.add_argument('model', type=str, help="Model name to insert data into (e.g., 'appname.ModelName')")

    def handle(self, *args, **options):
        # Get model from user input
        try:
            app_label, model_name = options['model'].split('.')
            model = apps.get_model(app_label, model_name)
        except (ValueError, LookupError) as e:
            raise CommandError(f"Model '{options['model']}' not found.")

        # Gather field data from user
        data = {}
        for field in model._meta.fields:
            # Skip auto-created fields
            if field.auto_created or field.is_relation:
                continue
            value = input(f'Enter value for {field.name} ({field.get_internal_type()}): ')
            data[field.name] = field.to_python(value)

        # Confirm before save
        self.stdout.write(self.style.WARNING('Please review the entered data:'))
        for key, value in data.items():
            self.stdout.write(f'{key}: {value}')

        confirm = input('Save this data? [yes/no]: ')
        if confirm.lower() == 'yes':
            try:
                with transaction.atomic():
                    obj = model(**data)
                    obj.save()
                    self.stdout.write(self.style.SUCCESS(f'Successfully added {model_name} instance.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to add data: {e}'))
        else:
            self.stdout.write(self.style.NOTICE('Cancelled entry.'))
