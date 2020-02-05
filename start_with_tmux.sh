#!/bin/sh
tmux \
  new -d -s hue_server "cd /home/haydenshively/Developer/Hue; ./start.sh; read"
