#!/bin/bash

# Bash script to automate the installation and setup of the app

# To run:
# Fluid-Solutions$ source setup.sh

# install the reuqired python libraries
pip install -r requirements.txt

# initalize the database 
pushd app/
python3 app.py --initdb
popd

cd app/