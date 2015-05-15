#!/bin/bash -e

BASEDIR=`dirname $0`/..

$BASEDIR/bin/setup

source $BASEDIR/.env/bin/activate
cd $BASEDIR
export PYTHONPATH=.

$BASEDIR/AutoReserve.py
#exec python $@
