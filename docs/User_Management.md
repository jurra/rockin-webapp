# User management
## Creating a user manually within a container
For this you ha
```sh
docker ps # list all running containers to get the name of the container 
docker exec -it <container_name> bash
python manage.py createsuperuser
```

## Creating a user with a django script
### Example 1
To create a user via `python manage.py`, you'll often use the built-in command `createsuperuser` to create an admin user. However, if you want to automate user creation using a custom management command, follow these steps:

1. **Create a Custom Management Command**:

   First, decide which Django app you'd like to add this command to. For this example, I'll use an app named `accounts`. You can replace it with the name of one of your apps.

   Within your app directory (`accounts` in our example), create a new directory structure for the management command:

   ```
   your_project/
   ├── accounts/
   │   ├── management/
   │   │   ├── __init__.py
   │   │   ├── commands/
   │   │   │   ├── __init__.py
   │   │   │   ├── createuser.py
   ```

2. **Write the Custom Command**:

   Inside `createuser.py`, place the following code:

   ```python
   from django.core.management.base import BaseCommand, CommandError
   from django.contrib.auth.models import User

   class Command(BaseCommand):
       help = 'Create a new user'

       def add_arguments(self, parser):
           parser.add_argument('username', type=str, help='Username for the new user')
           parser.add_argument('email', type=str, help='Email for the new user')
           parser.add_argument('password', type=str, help='Password for the new user')

       def handle(self, *args, **kwargs):
           username = kwargs['username']
           email = kwargs['email']
           password = kwargs['password']

           try:
               user = User.objects.create_user(username=username, email=email, password=password)
               user.save()
               self.stdout.write(self.style.SUCCESS(f"Successfully created user {username}"))
           except Exception as e:
               raise CommandError(f"Error creating user: {str(e)}")
   ```

3. **Use the Command**:

   Now, you can use the new management command as follows:

   ```bash
   python manage.py createuser sample_username sample@email.com sample_password
   ```

   If everything is set up correctly, you should see a success message indicating that the user has been created.

**Note**: This command will create regular users. If you want to create superusers, you can modify the command logic accordingly using `User.objects.create_superuser(...)`. As always, ensure sensitive operations are conducted securely and handle potential exceptions that may arise from user creation.



### Example 2
To create a user in Django from a Python script, you can use Django's built-in User model. Here's a simple script that demonstrates how to create a user:

1. **Setting up the environment**:
   Before running any script that uses Django's ORM, you need to set up the Django environment by initializing the settings module.

2. **Use the User model to create a user**:
   Use the `create_user` helper method available on the User model to create a user.

Here's the script:

```python
import os
import django

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
django.setup()

# Now that the environment is set up, you can import the User model
from django.contrib.auth.models import User

def create_user(username, email, password):
    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()
    print(f"User {username} created successfully!")

if __name__ == "__main__":
    create_user('sample_username', 'sample@email.com', 'sample_password')
```

Replace `'your_project_name.settings'` with the actual path to your Django project's settings module.

After creating the script:

1. Activate your Django virtual environment:

    ```bash
    source your_virtual_env/bin/activate  # For Unix-based systems
    ```

    ```bash
    your_virtual_env\Scripts\activate  # For Windows
    ```

2. Run the script:

    ```bash
    python your_script_name.py
    ```

Ensure you have all the necessary dependencies installed in the virtual environment where you run this script, especially Django and the database drivers for your chosen database backend.

**Caution**: This is a basic example. In a real-world scenario, make sure to handle exceptions and include additional logic as required. Also, avoid hardcoding sensitive data like passwords directly in scripts.