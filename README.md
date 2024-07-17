# Rockin
Status: Discontinued

## Overview

Rockin was a Django-based project designed to manage data of cores extracted from wells, including core catchers, core chips, cuttings, and micro-chips. Initially intended to develop a full-stack application for geologists and drilling engineers, the project has been scaled down due to time limitations. The final outcome includes a Django ORM-based data model for a MySQL database and scripts to migrate data from Microsoft Access to MySQL. An intermediate solution allows using Microsoft Access as a frontend client connected to a remote MySQL database.

## Project Outcomes

1. **Django ORM-based Data Model**:
   - Developed a new data model using Django ORM to replicate the structure of the current Access database.
   - The data model is ready for use with a MySQL database, providing a robust foundation for future expansion.

2. **Data Migration Scripts**:
   - Created scripts to facilitate the migration of data from the Access database to the new MySQL database.
   - Ensured data integrity and consistency during the migration process.

3. **Intermediate Solution: Reusing Microsft Access as a frontend**:
   - Established a method for connecting Microsoft Access as a frontend client to a MySQL database hosted remotely.
   - This solution allows continued use of familiar Access forms while leveraging the capabilities of a robust MySQL backend.

## Discontinued features

1. Interactive forms for data entry and editing.All forms are implemented to enter data, but data retrieving, presentation and editing are missing and this is essential for the application to be viable.

## Usage

### Production and Server Management

To build and run the server using Docker, execute:

```bash
sudo docker-compose up -d --build
```

## Running the Database in a Container

To run the database in a Docker container, you need to apply the migrations first. This is specified in the `docker-compose.yaml` file at line 24. The application itself does not need to be run for the database to be functional.

### Applying Migrations in Docker

To apply migrations and set up the database, follow these steps:

1. **Build and Run Docker Compose**:
   - Navigate to the project directory containing the `docker-compose.yaml` file.
   - Run the following command to build and start the containers:
     ```bash
     docker-compose up -d --build
     ```

#### Troubleshooting
You can access interactive the container running the database to make sure the migrations are applied correctly.
2. **Access the Application Container**:
   - Identify the running database container:
     ```bash
     docker ps
     ```
   - Access the container's shell:
     ```bash
      docker exec -it <db_container_name> mysql -u root -p

     ```

3. **Run Migrations if not applied when running docker-compose**:
   Identify the running application container:
     ```bash
     docker ps
     ```
   - Access the application container's shell:
      ```bash
      docker exec -it <app_container_name> bash
      ```
   - Inside the container, run the migration commands:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```
### Data loading from exported Access data to MySQL using django

To load data exported from Microsoft Access as csv files to MySQL, follow the detailed procedure in the `crudapp/mannagement/commands` directory. Ensure all prerequisites are met and follow the instructions step by step. In order for csv table to be migrated first columns need to be renamed and checked to match the django ORM requirements in the model.

There is plenty of documentation in the scripts to guide you through the process.

#### Usage of the command to migrate data
This command will import data from a CSV file into the targeted database. The command requires the path to the CSV file, the model name, and the path to the mappings file.
```bash
python manage.py import_data path/to/csv.csv ModelName path/to/mappings.yaml
```
### Connecting Microsoft Access to a Remote MySQL Database
To connect your Microsoft Access application to an external MySQL database hosted on a server:

1. **Install MySQL ODBC Driver**:
   - Download and install the MySQL ODBC driver from the MySQL website: [MySQL Connector/ODBC](https://dev.mysql.com/downloads/connector/odbc/).

2. **Set Up System DSN**:
   - Open the ODBC Data Source Administrator and set up a new System DSN for the MySQL database.

3. **Link Tables in Access**:
   - Open Access, go to the "External Data" tab, and use the "ODBC Database" option to link to the MySQL database.
   - Select the System DSN created in the previous step and link the desired tables.

For detailed steps, refer to the documentation in the `docs` directory.

This setup allows you to run the database locally or on a server, enabling continued use of the application if someone decides to reactivate the project.

## Future Prospects

Although the full-stack application was not completed, the following components are reusable for future development:

1. **Django Data Model**:
   - The ORM-based data model can serve as the foundation for further application development.

2. **Data Migration Documentation**:
   - Detailed procedures and scripts for migrating data from Access to MySQL can be reused or adapted for similar projects.

3. **Access-MySQL Connection Guide**:
   - The guide for connecting Access to a remote MySQL database provides a practical intermediate solution for data management.

By leveraging these components, future developers can build upon the existing work to create a comprehensive solution for managing well core data.

