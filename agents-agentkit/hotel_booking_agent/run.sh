#!/bin/bash

# Start a toolbox server
./toolbox --tools-file tools.yaml > toolbox.log 2>&1 &

python -m agent