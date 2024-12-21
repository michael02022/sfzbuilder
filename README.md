# SFZBuilder (WIP - PROTOTYPE)

GUI for creating SFZ presets based on SFZ maps under SFZBuilder folder structure.

## Development: Qt Designer and resource file(s)
Create a virtual environment as `.venv` and install the next dependencies

```
pip install PySide6==6.7.3
pip install natsort
pip install pyinstaller
```

Once updated the UI and/or resource files, run `scripts/update_ui_files.sh`.<br/>
From VSCode just press <kbd>CTRL</kbd> <kbd>Shift</kbd> <kbd>B</kbd> or press <kbd>CTRL</kbd> <kbd>P</kbd> and write `task`, then press space and select `Save UI` task.

## Building
If you want to straight build SFZBuilder, you have to run `update_ui_files.sh` first through VSCode/ium before running pyinstaller.

To make a build for Windows/macOS/Linux, run `pyinstaller ./src/main.py --name=sfzbuilder` and then run the bash script `build.sh` to move the required files to run it normally.

The executable can be found in `dist/sfzbuilder/(executable named sfzbuilder)`

### macOS users
Make sure to run `sudo` when executing `pyinstaller`

If you have problems to run `build.sh` in macOS, execute `sudo chmod 755 build.sh`

## Usage
Download the init folder and save it in a place you find comfortable: https://github.com/michael02022/sfzbuilder-init-folder

And install a SFZPack, a ready-to-go start would be the [Fairlight IIx](https://github.com/sfzbuilder/sfzpack-gm.dls), alternately, you can use the [gm.dls bank](https://github.com/sfzbuilder/sfzpack-gm.dls)