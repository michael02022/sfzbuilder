# Copyright (c) 2024 Andrea Zanellato
# SPDX-License-Identifier: BSD-3-Clause

import sys, importlib.util
name   = 'AyrePy'
spec   = importlib.util.spec_from_file_location(name, "src/ui/AyrePy.py")
module = importlib.util.module_from_spec(spec)
sys.modules[name] = module
spec.loader.exec_module(module)

from PySide6.QtDesigner import QPyDesignerCustomWidgetCollection
from AyrePy import KnobPy

# Set PYSIDE_DESIGNER_PLUGINS to point to this directory and load the plugin
if __name__ == '__main__':
  QPyDesignerCustomWidgetCollection.registerCustomWidget(
    KnobPy, xml="<widget class=\"KnobPy\" name=\"knob\"/>", tool_tip="", icon=":/ayreqt_plugin/knob",
    group="AyrePy", module="AyrePy"
  )
