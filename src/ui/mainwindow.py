# Copyright (c) 2024 Andrea Zanellato
# SPDX-License-Identifier: BSD-3-Clause

# This Python file uses the following encoding: utf-8
from PySide6.QtCore    import QSettings
from PySide6.QtGui     import QIcon
from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QApplication, QButtonGroup
from .ui_mainwindow    import Ui_MainWindow
from .tabpan           import setupKnobs
from .rc_resources     import *
from collections       import defaultdict
from utils.opcodes     import *
from utils.classes.mapping import Mapping
import os
import glob
import pathlib

def get_mappings(config_path):
  mappings_dict = {}
  mappings_dict["MSamples"] = [p for p in glob.glob(f"**/MSamples/**", recursive=True, root_dir=f"{config_path}/MappingPool/") if p.endswith(".sfz")]
  mappings_dict["PSamples"] = [p for p in glob.glob(f"**/PSamples/**", recursive=True, root_dir=f"{config_path}/MappingPool/") if p.endswith(".sfz")]
  mappings_dict["Wavetables"] = [p for p in glob.glob(f"**", recursive=True, root_dir=f"{config_path}/Wavetables/") if p.endswith(".wav")]
  return mappings_dict

def get_pack(ls):
  pack_dict = defaultdict(list)
  for p in ls:
      path_ls = pathlib.Path(p).parts # split path into list
      pack_dict[path_ls[0]].append(os.path.join(*path_ls[1:]))
  return pack_dict

def which_pack(mappings_dict, pbool, wbool):
    pack = {}
    if pbool:
        pack = get_pack(mappings_dict["PSamples"])
        return pack
    else:
        if wbool:
          pack = get_pack(mappings_dict["Wavetables"])
        else:
          pack = get_pack(mappings_dict["MSamples"])
        return pack

def which_pack_str(pbool, wbool):
    if pbool:
        return "PSamples"
    else:
        if wbool:
          return "Wavetables"
        else:
          return "MSamples"

def get_map_names(map_objects):
    ls = []
    for map in map_objects:
        ls.append(map.get_name())
    return ls

def clip(n, range):
    if n < range[0]:
        return range[0]
    elif n > range[1]:
        return range[1]
    else:
        return n

class MainWindow(QMainWindow):
  def __init__(self, parent=None):
    super().__init__(parent)

    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    setupKnobs(self.ui)

    self.current_map_ls = []
    self.current_pack_dict = {}
    self.map_objects = []

    self.settings = QSettings(self, QSettings.IniFormat, QSettings.UserScope, QApplication.organizationName, QApplication.applicationDisplayName)
    self.enable_edit = False
    self.msgbox_ok = QMessageBox(self)
    self.chk_group = QButtonGroup(self); self.chk_group.addButton(self.ui.chkMap); self.chk_group.addButton(self.ui.chkPercussion); self.chk_group.addButton(self.ui.chkWavetable)
    self.chk_group.setExclusive(True)

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

    # Init folders and mapping dictionary
    self.ui.pbnMainFolder.clicked.connect(self.onMainFolder)
    self.ui.pbnPresetFolder.clicked.connect(self.onPresetFolder)
    if self.settings.value("mainfolderpath") is not None:
      self.ui.txtMainFolder.setText(self.settings.value("mainfolderpath"))
      self.ui.lblPresetPrefix.setText(f"{self.settings.value('presetfolderpath')}/")
      self.mappings_dict = get_mappings(self.settings.value("mainfolderpath"))
      self.enable_edit = True
      #print(self.mappings_dict)

    self.chk_group.buttonClicked.connect(self.onCheckboxesWavetables)

    self.ui.pbnMapAdd.clicked.connect(self.onMapAdd)
    self.ui.pbnMapDelete.clicked.connect(self.onMapDelete)
    self.ui.pbnMapUp.clicked.connect(self.onMapUp)
    self.ui.pbnMapDown.clicked.connect(self.onMapDown)
    self.ui.pbnMapClone.clicked.connect(self.onMapClone)

    self.ui.cbxPack.currentIndexChanged.connect(self.onPackChanged)
    self.ui.cbxMap.currentIndexChanged.connect(self.onMapChanged)
    self.ui.listMap.itemClicked.connect(self.onItemMap)

    self.ui.pbnAmpEnvAttackShapeEnable.clicked.connect(self.onAmpEnvAttackShapeEnabled)
    self.ui.pbnAmpEnvDecayShapeEnable.clicked.connect(self.onAmpEnvDecayShapeEnabled)
    self.ui.pbnAmpEnvReleaseShapeEnable.clicked.connect(self.onAmpEnvReleaseShapeEnabled)

    self.ui.pbnFilEnvAttackShapeEnable.clicked.connect(self.onFilEnvAttackShapeEnabled)
    self.ui.pbnFilEnvDecayShapeEnable.clicked.connect(self.onFilEnvDecayShapeEnabled)
    self.ui.pbnFilEnvReleaseShapeEnable.clicked.connect(self.onFilEnvReleaseShapeEnabled)

  def onMainFolder(self):
    main_folder_path = QFileDialog.getExistingDirectory(parent=self, caption="Select a SFZBuilder folder", options=QFileDialog.ShowDirsOnly)
    if False in (os.path.exists(f"{main_folder_path}/MappingPool"), os.path.exists(f"{main_folder_path}/Presets"), os.path.exists(f"{main_folder_path}/Projects")):
      self.msgbox_ok.setText("This is not a valid folder. It must include MappingPool, Presets and Projects folders.")
      self.msgbox_ok.exec()
    else:
      self.ui.txtMainFolder.setText(main_folder_path)
      self.settings.setValue("mainfolderpath", main_folder_path)

  def onPresetFolder(self):
    preset_folder_path = QFileDialog.getExistingDirectory(parent=self, caption="Select a preset folder", options=QFileDialog.ShowDirsOnly, dir=f"{self.settings.value('mainfolderpath')}/Presets")
    self.ui.lblPresetPrefix.setText(f"{preset_folder_path}/")
    if preset_folder_path != "":
      self.settings.setValue("presetfolderpath", preset_folder_path)

  def onMapAdd(self):
    if self.enable_edit:
      self.current_pack_dict = which_pack(self.mappings_dict, self.ui.chkPercussion.isChecked(), self.ui.chkWavetable.isChecked())

      self.pack_ls = list(self.current_pack_dict)

      self.ui.cbxPack.clear(); self.ui.cbxPack.addItems(self.pack_ls)
      self.map_ls = self.current_pack_dict[self.pack_ls[0]]
      self.ui.cbxMap.clear(); self.ui.cbxMap.addItems(self.map_ls)

      # Mapping object creation
      self.sfz_map = Mapping(which_pack(self.mappings_dict, self.ui.chkPercussion.isChecked(), self.ui.chkWavetable.isChecked()))
      self.sfz_map.set_map(list(self.current_pack_dict)[0], self.map_ls[0])
      self.sfz_map.change_type(which_pack_str(self.ui.chkPercussion.isChecked(), self.ui.chkWavetable.isChecked()))
      self.map_objects.append(self.sfz_map)

      self.ui.listMap.clear(); self.ui.listMap.addItems(get_map_names(self.map_objects))
      #print(vars(self.map_objects[0]))
    else:
      self.msgbox_ok.setText("Please select a SFZBuilder folder.")
      self.msgbox_ok.exec()

  def onCheckboxesWavetables(self):
    if self.ui.listMap.count() != 0:
      self.current_pack_dict = which_pack(self.mappings_dict, self.ui.chkPercussion.isChecked(), self.ui.chkWavetable.isChecked())

      self.pack_ls = list(self.current_pack_dict)

      self.ui.cbxPack.clear(); self.ui.cbxPack.addItems(self.pack_ls)
      self.map_ls = self.current_pack_dict[self.pack_ls[0]]
      self.ui.cbxMap.clear(); self.ui.cbxMap.addItems(self.map_ls)

      # update
      idx = self.ui.listMap.currentRow()

      self.map_objects[idx].set_map(list(self.current_pack_dict)[0], self.map_ls[0])
      self.map_objects[idx].change_type(which_pack_str(self.ui.chkPercussion.isChecked(), self.ui.chkWavetable.isChecked()))

      self.ui.listMap.clear(); self.ui.listMap.addItems(get_map_names(self.map_objects))
      self.ui.listMap.setCurrentRow(idx)

  def onMapDelete(self):
    if self.ui.listMap.count() != 0:
      idx = self.ui.listMap.currentRow()
      self.msgbox_yesno = QMessageBox(self); self.msgbox_yesno.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
      self.msgbox_yesno.setText(f"Are you sure you want to remove {self.map_objects[idx].get_name()}?")
      answer = self.msgbox_yesno.exec()
      match answer:
        case QMessageBox.Yes:
          del self.map_objects[idx]
          self.ui.listMap.clear(); self.ui.listMap.addItems(get_map_names(self.map_objects))
          if self.ui.listMap.count() != 0: # if it has objects to select
            if self.ui.listMap.count() <= idx:
              self.ui.listMap.setCurrentRow(self.ui.listMap.count() - 1) # set index to the last object
            else:
              self.ui.listMap.setCurrentRow(idx)
        case QMessageBox.No:
          None
  # TODO: FIX A BUG WHERE MULTIPLE MAP OBJECTS ARE CHANGING THEIR MAPS INSTEAD OF THE SELECTED ONE ONLY
  def onMapClone(self):
    if self.ui.listMap.count() != 0:
      idx = self.ui.listMap.currentRow()
      element = self.map_objects[idx]
      self.map_objects.insert(clip(idx + 1, (0, len(self.map_objects))), element)
      self.ui.listMap.clear(); self.ui.listMap.addItems(get_map_names(self.map_objects))
      self.ui.listMap.setCurrentRow(idx + 1)

  def onMapUp(self):
    if self.ui.listMap.count() != 0:
      idx = clip(self.ui.listMap.currentRow(), (0, len(self.map_objects)))
      self.map_objects.insert(clip(idx - 1, (0, len(self.map_objects))), self.map_objects.pop(idx))
      self.ui.listMap.clear(); self.ui.listMap.addItems(get_map_names(self.map_objects))
      self.ui.listMap.setCurrentRow(clip(idx - 1, (0, len(self.map_objects))))

  def onMapDown(self):
    if self.ui.listMap.count() != 0:
      idx = clip(self.ui.listMap.currentRow(), (0, len(self.map_objects)))
      self.map_objects.insert(clip(idx + 1, (0, len(self.map_objects))), self.map_objects.pop(idx))
      self.ui.listMap.clear(); self.ui.listMap.addItems(get_map_names(self.map_objects))
      self.ui.listMap.setCurrentRow(clip(idx + 1, (0, len(self.map_objects) - 1)))

  def onPackChanged(self):
    self.current_pack_dict = which_pack(self.mappings_dict, self.ui.chkPercussion.isChecked(), self.ui.chkWavetable.isChecked())
    self.map_ls = self.current_pack_dict[self.pack_ls[self.ui.cbxPack.currentIndex()]]
    self.ui.cbxMap.clear(); self.ui.cbxMap.addItems(self.map_ls)

    # update
    if self.ui.listMap.count() != 0:
      idx = self.ui.listMap.currentRow()
      pk_idx = self.ui.cbxPack.currentIndex()
      mp_idx = self.ui.cbxMap.currentIndex()

      self.map_objects[idx].set_map(list(self.current_pack_dict)[pk_idx], self.map_ls[mp_idx])

      self.ui.listMap.clear(); self.ui.listMap.addItems(get_map_names(self.map_objects))
      self.ui.listMap.setCurrentRow(idx)
    else:
      None

  def onMapChanged(self):
    if self.ui.listMap.count() != 0:
      idx = self.ui.listMap.currentRow()
      pk_idx = self.ui.cbxPack.currentIndex()
      mp_idx = self.ui.cbxMap.currentIndex()

      self.map_objects[idx].set_map(list(self.current_pack_dict)[pk_idx], self.map_ls[mp_idx])

      self.ui.listMap.clear(); self.ui.listMap.addItems(get_map_names(self.map_objects))
      self.ui.listMap.setCurrentRow(idx)
    else:
      None

  def onItemMap(self):
    self.get_map_values()

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

  def get_map_values(self):
    idx = self.ui.listMap.currentRow()
    map_dict = vars(self.map_objects[idx])
    for k in map_dict:
      match k:
        case "map_key_range":
          self.ui.sbxKeyLo.setValue(map_dict.get(k)[0])
          self.ui.sbxKeyHi.setValue(map_dict.get(k)[1])
        case "map_vel_range":
          self.ui.sbxVelLo.setValue(map_dict.get(k)[0])
          self.ui.sbxVelHi.setValue(map_dict.get(k)[1])
        case "on_cc_rangebool":
          self.ui.chkNoteOn.setChecked(map_dict.get(k))
        case "on_cc_range":
          self.ui.sbxCc.setValue(map_dict.get(k)[0])
          self.ui.sbxCcLo.setValue(map_dict.get(k)[1])
          self.ui.sbxCcHi.setValue(map_dict.get(k)[2])
        case "random_rangebool":
          self.ui.chkRandom.setChecked(map_dict.get(k))
        case "random_range":
          self.ui.dsbRandomLo.setValue(map_dict.get(k)[0])
          self.ui.dsbRandomLo.setValue(map_dict.get(k)[1])

  def update_obj(self):
    None
