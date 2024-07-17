# Connect Access Frontend to a remote SQL Database
## Getting started
To connect your Microsoft Access application to an external SQL database hosted on a server, you can follow these general steps:

1. **Identify Database Provider**: Ensure that your Access application supports the type of SQL database you're trying to connect to (e.g., SQL Server, MySQL, PostgreSQL).

2. **Install Necessary Drivers**: Install any necessary ODBC (Open Database Connectivity) or OLE DB drivers required to connect to the specific type of SQL database you're using. You may need to download and install these drivers from the database vendor's website.

3. **Configure ODBC Data Source (Optional)**: You can set up an ODBC data source on your machine to establish a connection to the SQL database. This step is optional, as Access can also connect directly using connection strings without creating a data source.

4. **Open Access Database**: Launch your Microsoft Access application and open the database that you want to connect to the SQL database.

5. **External Data Tab**: In the Access ribbon, go to the "External Data" tab.

6. **Choose Data Source**: Click on "ODBC Database" or "ODBC Database" depending on your version of Access.

7. **Select Data Source**: In the "Get External Data - ODBC Database" wizard, select the option to link to the data source by creating a linked table. Click "OK".

8. **Select Data Source Window**: In the "Select Data Source" window, choose the appropriate ODBC data source that you have configured or select "New Data Source" to create a new one.

9. **Configure Connection**: Follow the prompts to configure the connection to your SQL database. You'll need to provide connection details such as server name, database name, authentication credentials, etc.

10. **Select Tables**: After successfully connecting to the SQL database, you'll be presented with a list of tables/views available in the database. Select the tables/views that you want to link to your Access database.

11. **Finish**: Complete the wizard, and Access will create linked tables in your database that correspond to the selected tables/views in the SQL database.

12. **Verify Connection**: Verify that the linked tables are properly connected to the SQL database by checking if you can view the data in those tables within Access.

By following these steps, you should be able to connect your Microsoft Access application to an external SQL database hosted on a server. Remember to ensure that you have the necessary permissions and network access to connect to the remote database.

## Detailed procedure for MySQL
To connect to the MySQL database running in a Docker container on a remote server using Microsoft Access, you can use ODBC (Open Database Connectivity). Here's how you can set it up:

1. **Install MySQL ODBC Driver**:
   First, you need to install the MySQL ODBC driver on your local machine. You can download it from the MySQL website: [MySQL Connector/ODBC](https://dev.mysql.com/downloads/connector/odbc/).

2. **Set Up System DSN**:
   - Open the ODBC Data Source Administrator on your local machine. You can find it in the Control Panel under Administrative Tools or by searching for "ODBC Data Sources" in the Windows search bar.
   - Go to the "System DSN" tab and click "Add".
   - Choose the MySQL ODBC Driver from the list and click "Finish".
   - Configure the Data Source Name (DSN), description, MySQL server IP address or hostname, port (3308 in this case), MySQL database name, username, and password.
   - Test the connection to ensure it's successful, then click "OK" to save the DSN.

3. **Link Tables in Access**:
   - Open Microsoft Access.
   - Create a new blank database or open an existing one.
   - Go to the "External Data" tab and click "ODBC Database" in the "Import & Link" group.
   - In the "Get External Data - ODBC Database" dialog, choose "Link to the data source by creating a linked table" and click "OK".
   - In the "Select Data Source" dialog, choose the System DSN you created earlier and click "OK".
   - Enter the MySQL username and password when prompted.
   - Select the tables you want to link to Access and click "OK".
   - Access will create linked tables that directly reference the data in the MySQL database. You can interact with these tables in Access as if they were local tables.

4. **Accessing the Data**:
   - Once the linked tables are created, you can use Access to query, update, and manipulate the data just like any other Access table.
   - You can create forms, reports, and queries using the linked tables to analyze and work with the data from the MySQL database.

By following these steps, you can establish a connection from Microsoft Access to the MySQL database running in a Docker container on a remote server using ODBC. This allows you to seamlessly integrate the data from the MySQL database into your Access application.
