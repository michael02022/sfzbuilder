#!/bin/bash

.venv/bin/pyside6-rcc -g python resources/resources.qrc >  src/ui/rc_resources.py
.venv/bin/pyside6-uic -g python -o src/ui/ui_mainwindow.py src/ui/mainwindow.ui
.venv/bin/pyside6-uic -g python -o src/ui/ui_importwindow.py src/ui/importwindow.ui
.venv/bin/pyside6-uic -g python -o src/ui/ui_exportwindow.py src/ui/exportwindow.ui

sed -i 's/PySide2/PySide6/g' src/ui/rc_resources.py
sed -i 's/PySide2/PySide6/g' src/ui/ui_mainwindow.py
sed -i 's/PySide2/PySide6/g' src/ui/ui_importwindow.py
sed -i 's/.Knob.hpp//g'      src/ui/ui_mainwindow.py
sed -i 's/AyrePy/.AyrePy/g'  src/ui/ui_mainwindow.py

if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s|import resources_rc|from .rc_resources import *|g" src/ui/ui_mainwindow.py
else
    sed -i "s/import resources_rc/from .rc_resources import */g" src/ui/ui_mainwindow.py
fi