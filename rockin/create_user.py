'''
A script for development purposes to create a user in the database.
'''
import os
import django
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Set up Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# Get user details from environment variables
username = os.getenv("DJANGO_USERNAME")
email = os.getenv("DJANGO_EMAIL")
password = os.getenv("DJANGO_PASSWORD")

# Delete user
try:
    user = User.objects.get(username=username)
    user.delete()
    print(f"User {username} has been deleted.")
except ObjectDoesNotExist:
    print(f"No user found with username: {username}")

# Create user
user = User.objects.create_user(username, email, password)
user.save()
print(f"User {username} has been created.")
