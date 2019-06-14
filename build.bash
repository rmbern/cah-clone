#!/usr/bin/env bash

set -euf

# This script is used to install the dependencies
# the web server needs to run and to build the # python wheel file for distribution from source.  
# Install non-python dependencies, if needed.
if [[ ! $(type -P npm) ]] ; then
  printf \
    "You need npm installed and in your PATH to run this script!\n"

  exit 1
fi 
if [[ ! $(type -P docker) ]] ; then
  printf \
    "You need docker installed and in your PATH to run this script!\n"

  exit 1
fi

mkdir -p cah/static/node_modules
pushd cah/static/node_modules
if [ ! -d "bootstrap" ] ; then
  npm install bootstrap@4.3.1
fi 
popd
# Non python deps end here.

# Create a virtual enviornment, if one does not exist.
if [ ! -d "env" ] ; then
  python3 -m venv env
fi
# Activate script depends on undeclared variables
set +u
. env/bin/activate
set -u

# Now using python instead of python3 because we
# are in the virtual enviornment.
python setup.py bdist_wheel

# Build the docker image
docker build --tag=cah .

printf "Project built!\n"
printf "Run the cah docker image to start the server!\n"
printf "\"docker run -p 5000:5000 cah\"\n"
