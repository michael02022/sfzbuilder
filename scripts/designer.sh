#!/bin/bash

APP_PATH="$(dirname -- "${BASH_SOURCE[0]}")"
export LD_PRELOAD=libpython3.11.so
PYSIDE_DESIGNER_PLUGINS="$APP_PATH" designer6 "$APP_PATH/../src/ui/mainwindow.ui"
