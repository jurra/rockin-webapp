# Exporting data and importing data in docker

### 1. **Export the Volume Data**
   - **Identify the Volume**: Determine the volume associated with your MySQL container.
     ```sh
     docker inspect container_id | grep -i volume
     ```
   - **Create a Backup of the Volume**: Use a temporary container to create a tarball of the volume data.
     ```sh
     docker run --rm --volumes-from container_id -v $(pwd):/backup ubuntu tar cvf /backup/volume_backup.tar /path/to/volume
     ```
     Replace `/path/to/volume` with the actual path where the MySQL data is stored in the container (e.g., `/var/lib/mysql`).

### 2. **Transfer the Volume Data to the Server**
   - **Copy the Tarball**: Transfer the created tarball to your server.
     ```sh
     scp volume_backup.tar user@server:/path/to/destination
     ```

### 3. **Load the Docker Image on the Server**
   - **Transfer Docker Image**: If you haven't already, transfer the Docker image to the server.
     ```sh
     docker save my_database_image > my_database_image.tar
     scp my_database_image.tar user@server:/path/to/destination
     ```
   - **Load Docker Image**: Load the Docker image on the server.
     ```sh
     docker load < /path/to/destination/my_database_image.tar
     ```

### 4. **Restore the Volume Data on the Server**
   - **Create a Volume on the Server**: Create a Docker volume on the server to store MySQL data.
     ```sh
     docker volume create my_database_volume
     ```
   - **Extract the Tarball**: Use a temporary container to extract the tarball into the created volume.
     ```sh
     docker run --rm -v my_database_volume:/path/to/volume -v /path/to/destination:/backup ubuntu bash -c "cd /path/to/volume && tar xvf /backup/volume_backup.tar --strip 1"
     ```

### 5. **Run the Container with the Restored Volume**
   - **Run the Docker Container**: Start the Docker container on the server using the restored volume.
     ```sh
     docker run -d --name my_database_container -e MYSQL_ROOT_PASSWORD=root_password -v my_database_volume:/path/to/volume my_database_image
     ```
     Replace `/path/to/volume` with the path where MySQL expects to find its data (e.g., `/var/lib/mysql`).

### Summary of Steps:
1. Create a tarball backup of the volume data from the source container.
2. Transfer the tarball to the destination server.
3. Create a Docker volume on the server.
4. Extract the tarball into the new volume.
5. Run the Docker container using the restored volume.

By following these steps, you ensure that the volume setup, along with all the data within it, is preserved during the migration process.


```bash
docker run --rm -v my_database_volume:/path/to/volume -v /path/to/destination:/backup ubuntu bash -c "cd /path/to/volume && tar xvf /backup/volume_backup.tar --strip 1"
```

### Command Breakdown

1. **`docker run`**:
   - This command is used to run a new Docker container.

2. **`--rm`**:
   - This option tells Docker to automatically remove the container when it exits. This helps to avoid leaving behind stopped containers that can clutter the system.

3. **`-v my_database_volume:/path/to/volume`**:
   - This option mounts the Docker volume `my_database_volume` to the container's filesystem at the path `/path/to/volume`.
   - `my_database_volume` is the name of the Docker volume.
   - `/path/to/volume` is the path inside the container where the volume will be mounted.

4. **`-v /path/to/destination:/backup`**:
   - This option mounts a host directory `/path/to/destination` to the container's filesystem at the path `/backup`.
   - `/path/to/destination` is the path on the host machine.
   - `/backup` is the path inside the container where this host directory will be mounted.

5. **`ubuntu`**:
   - This specifies the base image to use for the container. In this case, it uses the official Ubuntu image.

6. **`bash -c "cd /path/to/volume && tar xvf /backup/volume_backup.tar --strip 1"`**:
   - This part of the command tells the container to run a bash shell and execute the commands within the quotes.
   - `bash -c` runs the specified command string in a new bash shell.

### Inside the Bash Command

- **`cd /path/to/volume`**:
  - This changes the directory to `/path/to/volume` inside the container, which is the mount point for `my_database_volume`.

- **`&&`**:
  - This logical AND operator ensures that the next command (`tar xvf`) is only executed if the `cd` command is successful.

- **`tar xvf /backup/volume_backup.tar --strip 1`**:
  - `tar` is the command used to extract files from a tar archive.
  - `xvf` are options for the `tar` command:
    - `x`: Extract the files from the archive.
    - `v`: Verbosely list the files being processed.
    - `f`: Specifies the filename of the archive to extract.
  - `/backup/volume_backup.tar` is the path to the tar archive inside the container. This path corresponds to the host directory `/path/to/destination` mounted as `/backup` in the container.
  - `--strip 1` is an option for `tar` that removes the leading directory component from the file names in the archive before extracting. This means if the archive contains a directory structure, it will strip the top-level directory and extract the files and subdirectories directly into `/path/to/volume`.

### Summary

This command runs a temporary Docker container based on the Ubuntu image, mounts a Docker volume and a host directory into the container, and then extracts the contents of a tar archive from the host directory into the Docker volume. The container is removed automatically after the operation completes.


### Step 1: List Running Containers
First, identify the running containers and their IDs or names.

```bash
docker ps
```

### Step 2: Inspect the Container
Choose the container you are interested in (for example, `my_mysql_container`) and inspect it to find out the volume mounts.

```bash
docker inspect my_mysql_container
```

### Step 3: Locate Volume Information
In the JSON output from `docker inspect`, look for the `Mounts` section. This section provides details about the mounted volumes.

#### Using `jq` for Better Readability
If you have `jq` installed, you can filter the output to show only the `Mounts` section:

```bash
docker inspect my_mysql_container | jq '.[0].Mounts'
```

Example output might look like this:

```json
[
  {
    "Type": "volume",
    "Name": "my_database_volume",
    "Source": "/var/lib/docker/volumes/my_database_volume/_data",
    "Destination": "/path/to/volume",
    "Driver": "local",
    "Mode": "rw",
    "RW": true,
    "Propagation": ""
  },
  {
    "Type": "bind",
    "Source": "/path/to/destination",
    "Destination": "/backup",
    "Mode": "",
    "RW": true,
    "Propagation": "rprivate"
  }
]
```

### Step 4: Identify Paths
From the output, note down the following information:
- `my_database_volume` (volume name)
- `/path/to/volume` (container path for the volume)
- `/path/to/destination` (host path for the bind mount)
- `/backup` (container path for the bind mount)

### Step 5: Verify Host Paths
Ensure the paths on your host system exist and have the necessary permissions:
- `/path/to/destination`

If the directory doesn't exist, create it:

```bash
mkdir -p /path/to/destination
```

### Step 6: Prepare the Backup File
Ensure that the backup file `volume_backup.tar` exists in `/path/to/destination`. If not, place it there.

### Step 7: Run the Docker Command
Now you can run the command to restore the backup into the Docker volume:

```bash
docker run --rm -v my_database_volume:/path/to/volume -v /path/to/destination:/backup ubuntu bash -c "cd /path/to/volume && tar xvf /backup/volume_backup.tar --strip 1"
```

### Full Workflow Example
1. **List running containers**:

   ```bash
   docker ps
   ```

2. **Inspect the chosen container**:

   ```bash
   docker inspect my_mysql_container | jq '.[0].Mounts'
   ```

3. **Ensure host paths exist and are correct**:

   ```bash
   ls /path/to/destination
   ```

   If necessary, create the directory:

   ```bash
   mkdir -p /path/to/destination
   ```

4. **Place the backup file in the host directory**:

   ```bash
   cp /path/to/your/backup/volume_backup.tar /path/to/destination/
   ```

5. **Run the Docker command**:

   ```bash
   docker run --rm -v my_database_volume:/path/to/volume -v /path/to/destination:/backup ubuntu bash -c "cd /path/to/volume && tar xvf /backup/volume_backup.tar --strip 1"
   ```

By following these steps, you ensure that all necessary paths and files are correctly set up, and you can successfully run the Docker command to restore your volume from the backup tar file.


To perform the series of operations using Docker Compose, we will break down the steps and create the necessary Docker Compose files and scripts to achieve the same result. Here is a detailed plan to achieve this:

### Step 1: Export the Volume Data
We'll create a Docker Compose service to create a tarball of the volume data.

### Step 2: Transfer the Volume Data to the Server
We'll assume you can manually transfer the tarball file using `scp`.

### Step 3: Load the Docker Image on the Server
We'll assume you can manually transfer and load the Docker image using `docker save` and `docker load`.

### Step 4: Restore the Volume Data on the Server
We'll create a Docker Compose service to restore the tarball into the Docker volume on the server.

### Step 5: Run the Container with the Restored Volume
We'll create a Docker Compose service to run the container using the restored volume.

Here's how to do this step-by-step:

### Step 1: Create the Backup Tarball

**docker-compose.export.yml**:
```yaml
version: '3.8'

services:
  backup:
    image: ubuntu
    volumes:
      - my_database_volume:/var/lib/mysql  # Replace with actual path if different
      - ./backup:/backup
    command: bash -c "cd /var/lib/mysql && tar cvf /backup/volume_backup.tar ."
    # Run once and then stop
    restart: "no"

volumes:
  my_database_volume:
    external: true
```

**Command to run**:
```sh
docker-compose -f docker-compose.export.yml up
```

This creates a tarball of the volume data in the `./backup` directory on your host.

### Step 2: Transfer the Volume Data to the Server
Manually transfer `volume_backup.tar` to the destination server using `scp`:

```sh
scp ./backup/volume_backup.tar user@server:/path/to/destination
```

### Step 3: Load the Docker Image on the Server
Manually transfer and load the Docker image on the server:

```sh
docker save my_database_image > my_database_image.tar
scp my_database_image.tar user@server:/path/to/destination
ssh user@server "docker load < /path/to/destination/my_database_image.tar"
```

### Step 4: Restore the Volume Data on the Server

**docker-compose.restore.yml**:
```yaml
version: '3.8'

services:
  restore:
    image: ubuntu
    volumes:
      - my_database_volume:/var/lib/mysql  # Replace with actual path if different
      - /path/to/destination:/backup
    command: bash -c "cd /var/lib/mysql && tar xvf /backup/volume_backup.tar --strip 1"
    # Run once and then stop
    restart: "no"

volumes:
  my_database_volume:
    external: true
```

**Command to run**:
```sh
docker-compose -f docker-compose.restore.yml up
```

This extracts the tarball into the Docker volume on the server.

### Step 5: Run the Docker Container with the Restored Volume

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  my_database:
    image: my_database_image
    environment:
      MYSQL_ROOT_PASSWORD: root_password  # Replace with actual root password
    volumes:
      - my_database_volume:/var/lib/mysql  # Replace with actual path if different
    ports:
      - "3306:3306"  # Replace with actual ports if different
    restart: always

volumes:
  my_database_volume:
    external: true
```

**Command to run**:
```sh
docker-compose up -d
```

This starts the MySQL container with the restored volume.

### Summary of Commands:

1. **Create the backup tarball**:
   ```sh
   docker-compose -f docker-compose.export.yml up
   ```

2. **Transfer the tarball to the server**:
   ```sh
   scp ./backup/volume_backup.tar user@server:/path/to/destination
   ```

3. **Transfer and load the Docker image on the server**:
   ```sh
   docker save my_database_image > my_database_image.tar
   scp my_database_image.tar user@server:/path/to/destination
   ssh user@server "docker load < /path/to/destination/my_database_image.tar"
   ```

4. **Extract the tarball into the volume on the server**:
   ```sh
   docker-compose -f docker-compose.restore.yml up
   ```

5. **Run the MySQL container**:
   ```sh
   docker-compose up -d
   ```

By following these steps, you can export, transfer, and restore the Docker volume data, and then run the Docker container using Docker Compose.