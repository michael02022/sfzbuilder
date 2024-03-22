#!/bin/sh

PYTHON=$(which python3 2>/dev/null)

if [ ! -f ${PYTHON} ]; then
  PYTHON=python
fi

if [ "$1" = "--gdb" ]; then
  PYTHON="gdb --args $PYTHON"
fi

exec $PYTHON src/main.py
