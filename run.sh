#!/bin/bash -e

BASEDIR=`dirname $0`/

$BASEDIR/bin/scripts/setup

source $BASEDIR/.env/bin/activate
cd $BASEDIR
export PYTHONPATH=.

echo "Running Automator script now"
python3 AutoReserve.py > dailyLog

deactivate
