# SFZBuilder (WIP - PROTOTYPE)

GUI for creating SFZ presets based on SFZ maps under SFZBuilder folder structure.

## Development: Qt Designer and resource file(s)
Create a virtual environment as `.venv`

Windows (CMD):

```
python -m venv .venv
call .venv\Scripts\activate
```

macOS/Linux (Bash):

```
python3 -m venv .venv
source ./.venv/bin/activate
```

and install the next dependencies

```
pip install PySide6==6.7.3
pip install natsort
pip install pyinstaller
```

Once updated the UI and/or resource files, run `scripts/update_ui_files.sh`.<br/>
From VSCode/ium just press <kbd>CTRL</kbd> <kbd>Shift</kbd> <kbd>B</kbd> or press <kbd>CTRL</kbd> <kbd>P</kbd> and write `task`, then press space and select `Save UI` task. Ignore the error messages once executed.

## Building
If you want to straight build SFZBuilder, you have to run `update_ui_files.sh` first through VSCode/ium before running pyinstaller.

To make a build for Windows/macOS/Linux, run:

```
pyinstaller ./src/main.py --name=sfzbuilder --clean
```

and then run the bash script `build.sh` to move the required files to run it normally.

The executable can be found in `dist/sfzbuilder/(executable named sfzbuilder)`

### macOS users
Make sure to run `sudo` when executing `pyinstaller`

If you have problems to run `build.sh` in macOS, execute `sudo chmod 755 build.sh` and then `sudo ./build.sh`

## Usage
1. Download the init folder and save it in a place you find comfortable:

https://github.com/michael02022/sfzbuilder-init-folder

You can rename this folder with whatever name you like.

2. Install a SFZPack, a ready-to-go start would be:

[SFZBuilder Factory Library Demo](https://huggingface.co/datasets/michl1149/SFZBuilder-Factory-Library-Demo/blob/main/SFZBuilder%20Factory%20Library%20Demo.zip)

and

[Fairlight IIx](https://github.com/sfzmaker/sfzpack-Fairlight_IIx)

Alternately, you can use the [gm.dls bank](https://github.com/sfzmaker/sfzpack-gm.dls)

You should cut/copy the folders inside `MappingPool` forder from these SFZPacks to your init folder to install them.