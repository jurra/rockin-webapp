# Setting up development environment with Docker containers
We can either run mysql server locally as a process, or we can run it in a docker container. The latter is the preferred way, as it is easier to setup and manage using docker-compose. Alternatively we could have a bash script that starts the mysql container. However the latter is not implemented yet.

## Considerations for current setup
For testing the user has to enter the container interactively and grant priveleges like this example:
```bash
docker exec -it <container_name> mysql -u root -p

# This is the mysql prompt inside the container
mysql -u root -p
mysql> GRANT ALL PRIVILEGES ON test_myrockdb.* TO '<user_name>'@'%';
mysql> FLUSH PRIVILEGES;
```

