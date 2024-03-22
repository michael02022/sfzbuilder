rcc -g python resources/resources.qrc > resources/rc_resources.py
uic -g python -o src/ui/ui_mainwindow.py src/ui/mainwindow.ui

sed -i 's/PySide2/PySide6/g' resources/rc_resources.py
sed -i 's/PySide2/PySide6/g' src/ui/ui_mainwindow.py
