cmake_minimum_required(VERSION 3.18.0)
project(SFZBuilder
    VERSION      0.1.0
    LANGUAGES    # NONE
    DESCRIPTION  "SFZ mapping builder tool via presets."
    HOMEPAGE_URL "https://github.com/michael02022/sfzbuildertool"
)
set(PROJECT_FILES
    .editorconfig
    .gitignore
    resources/resources.qrc
    src/ui/mainwindow.py
    src/ui/mainwindow.ui
    src/utils/classes/global.py
    src/utils/classes/mapping.py
    src/utils/constants.py
    src/utils/enums.py
    main.py
)
add_custom_target(src SOURCES ${PROJECT_FILES})
