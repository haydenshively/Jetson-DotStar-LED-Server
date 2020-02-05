#!/bin/sh
echo "nvidia" | sudo -S -k python3 server.py &
ssh -f -N -R 8080:localhost:8080 haydenshively@35.212.240.99
echo "\n"
