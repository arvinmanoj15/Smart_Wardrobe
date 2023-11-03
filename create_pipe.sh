#!/bin/bash

# Create the named pipe
mkfifo /tmp/myfifo

# Give write permission to all users
chmod a+w /tmp/myfifo
