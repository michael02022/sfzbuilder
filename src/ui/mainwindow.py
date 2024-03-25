# Copyright (c) 2024 Andrea Zanellato
# SPDX-License-Identifier: BSD-3-Clause

# This Python file uses the following encoding: utf-8
from PySide6.QtCore    import QSettings
from PySide6.QtGui     import QIcon
from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QApplication
from .ui_mainwindow    import Ui_MainWindow
from .tabpan           import setupKnobs
import os

import sys, importlib.util
spec      = importlib.util.spec_from_file_location("rc", "resources/rc_resources.py")
resources = importlib.util.module_from_spec(spec)
sys.modules["resources"] = resources
spec.loader.exec_module(resources)
import resources as rc

current_map_ls = []
current_pack_dict = {}

class MainWindow(QMainWindow):
  def __init__(self, parent=None):
    super().__init__(parent)

    rc.qInitResources() # TODO: Not needed, just silence a warning about the import above.

    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    setupKnobs(self.ui)
    self.settings = QSettings(self, QSettings.IniFormat, QSettings.UserScope, QApplication.organizationName, QApplication.applicationDisplayName)

    self.ui.actNew.setIcon(QIcon.fromTheme("document-new",        QIcon(":/document-new")))
    self.ui.actOpen.setIcon(QIcon.fromTheme("document-open",      QIcon(":/document-open")))
    self.ui.actSave.setIcon(QIcon.fromTheme("document-save",      QIcon(":/document-save")))
    self.ui.actSaveAs.setIcon(QIcon.fromTheme("document-save-as", QIcon(":/document-save-as")))
    self.ui.actQuit.setIcon(QIcon.fromTheme("application-exit",   QIcon(":/application-exit")))

    self.ui.pbnMapAdd.setIcon(QIcon.fromTheme("list-add",            QIcon(":/list-add")))
    self.ui.pbnMapClone.setIcon(QIcon.fromTheme("edit-copy",         QIcon(":/edit-copy")))
    self.ui.pbnMapDelete.setIcon(QIcon.fromTheme("list-remove",      QIcon(":/list-remove")))
    self.ui.pbnMapDown.setIcon(QIcon.fromTheme("go-down",            QIcon(":/go-down")))
    self.ui.pbnMapImport.setIcon(QIcon.fromTheme("emblem-downloads", QIcon(":/import")))
    self.ui.pbnMapUp.setIcon(QIcon.fromTheme("go-up",                QIcon(":/go-up")))

    self.ui.pbnMainFolder.clicked.connect(self.onMainFolder)
    if self.settings.value("mainfolderpath") is not None:
      self.ui.txtMainFolder.setText(self.settings.value("mainfolderpath"))

    self.ui.pbnAmpEnvAttackShapeEnable.clicked.connect(self.onAmpEnvAttackShapeEnabled)
    self.ui.pbnAmpEnvDecayShapeEnable.clicked.connect(self.onAmpEnvDecayShapeEnabled)
    self.ui.pbnAmpEnvReleaseShapeEnable.clicked.connect(self.onAmpEnvReleaseShapeEnabled)

    self.ui.pbnFilEnvAttackShapeEnable.clicked.connect(self.onFilEnvAttackShapeEnabled)
    self.ui.pbnFilEnvDecayShapeEnable.clicked.connect(self.onFilEnvDecayShapeEnabled)
    self.ui.pbnFilEnvReleaseShapeEnable.clicked.connect(self.onFilEnvReleaseShapeEnabled)

  def onMainFolder(self):
    main_folder_path = QFileDialog.getExistingDirectory(parent=self, caption="Select a SFZBuilder folder", options=QFileDialog.ShowDirsOnly)
    self.msgbox_ok = QMessageBox(self)
    if False in (os.path.exists(f"{main_folder_path}/MappingPool"), os.path.exists(f"{main_folder_path}/Presets"), os.path.exists(f"{main_folder_path}/Projects")):
      self.msgbox_ok.setText("This is not a valid folder. It must include MappingPool, Presets and Projects folders.")
      self.msgbox_ok.exec()
    else:
      self.ui.txtMainFolder.setText(main_folder_path)
      self.settings.setValue("mainfolderpath", main_folder_path)

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

  def onAmpEnvReleaseShapeEnabled(self):
    self.ui.pnlAmpEnvReleaseShape.setEnabled(not self.ui.pnlAmpEnvReleaseShape.isEnabled())
    if self.ui.pnlAmpEnvReleaseShape.isEnabled():
      self.ui.pbnAmpEnvReleaseShapeEnable.setText(self.tr("Disable"))
    else:
      self.ui.pbnAmpEnvReleaseShapeEnable.setText(self.tr("Enable"))

  def onFilEnvAttackShapeEnabled(self):
    self.ui.pnlFilEnvAttackShape.setEnabled(not self.ui.pnlFilEnvAttackShape.isEnabled())
    if self.ui.pnlFilEnvAttackShape.isEnabled():
      self.ui.pbnFilEnvAttackShapeEnable.setText(self.tr("Disable"))
    else:
      self.ui.pbnFilEnvAttackShapeEnable.setText(self.tr("Enable"))

  def onFilEnvDecayShapeEnabled(self):
    self.ui.pnlFilEnvDecayShape.setEnabled(not self.ui.pnlFilEnvDecayShape.isEnabled())
    if self.ui.pnlFilEnvDecayShape.isEnabled():
      self.ui.pbnFilEnvDecayShapeEnable.setText(self.tr("Disable"))
    else:
      self.ui.pbnFilEnvDecayShapeEnable.setText(self.tr("Enable"))

  def onFilEnvReleaseShapeEnabled(self):
    self.ui.pnlFilEnvReleaseShape.setEnabled(not self.ui.pnlFilEnvReleaseShape.isEnabled())
    if self.ui.pnlFilEnvReleaseShape.isEnabled():
      self.ui.pbnFilEnvReleaseShapeEnable.setText(self.tr("Disable"))
    else:
      self.ui.pbnFilEnvReleaseShapeEnable.setText(self.tr("Enable"))
