To run a new instance of a Docker Compose setup without overriding or affecting the current running containers from the same Docker Compose file, you'll need to use a different project name. Docker Compose uses the project name as a namespace to isolate environments, and by default, the project name is derived from the directory name where the `docker-compose.yml` file resides.

To specify a different project name, use the `-p` or `--project-name` option when you run Docker Compose. This way, you can have multiple instances of the same Docker Compose setup running independently.

Here’s how you do it:

### Running with a Different Project Name

1. **Navigate to the Directory**: Make sure you're in the directory containing your `docker-compose.dev.yaml`.

2. **Start Docker Compose with a Custom Project Name**:
   
   ```bash
   docker-compose -p custom_project_name -f docker-compose.dev.yaml up -d
   ```

   Replace `custom_project_name` with a name you choose. This name will be used as the project name, and it should be different from the name used by any currently running instances.

### Example

If you have a project running with the default project name (derived from the directory name) and you want to start a new instance without affecting the running one, you could do:

```bash
docker-compose -p myproject_v2 -f docker-compose.dev.yaml up -d
```

## Get in the docker container for the app to build the database

```bash
docker exec -it <container_name> sh
python manage.py makemigrations crudapp
python manage.py migrate
```

### Considerations

- **Port Conflicts**: If your `docker-compose` services expose ports (e.g., `80:80`), make sure to adjust these in the `.yaml` file for the new instance to avoid conflicts with the ports used by the already running instance.
- **Volume Conflicts**: Similarly, if your services use named volumes and you want to keep data separate between instances, you'll need to define different volume names for the new instance.
- **Network Conflicts**: If you have defined custom networks, ensure that there are no conflicts between the instances.

By following these steps, you can run multiple instances of the same Docker Compose setup simultaneously without them interfering with each other, maintaining separate environments for each instance.