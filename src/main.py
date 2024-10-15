# Copyright (c) 2024 Andrea Zanellato
# SPDX-License-Identifier: BSD-3-Clause

# This Python file uses the following encoding: utf-8
from PySide6.QtCore    import QLocale, QTranslator
from PySide6.QtGui     import QCursor, QIcon
from PySide6.QtWidgets import QApplication
#from PySide6.QtUiTools import QUiLoader

import os, sys
sys.path.append(f"{os.getcwd()}")
from ui.mainwindow import MainWindow
#sys.path.insert(0, "..")

testingOtherTranslation = False # FIXME: put this somewhere in a gitignored config file

def centerOnScreen(widget):
  screen = QApplication.screenAt(QCursor.pos())
  rect   = screen.geometry()
  widget.move((rect.width() - widget.width()) / 2,
    (rect.height() - widget.height()) / 2);

if __name__ == "__main__":
  app = QApplication(sys.argv)
  app.setApplicationDisplayName("SFZBuilder")
  app.setApplicationName("sfzbuilder")
  app.setApplicationVersion("0.1.0")
  app.setOrganizationDomain("sfz.tools")
  app.setOrganizationName("SFZTools")
  app.setWindowIcon(QIcon(":/pngicon"))
  app.setStyle("Fusion")

  locale = QLocale.system()
  if testingOtherTranslation:
    locale = QLocale("it")
    QLocale.setDefault(locale)

  translator = QTranslator(app)
  translator.load("../resources/translations/sfzbuilder_" + locale.name(), os.path.dirname(__file__))
  app.installTranslator(translator)

  window = MainWindow(app)
# window = QUiLoader().load("src/ui/mainwindow.ui", None)
  centerOnScreen(window)
  window.show()

  sys.exit(app.exec())
