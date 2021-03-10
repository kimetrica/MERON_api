#!/bin/bash
set -e

echo Using usermod to set UID to ${UID}
# this will allow mounts to work, when the user on the host system has
# a UID other than 1000
# This is not required for production but shouldn't hurt
usermod -u ${UID} django

echo Installing test dependencies
pip install -r /app/meron_api/requirements/test.txt

echo Starting normal execution as django user
echo Running tests
gosu django pytest
