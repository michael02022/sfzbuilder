#!/bin/sh

current_dir=$(pwd)

#source "$(pwd)/.venv/bin/activate"
wait
#python3 "$(pwd)/.venv/bin/python" pyinstaller "$(pwd)/src/main.py"
#notify-send "Building SFZBuilder..."
#echo "Building SFZBuilder..."
#wait
# rename
#mv "$(pwd)/dist/main/main" "$(pwd)/dist/main/sfzbuilder"

# create folders
mkdir -p "$(pwd)/dist/sfzbuilder/src/ui"
mkdir -p "$(pwd)/dist/sfzbuilder/_internal/utils/fxdict"
mkdir -p "$(pwd)/dist/sfzbuilder/_internal/utils/programlist"

# copy the stuff needed
cp -a "$(pwd)/src/ui/rc_resources.py" "$(pwd)/dist/sfzbuilder/src/ui/rc_resources.py"

cp -a "$(pwd)/src/utils/fxdict/." "$(pwd)/dist/sfzbuilder/_internal/utils/fxdict"
cp -a "$(pwd)/src/utils/programlist/." "$(pwd)/dist/sfzbuilder/_internal/utils/programlist"
