FROM ubuntu:22.04

# Install SSH server, python and venv
RUN apt-get update && apt-get install -y openssh-server python3 python3-pip python3-venv

# Create a directory for the SSH daemon
RUN mkdir /var/run/sshd

# Set a password for the root user (for demonstration purposes)
# In a real-world scenario, you should use SSH keys for authentication.
RUN echo 'root:ansible' | chpasswd

# Permit root login with password
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Create a virtual environment and install ansible
RUN python3 -m venv /opt/venv
RUN /opt/venv/bin/pip install ansible ansible-lint

# Add venv to the PATH
ENV PATH="/opt/venv/bin:$PATH"

# Expose port 22 for SSH
EXPOSE 22

# Start the SSH daemon
COPY host-entrypoint.sh /usr/local/bin/
ENTRYPOINT ["host-entrypoint.sh"]