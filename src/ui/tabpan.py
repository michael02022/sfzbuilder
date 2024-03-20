# This Python file uses the following encoding: utf-8
from PySide6.QtCore    import Qt
from PySide6.QtGui     import QPixmap
from PySide6.QtWidgets import QLabel
from .Knob import Knob
from .ui_mainwindow    import Ui_MainWindow

def tabPanAddKnobs(parent:Ui_MainWindow):
  names = [ "Pan", "PanKeytrack", "PanVeltrack", "PanRandom" ]
  i = 1
  for name in names:
    knbPixmap = QPixmap(r":/pan")
    knbPixmap.scaledToWidth(48, Qt.SmoothTransformation)
    knob = Knob(parent.ui.tabPan)
    knob.setObjectName("knb" + name)
    knob.resize(48, 48)
    knob
    knob.setPixmap(knbPixmap, 100)
    knob.setValue(0.000);
    parent.ui.layPanKnobs.addWidget(knob, 1, i)
    i += 1

    lblValName = "lbl" + name + "Val"
    lblVal = parent.ui.tabPan.findChild(QLabel, lblValName)
    knob.valueChanged.connect(lambda v: lblVal.setText("{:.3f}".format(v)))
