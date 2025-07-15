#!/bin/sh

# Path to the authorized_keys file
AUTHORIZED_KEYS_FILE="/root/.ssh/authorized_keys"

# Create the .ssh directory if it doesn't exist
mkdir -p /root/.ssh

# Add the public key to authorized_keys
cat /ssh_key/id_rsa.pub >> "$AUTHORIZED_KEYS_FILE"

# Start the SSH daemon
/usr/sbin/sshd -D
