# Dev notes

## Create a new database to test the app
```
>>> python manage.py migrate
>>> python manage.py makemigrations
```
## Create a super user with django
To create a superuser in Django, you can use the built-in `createsuperuser` management command. This command will prompt you to enter a username, email, and password for the superuser account. Here's how you can do it:

1. Open a terminal/command prompt.

2. Navigate to your Django project directory (the one containing `manage.py`).

3. Run the following command:

   ```
   python manage.py createsuperuser
   ```

4. You will be prompted to enter a username, email address, and password for the superuser.

5. After entering the required information, the superuser account will be created.

Here's an example of what the command and prompts might look like:

```
$ python manage.py createsuperuser
Username: admin
Email address: admin@example.com
Password: **********
Password (again): **********
Superuser created successfully.
```

Once you've created the superuser, you can use the provided credentials to log in to the Django admin interface with administrative privileges.

Keep in mind that the `createsuperuser` command is part of Django's authentication system and assumes you have already set up a database and configured authentication settings.

## Create a user with mysql to setup the database
To create a new user in MySQL, you can use the `CREATE USER` statement. Here's the general syntax:

```sql
CREATE USER 'username'@'hostname' IDENTIFIED BY 'password';
```

- `'username'` is the name you want to give to the user.
- `'hostname'` specifies from where the user is allowed to connect. You can use `'%'` as a wildcard to allow connections from any host, or you can specify a specific IP address or hostname.
- `'password'` is the password you want to set for the user.

For example, to create a user named "myuser" with a password "mypassword" that can connect from any host, you can use:

```sql
CREATE USER 'myuser'@'%' IDENTIFIED BY 'mypassword';
```

After creating the user, you might also want to grant appropriate privileges to the user on specific databases or tables. You can use the `GRANT` statement for that purpose. For example, to grant all privileges on a specific database to the user:

```sql
GRANT ALL PRIVILEGES ON databasename.* TO 'myuser'@'%';
```

Don't forget to flush the privileges after making changes:

```sql
FLUSH PRIVILEGES;
```

Keep in mind that creating users and managing their privileges may require administrative rights on the MySQL server. Be cautious when assigning privileges to users, as granting excessive permissions can pose security risks.