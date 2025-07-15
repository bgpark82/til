#!/bin/sh

# Path to the SSH key
SSH_KEY_PATH="/root/.ssh/id_rsa"

# Generate SSH key if it doesn't exist
if [ ! -f "$SSH_KEY_PATH" ]; then
  echo "Generating SSH key..."
  ssh-keygen -t rsa -b 4096 -f "$SSH_KEY_PATH" -N ""
fi

# Keep the container running
tail -f /dev/null
