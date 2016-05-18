#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

set -e

# If the run command is the default, do some initialization first
if [ "$(which "$1")" = "/usr/local/bin/start-singleuser.sh" ]; then
  # Mount JPY_USER shared folder to the NOTEBOOK_DIR folder
  : ${NOTEBOOK_DIR:=/home/$NB_USER/work}
  mount -v -t cifs //dtu-storage.win.dtu.dk/$JPY_USER $NOTEBOOK_DIR -o username=$JPY_USER,password=$JPY_PASS,sec=ntlm
fi

# Run the command provided
exec "$@"
