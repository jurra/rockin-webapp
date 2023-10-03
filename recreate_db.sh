#!/bin/bash

# Load environment variables from .env file
export $(cat .env | xargs)

# Drop the Database
mysql -h $DB_HOST -u $DB_USER -p$DB_PASSWORD -e "DROP DATABASE IF EXISTS $DB_NAME;"

# Create a New Database
mysql -h $DB_HOST -u $DB_USER -p$DB_PASSWORD -e "CREATE DATABASE $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"