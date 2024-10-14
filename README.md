# SFZBuilder (WIP - PROTOTYPE)

GUI for creating SFZ presets based on SFZ maps under SFZBuilder folder structure.

## Development: Qt Designer and resource file(s)
Create a virtual environment and install the next dependencies

```
pip install PySide6==6.7.3
pip install pyinstaller
```

To generate the python code from ui and resource files by Qt Designer in Linux distros, you have to install the package `qtbase5-dev-tools`, which contains the `uic` and `rcc` tools.

Once updated the UI and/or resource files, run `scripts/update_ui_files.sh`.<br/>
From VSCode just press <kbd>CTRL</kbd> <kbd>Shift</kbd> <kbd>B</kbd> or press <kbd>CTRL</kbd> <kbd>P</kbd> and write `task`, then press space and select `Save UI` task.

## Building
If you want to straight build SFZBuilder, you have to run `update_ui_files.sh` first through VSCode before running pyinstaller.

To make a build for Windows/macOS/Linux, run `pyinstaller ./src/main.py --name=sfzbuilder` and then run the bash script `build.sh` to move the required files to run it normally.