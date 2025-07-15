# Ansible Docker Test Environment

This project provides a self-contained environment for testing Ansible playbooks against multiple host machines simulated using Docker containers. It includes an Ansible control node and three target hosts, all configured for passwordless SSH access via RSA keys.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

*   **Docker**: [Install Docker Desktop](https://www.docker.com/products/docker-desktop)
*   **Docker Compose**: Usually comes bundled with Docker Desktop.
*   **Make**: A build automation tool, typically pre-installed on Linux/macOS.

## Environment Setup

1.  **Build and Run Docker Containers**:
    Navigate to the project root directory and run the following command to build the Docker images and start the containers in detached mode:
    ```bash
    docker-compose up -d --build
    ```
    This will create four containers:
    *   `ansible-control-node`: Your Ansible controller.
    *   `host1`, `host2`, `host3`: The target hosts for your Ansible playbooks.

2.  **Access the Ansible Control Node**:
    To run Ansible commands, you need to execute them from within the `ansible-control-node` container. Use the following command to get a bash shell inside it:
    ```bash
    docker-compose exec ansible-control-node /bin/bash
    ```
    Once inside, you will be in the `/ansible` directory, which is a mounted volume of your project root, so your playbooks and inventory files will be accessible.

3.  **Makefile Commands**:
    *   `make setup`: This command will print instructions on how to activate the Python virtual environment for Ansible on your local machine. (Note: This does not activate the venv inside the Docker container).
    *   `make clean`: This command will remove the `.venv` directory (the local Python virtual environment).

## Ansible Inventory (`inventory.ini`)

The `inventory.ini` file is configured to allow the `ansible-control-node` to connect to the host containers using their internal Docker network IP addresses:

```ini
[myhosts]
192.0.2.50
192.0.2.51
192.0.2.52
```

## Example Playbook (`playbook.yml`)

A simple example playbook is provided to test connectivity and basic Ansible functionality:

```yaml
- name: A simple playbook
  hosts: localhost
  connection: local
  tasks:
    - name: Print a message
      ansible.builtin.debug:
        msg: "Hello, Ansible!"
```

To run this playbook from within the `ansible-control-node` container:

```bash
ansible-playbook -i inventory.ini playbook.yml
```

## SSH Key Authentication

This setup automatically configures passwordless SSH access from the `ansible-control-node` to `host1`, `host2`, and `host3` using RSA key pairs. Here's how it works:

1.  **Key Generation**: When the `ansible-control-node` starts, it generates an SSH RSA key pair (`id_rsa` and `id_rsa.pub`) if one doesn't already exist.
2.  **Public Key Sharing**: The public key (`id_rsa.pub`) is shared with all host containers via a shared Docker volume (`ssh_key`).
3.  **Key Authorization**: Each host container's entrypoint script automatically adds this public key to its `/root/.ssh/authorized_keys` file.

This allows Ansible to connect to the hosts without requiring a password, streamlining your automation tasks.

## Troubleshooting and Notes

*   If you make changes to the `Dockerfile` or `docker-compose.yml`, remember to rebuild your containers using `docker-compose up -d --build`.
*   The `root` user on the host containers has a password `ansible` for direct SSH access (e.g., `ssh root@localhost -p 2222`), but Ansible will use key-based authentication.
*   Direct `ping` to container IPs from your macOS host is generally not possible due to Docker's networking on macOS. Use `docker-compose exec` to interact with the containers.
