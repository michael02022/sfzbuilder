# This Python file uses the following encoding: utf-8
from PySide6.QtCore    import Qt
from PySide6.QtGui     import QIcon, QPixmap
from PySide6.QtWidgets import QMainWindow
from .ui_mainwindow    import Ui_MainWindow
from .Knob import Knob
import resources.rc_resources as rc

class MainWindow(QMainWindow):
  def __init__(self, parent=None):
    super().__init__(parent)

    rc.qInitResources() # TODO: Not needed, just silence the import warning above.

    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    self.ui.actNew.setIcon(QIcon.fromTheme("document-new",        QIcon(":/document-new")))
    self.ui.actOpen.setIcon(QIcon.fromTheme("document-open",      QIcon(":/document-open")))
    self.ui.actSave.setIcon(QIcon.fromTheme("document-save",      QIcon(":/document-save")))
    self.ui.actSaveAs.setIcon(QIcon.fromTheme("document-save-as", QIcon(":/document-save-as")))
    self.ui.actQuit.setIcon(QIcon.fromTheme("application-exit",   QIcon(":/application-exit")))

    self.ui.pbnAmpEnvAttackShapeEnable.clicked.connect(self.onAmpEnvAttackShapeEnabled)
    self.ui.pbnAmpEnvDecayShapeEnable.clicked.connect(self.onAmpEnvDecayShapeEnabled)

    panPixmap = QPixmap(r":/pan")
    panPixmap.scaledToWidth(48, Qt.SmoothTransformation)
    knbPan = Knob(self.ui.tabPan)
    knbPan.resize(48, 48)
    knbPan.setPixmap(panPixmap, 100)
    knbPan.setValue(0.7);
    self.ui.layPanKnobs.addWidget(knbPan, 1, 1)

    self.ui.lblPanVal.setText(str(knbPan.value()))
    knbPan.valueChanged.connect(lambda v: self.ui.lblPanVal.setText("{:.3f}".format(v)))

  def onAmpEnvAttackShapeEnabled(self):
    self.ui.pnlAmpEnvAttackShape.setEnabled(not self.ui.pnlAmpEnvAttackShape.isEnabled())
    if self.ui.pnlAmpEnvAttackShape.isEnabled():
      self.ui.pbnAmpEnvAttackShapeEnable.setText(self.tr("Disable"))
    else:
      self.ui.pbnAmpEnvAttackShapeEnable.setText(self.tr("Enable"))

  def onAmpEnvDecayShapeEnabled(self):
    self.ui.pnlAmpEnvDecayShape.setEnabled(not self.ui.pnlAmpEnvDecayShape.isEnabled())
    if self.ui.pnlAmpEnvDecayShape.isEnabled():
      self.ui.pbnAmpEnvDecayShapeEnable.setText(self.tr("Disable"))
    else:
      self.ui.pbnAmpEnvDecayShapeEnable.setText(self.tr("Enable"))
