# This Python file uses the following encoding: utf-8
from PySide6.QtGui     import QCursor, QIcon
from PySide6.QtWidgets import QApplication
from ui.mainwindow     import MainWindow

import sys
import resources.rc_resources as rc
sys.path.insert(0, "..")

def centerOnScreen(widget):
  screen = QApplication.screenAt(QCursor.pos())
  rect   = screen.geometry()
  widget.move((rect.width() - widget.width()) / 2,
    (rect.height() - widget.height()) / 2);

if __name__ == "__main__":
  rc.qInitResources()

  app = QApplication(sys.argv)
  app.setApplicationDisplayName("SFZBuilder")
  app.setApplicationName("sfzbuilder")
  app.setApplicationVersion("0.1.0")
  app.setOrganizationDomain("sfz.tools")
  app.setOrganizationName("SFZTools")
  app.setWindowIcon(QIcon(":/pngicon"))
  app.setStyle("Fusion")

  window = MainWindow()
  centerOnScreen(window)
  window.show()

  sys.exit(app.exec())
