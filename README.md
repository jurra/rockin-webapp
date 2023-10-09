# Rockin
Status: In development

Welcome to the Django app designed to manage data of cores extracted from wells. With this app, you can capture data from wells, including core catchers, core chips, cuttings and micro-chips. The app is designed to work with a SQL database backend. Whether you are a geologist, drilling engineer, or simply interested in well and core data, this app is a solution that can help in managing your information efficiently and effectively.

## Usage


## Develop notes
Migrate with django after updating the model:
```
(env)$ python manage.py makemigrations
(env)$ python manage.py migrate
```

Run server:
```
(env)$ python manage.py runserver
```

## Troubleshooting and testing
When running tests reuse the database. This will avoid having the database existing related error.
```
pytest --reuse-db
```

## Production and server management notes
```
sudo docker-compose up -d --build
```
