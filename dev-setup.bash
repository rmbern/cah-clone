#!/usr/bin/env bash

# Setup bash enviornment for development and testing

# Source this file to be able to run "flask run",
# "pytest," etc.

export FLASK_APP=cah
export FLASK_ENV=development

# Sets up imports for the ./test directory
export PYTHONPATH="${PWD}"
