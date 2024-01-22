To connect to a MySQL database running in a Docker container on a remote server using MySQL Workbench, you will need to set up a secure connection, typically via an SSH tunnel. This approach allows you to connect to the database without exposing the MySQL port to the internet.

Here are the steps to connect to the remote MySQL database:

### 1. Ensure the MySQL Container is Running

Verify that the MySQL service is running on the remote server with Docker Compose:

```bash
docker-compose up -d
```

### 2. Set Up SSH Access

Ensure you have SSH access to the remote server. You'll use SSH to create a secure tunnel to the server.

### 3. Create an SSH Tunnel

On your local machine, create an SSH tunnel that forwards a local port to the MySQL port on the remote server:

```bash
ssh -L 3308:localhost:3308 -N -f -l <username> <remote_server_ip>
```
It worked in the context of the tudelft by providing the server domain instead of the ip address.

- `ssh`: This is the command used to start an SSH (Secure Shell) session, which allows secure access to a remote machine.

- `-L 3307:localhost:3306`: This option is setting up port forwarding.
    - `3307`: This is the local port on your machine. When you connect to this port, the connection will be forwarded to the specified destination.
    - `localhost:3306`: This is the destination of the port forward. In this case, you're forwarding to port `3306` on `localhost` as understood from the perspective of the remote server. `localhost` here refers to the remote server itself. Port `3306` is typically the default port for MySQL, so this setup is often used to securely connect to a remote MySQL database.
    
- `-N`: This option tells SSH that no remote commands will be executed, and it's used when the SSH session is only needed for port forwarding. This won't open a remote shell or command prompt.

- `-f`: This option tells SSH to go into the background, which means it won't occupy your command prompt or terminal window after the command is executed. The SSH session continues to run in the background.

- `-l <username>`: This option specifies the username to log in as on the remote server. Replace `<username>` with the actual username you use for the SSH connection.

- `<remote_server_ip>`: This is the IP address or hostname of the remote server to which you're establishing the SSH connection. Replace `<remote_server_ip>` with the actual IP address or hostname of your server.

In essence, this command establishes an SSH connection to `<remote_server_ip>` using the specified `<username>`, sets up a tunnel that forwards any connections made to port `3307` on your local machine to port `3306` on the remote server, and runs this SSH session in the background. This is a common technique for securely accessing a remote service (like MySQL) that isn't exposed directly to the internet.

### 4. Configure MySQL Workbench

Open MySQL Workbench and create a new connection:

1. Click the "+" icon next to "MySQL Connections".
2. In the "Setup New Connection" dialog:
   - **Connection Name**: Enter a descriptive name (e.g., "Remote Docker MySQL").
   - **Connection Method**: Choose "Standard (TCP/IP)".
   - **Hostname**: Enter `127.0.0.1` (since you're connecting via the SSH tunnel).
   - **Port**: Enter `3307` (the local port you're forwarding).
   - **Username**: Enter the MySQL username (value of `${DB_USER}` in your `.env` file).
   - **Password**: Click "Store in Vault" and enter the MySQL password (value of `${DB_PWD}` in your `.env` file).

3. Click "Test Connection" to verify the settings. If successful, save the connection.

### 5. Connect and Interact with the Database

Now you can use MySQL Workbench to interact with the MySQL database as if it were running locally on your machine.

### 6. Security Considerations

- Do not expose the MySQL port (3306) directly to the internet. The SSH tunnel provides a secure way to access it.
- Ensure that your MySQL user permissions and passwords are secure.
- Regularly update and patch your server and Docker images.

### 7. Troubleshooting

If you encounter issues:
- Check that the SSH tunnel is correctly established.
- Verify that the MySQL container is running on the remote server.
- Ensure there are no firewalls blocking the SSH or MySQL ports.
- Check that the MySQL user has the correct permissions.

By following these steps, you can securely connect to a MySQL database running in a Docker container on a remote server using MySQL Workbench.