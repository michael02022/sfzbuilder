# Copyright (c) 2024 Andrea Zanellato
# SPDX-License-Identifier: BSD-3-Clause

# This Python file uses the following encoding: utf-8
from PySide6.QtCore    import QSettings
from PySide6.QtGui     import QIcon
from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QApplication, QButtonGroup
from .ui_mainwindow    import Ui_MainWindow
#from .tabpan           import setupKnobs
from .rc_resources     import *
from collections       import defaultdict
from utils.opcodes     import *
from utils.classes.mapping import Mapping
from utils.enums       import *
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

def float_to_int(_flt, decimals):
  negative = False
  flt = "{:.3f}".format(float(_flt))
  ls = str(flt).split(".")
  if "-" in ls[0]:
    negative = True
    s = ls[0][1:]
  else:
    s = ls[0]
  zeros = (decimals - len(ls[1]))
  d = ls[1] + ("0" * zeros)
  r = s + d
  if negative:
    r = "-" + r
  return int(r)

def int_to_float(integer, decimals):
  decimals = 3
  negative = False
  ls = str(integer)
  if "-" in ls[0]:
    negative = True
    s = ls[1:]
  else:
    s = ls
  if len(s) <= decimals:
    predecimal = 0
  else:
    predecimal = s[:-abs(decimals)]

  postdecimal = s[-abs(decimals):]
  r = f"{predecimal}.{postdecimal}"
  if negative:
    r = "-" + r

  return float(r)

class MainWindow(QMainWindow):
  def __init__(self, parent=None):
    super().__init__(parent)

    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    #setupKnobs(self.ui)

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

    # ENVELOPES
    #self.ui.knbPan.setMinimum(-100.0)
    #self.ui.knbPan.setMaximum(100.0)

    self.ui.cbxAmpEnvAttackShapeEnable.stateChanged.connect(self.onAmpEnvAttackShapeEnabled)
    self.ui.cbxAmpEnvDecayShapeEnable.stateChanged.connect(self.onAmpEnvDecayShapeEnabled)
    self.ui.cbxAmpEnvReleaseShapeEnable.stateChanged.connect(self.onAmpEnvReleaseShapeEnabled)

    self.ui.cbxFilEnvAttackShapeEnable.stateChanged.connect(self.onFilEnvAttackShapeEnabled)
    self.ui.cbxFilEnvDecayShapeEnable.stateChanged.connect(self.onFilEnvDecayShapeEnabled)
    self.ui.cbxFilEnvReleaseShapeEnable.stateChanged.connect(self.onFilEnvReleaseShapeEnabled)

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
  def onAmpEnvDecayShapeEnabled(self):
    self.ui.pnlAmpEnvDecayShape.setEnabled(not self.ui.pnlAmpEnvDecayShape.isEnabled())
  def onAmpEnvReleaseShapeEnabled(self):
    self.ui.pnlAmpEnvReleaseShape.setEnabled(not self.ui.pnlAmpEnvReleaseShape.isEnabled())
  def onFilEnvAttackShapeEnabled(self):
    self.ui.pnlFilEnvAttackShape.setEnabled(not self.ui.pnlFilEnvAttackShape.isEnabled())
  def onFilEnvDecayShapeEnabled(self):
    self.ui.pnlFilEnvDecayShape.setEnabled(not self.ui.pnlFilEnvDecayShape.isEnabled())
  def onFilEnvReleaseShapeEnabled(self):
    self.ui.pnlFilEnvReleaseShape.setEnabled(not self.ui.pnlFilEnvReleaseShape.isEnabled())

  # UPDATE OBJECT -> WIDGET
  def get_map_values(self):
    idx = self.ui.listMap.currentRow()
    map_dict = vars(self.map_objects[idx])
    for k in map_dict:
      match k:
        ## WAVETABLE
        case "wave":
          self.ui.cbxWave.setCurrentIndex(wavetables.index(map_dict.get(k)))
        case "wave_mode":
          self.ui.cbxWaveMode.setCurrentIndex(wave_modes.index(map_dict.get(k)))
        case "wave_unison":
          self.ui.sbxWaveUnison.setValue(map_dict.get(k))
        case "wave_quality":
          self.ui.sbxWaveQuality.setValue(map_dict.get(k))
        case "wave_phase":
          self.ui.sbxWavePhase.setValue(map_dict.get(k))
        case "wave_mod_depth":
          self.ui.sbxWaveModDepth.setValue(map_dict.get(k))
        case "wave_mod_depth_cc":
          self.ui.sbxWaveModDepthCc.setValue(map_dict.get(k)[0])
          self.ui.sbxWaveModDepthCcVal.setValue(map_dict.get(k)[1])
        case "wave_detune":
          self.ui.sbxWaveDetune.setValue(map_dict.get(k))
        case "wave_detune_cc":
          self.ui.sbxWaveDetuneCc.setValue(map_dict.get(k)[0])
          self.ui.sbxWaveDetuneCcVal.setValue(map_dict.get(k)[1])
        ## MAP
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
        case "volume":
          self.ui.dsbVolume.setValue(map_dict.get(k))
        case "keyswitchbool":
          self.ui.chkKeyswitchCount.setChecked(map_dict.get(k))
        case "keyswitch":
          self.ui.sbxKeyswitchCount.setValue(map_dict.get(k))
        case "sw_label":
          self.ui.txtKeyswitchLabel.setText(map_dict.get(k))
        case "output":
          self.ui.sbxOutput.setValue(map_dict.get(k))
        case "polybool":
          self.ui.chkPolyphony.setChecked(map_dict.get(k))
        case "poly":
          self.ui.sbxPolyphony.setValue(map_dict.get(k))
        case "note_polybool":
          self.ui.chkNotePolyphony.setChecked(map_dict.get(k))
        case "note_poly":
          self.ui.sbxNotePolyphony.setValue(map_dict.get(k))
        case "note_selfmask":
          self.ui.chkNoteSelfmask.setChecked(map_dict.get(k))
        case "trigger":
          self.ui.cbxTriggerMode.setCurrentIndex(trigger_modes.index(map_dict.get(k)))
        case "rt_dead":
          self.ui.chkRtDead.setChecked(map_dict.get(k))
        case "rt_decaybool":
          self.ui.chkRtDecay.setChecked(map_dict.get(k))
        case "rt_decay":
          self.ui.dsbRtDecay.setValue(map_dict.get(k))
        case "key_opcode":
          self.ui.chkUseKey.setChecked(map_dict.get(k))
        case "keycenterbool":
          self.ui.chkUseGlobalPitchKeycenter.setChecked(map_dict.get(k))
        case "keycenter":
          self.ui.sbxUsePitchKeycenter4All.setValue(map_dict.get(k))

        ## SAMPLE
        case "offsetbool":
          self.ui.chkSampleOffsetValue.setChecked(map_dict.get(k))
        case "offset":
          self.ui.sbxSampleOffsetValue.setValue(map_dict.get(k))
        case "offset_random":
          self.ui.sbxSampleOffsetRandom.setValue(map_dict.get(k))
        case "delay":
          self.ui.dsbSampleMapDelay.setValue(map_dict.get(k))
        case "note_offset":
          self.ui.sbxSampleTransposeNote.setValue(map_dict.get(k))
        case "pitch_transpose":
          self.ui.sbxSampleTransposePitch.setValue(map_dict.get(k))
        case "quality":
          self.ui.sbxSampleQuality.setValue(map_dict.get(k))
        case "loop_mode":
          self.ui.cbxLoopMode.setCurrentIndex(loop_modes.index(map_dict.get(k)))
        case "direction":
          self.ui.cbxDirection.setCurrentIndex(loop_directions.index(map_dict.get(k)))
        case "vel2offset":
          self.ui.sbxSampleOffsetVelocity.setValue(map_dict.get(k))
        case "exclass":
          self.ui.chkRegionExclusiveClass.setChecked(map_dict.get(k))
        case "group":
          self.ui.sbxGroup.setValue(map_dict.get(k))
        case "off_by":
          self.ui.sbxOffBy.setValue(map_dict.get(k))
        case "off_mode":
          self.ui.cbxOffMode.setCurrentIndex(off_modes.index(map_dict.get(k)))
        case "off_time":
          self.ui.dsbOffTime.setValue(map_dict.get(k))

        ## PAN
        case "panbool":
          self.ui.gbxPan.setChecked(map_dict.get(k))
        case "pan_keycenter":
          self.ui.sbxPanKeycenter.setValue(map_dict.get(k))
        case "pan_value":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialPan.setValue(dialval)
          self.ui.dsbPan.setValue(map_dict.get(k))
        case "pan_keytrack":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialPanKeytrack.setValue(dialval)
          self.ui.dsbPanKeytrack.setValue(map_dict.get(k))
        case "pan_veltrack":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialPanVeltrack.setValue(dialval)
          self.ui.dsbPanVeltrack.setValue(map_dict.get(k))
        case "pan_random":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialPanRandom.setValue(dialval)
          self.ui.dsbPanRandom.setValue(map_dict.get(k))

        ## AMP
        case "amp_keycenter":
          self.ui.sbxAmpKeycenter.setValue(map_dict.get(k))
        case "amp_velfloorbool":
          self.ui.chkAmpVelFloor.setChecked(map_dict.get(k))
        case "amp_velfloor":
          self.ui.sbxAmpVelFloor.setValue(map_dict.get(k))
        case "amp_env_vel2attackbool":
          self.ui.chkAmpVelAttack.setChecked(map_dict.get(k))
        case "amp_env_vel2attack":
          self.ui.sbxAmpVelAttack.setValue(map_dict.get(k))
        case "amp_keytrack":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialAmpKeytrack.setValue(dialval)
          self.ui.dsbAmpKeytrack.setValue(map_dict.get(k))
        case "amp_veltrack":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialAmpVeltrack.setValue(dialval)
          self.ui.dsbAmpVeltrack.setValue(map_dict.get(k))
        case "amp_random":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialAmpRandom.setValue(dialval)
          self.ui.dsbAmpRandom.setValue(map_dict.get(k))

        ## AMP LFO
        case "amp_lfo":
          self.ui.gbxAmpLfo.setChecked(map_dict.get(k))
        case "amp_lfo_delay":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialAmpLfoDelay.setValue(dialval)
          self.ui.dsbAmpLfoDelay.setValue(map_dict.get(k))
        case "amp_lfo_fade":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialAmpLfoFade.setValue(dialval)
          self.ui.dsbAmpLfoFade.setValue(map_dict.get(k))
        case "amp_lfo_depth":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialAmpLfoDepth.setValue(dialval)
          self.ui.dsbAmpLfoDepth.setValue(map_dict.get(k))
        case "amp_lfo_freq":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialAmpLfoFreq.setValue(dialval)
          self.ui.dsbAmpLfoFreq.setValue(map_dict.get(k))

        ## AMP ENV
        case "amp_env":
          self.ui.gbxAmpEnv.setChecked(map_dict.get(k))
        case "amp_env_start":
          self.ui.sldAmpEnvStart.setValue(map_dict.get(k))
        case "amp_env_delay":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialAmpEnvDelay.setValue(dialval)
          self.ui.dsbAmpEnvDelay.setValue(map_dict.get(k))
        case "amp_env_attack":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialAmpEnvAttack.setValue(dialval)
          self.ui.dsbAmpEnvAttack.setValue(map_dict.get(k))
        case "amp_env_attack_shape":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialAmpEnvAttackShape.setValue(dialval)
          self.ui.dsbAmpEnvAttackShape.setValue(map_dict.get(k))
        case "amp_env_hold":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialAmpEnvHold.setValue(dialval)
          self.ui.dsbAmpEnvHold.setValue(map_dict.get(k))
        case "amp_env_decay":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialAmpEnvDecay.setValue(dialval)
          self.ui.dsbAmpEnvDecay.setValue(map_dict.get(k))
        case "amp_env_decay_shape":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialAmpEnvDecayShape.setValue(dialval)
          self.ui.dsbAmpEnvDecayShape.setValue(map_dict.get(k))
        case "amp_env_sustain":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialAmpEnvSustain.setValue(dialval)
          self.ui.dsbAmpEnvSustain.setValue(map_dict.get(k))
        case "amp_env_release":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialAmpEnvRelease.setValue(dialval)
          self.ui.dsbAmpEnvRelease.setValue(map_dict.get(k))
        case "amp_env_release_shape":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialAmpEnvReleaseShape.setValue(dialval)
          self.ui.dsbAmpEnvReleaseShape.setValue(map_dict.get(k))

        ## FILTER
        case "fil":
          self.ui.gbxFilterGeneral.setChecked(map_dict.get(k))
        case "fil_type":
          self.ui.cbxFilterType.setCurrentIndex(filter_type.index(map_dict.get(k)))
        case "fil_keycenter":
          self.ui.sbxFilterKeycenter.setValue(map_dict.get(k))
        case "cutoff":
          self.ui.dialFilterCutoff.setValue(map_dict.get(k))
          self.ui.sbxFilterCutoff.setValue(map_dict.get(k))
        case "resonance":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialFilterResonance.setValue(dialval)
          self.ui.dsbFilterResonance.setValue(map_dict.get(k))
        case "fil_keytrack":
          self.ui.dialFilterKeytrack.setValue(map_dict.get(k))
          self.ui.sbxFilterKeytrack.setValue(map_dict.get(k))
        case "fil_veltrack":
          self.ui.dialFilterVeltrack.setValue(map_dict.get(k))
          self.ui.sbxFilterVeltrack.setValue(map_dict.get(k))
        case "fil_random":
          self.ui.dialFilterRandom.setValue(map_dict.get(k))
          self.ui.sbxFilterRandom.setValue(map_dict.get(k))

        ## FILTER LFO
        case "fil_lfo":
          self.ui.gbxFilterLfo.setChecked(map_dict.get(k))
        case "fil_lfo_delay":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialFilterLfoDelay.setValue(dialval)
          self.ui.dsbFilterLfoDelay.setValue(map_dict.get(k))
        case "fil_lfo_fade":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialFilterLfoFade.setValue(dialval)
          self.ui.dsbFilterLfoFade.setValue(map_dict.get(k))
        case "fil_lfo_depth":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialFilterLfoDepth.setValue(dialval)
          self.ui.dsbFilterLfoDepth.setValue(map_dict.get(k))
        case "fil_lfo_freq":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialFilterLfoFreq.setValue(dialval)
          self.ui.dsbFilterLfoFreq.setValue(map_dict.get(k))

        ## FILTER ENV
        case "fil_env":
          self.ui.gbxFilEnv.setChecked(map_dict.get(k))

        case "fil_env_depth":
          self.ui.dialFilEnvDepth.setValue(map_dict.get(k))
          self.ui.sbxFilEnvDepth.setValue(map_dict.get(k))
        case "fil_vel2depth":
          self.ui.dialFilEnvDepthVel.setValue(map_dict.get(k))
          self.ui.sbxFilEnvDepthVel.setValue(map_dict.get(k))

        case "fil_env_start":
          self.ui.sldFilEnvStart.setValue(map_dict.get(k))
        case "fil_env_delay":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialFilEnvDelay.setValue(dialval)
          self.ui.dsbFilEnvDelay.setValue(map_dict.get(k))
        case "fil_env_attack":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialFilEnvAttack.setValue(dialval)
          self.ui.dsbFilEnvAttack.setValue(map_dict.get(k))
        case "fil_env_attack_shape":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialFilEnvAttackShape.setValue(dialval)
          self.ui.dsbFilEnvAttackShape.setValue(map_dict.get(k))
        case "fil_env_hold":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialFilEnvHold.setValue(dialval)
          self.ui.dsbFilEnvHold.setValue(map_dict.get(k))
        case "fil_env_decay":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialFilEnvDecay.setValue(dialval)
          self.ui.dsbFilEnvDecay.setValue(map_dict.get(k))
        case "fil_env_decay_shape":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialFilEnvDecayShape.setValue(dialval)
          self.ui.dsbFilEnvDecayShape.setValue(map_dict.get(k))
        case "fil_env_sustain":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialFilEnvSustain.setValue(dialval)
          self.ui.dsbFilEnvSustain.setValue(map_dict.get(k))
        case "fil_env_release":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialFilEnvRelease.setValue(dialval)
          self.ui.dsbFilEnvRelease.setValue(map_dict.get(k))
        case "fil_env_release_shape":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialFilEnvReleaseShape.setValue(dialval)
          self.ui.dsbFilEnvReleaseShape.setValue(map_dict.get(k))

        ## PITCH
        case "pitch":
          self.ui.gbxFilterGeneral.setChecked(map_dict.get(k))
        case "pitch_keytrack":
          self.ui.dialPitchKeytrack.setValue(map_dict.get(k))
          self.ui.sbxPitchKeytrack.setValue(map_dict.get(k))
        case "pitch_veltrack":
          self.ui.dialPitchVeltrack.setValue(map_dict.get(k))
          self.ui.sbxPitchVeltrack.setValue(map_dict.get(k))
        case "pitch_random":
          self.ui.dialPitchRandom.setValue(map_dict.get(k))
          self.ui.sbxPitchRandom.setValue(map_dict.get(k))

        ## PITCH LFO
        case "pit_lfo":
          self.ui.gbxPitchLfo.setChecked(map_dict.get(k))
        case "pit_lfo_delay":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialPitchLfoDelay.setValue(dialval)
          self.ui.dsbPitchLfoDelay.setValue(map_dict.get(k))
        case "pit_lfo_fade":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialPitchLfoFade.setValue(dialval)
          self.ui.dsbPitchLfoFade.setValue(map_dict.get(k))
        case "pit_lfo_depth":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialPitchLfoDepth.setValue(dialval)
          self.ui.dsbPitchLfoDepth.setValue(map_dict.get(k))
        case "pit_lfo_freq":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialPitchLfoFreq.setValue(dialval)
          self.ui.dsbPitchLfoFreq.setValue(map_dict.get(k))

        ## PITCH ENV
        case "pit_env":
          self.ui.gbxPitchEnv.setChecked(map_dict.get(k))

        case "pit_env_depth":
          self.ui.dialPitchEnvDepth.setValue(map_dict.get(k))
          self.ui.sbxPitchEnvDepth.setValue(map_dict.get(k))

        case "pit_env_start":
          self.ui.sldPitchEnvStart.setValue(map_dict.get(k))
        case "pit_env_delay":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialPitchEnvDelay.setValue(dialval)
          self.ui.dsbPitchEnvDelay.setValue(map_dict.get(k))
        case "pit_env_attack":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialPitchEnvAttack.setValue(dialval)
          self.ui.dsbPitchEnvAttack.setValue(map_dict.get(k))
        case "pit_env_hold":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialPitchEnvHold.setValue(dialval)
          self.ui.dsbPitchEnvHold.setValue(map_dict.get(k))
        case "pit_env_decay":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialPitchEnvDecay.setValue(dialval)
          self.ui.dsbPitchEnvDecay.setValue(map_dict.get(k))
        case "pit_env_sustain":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialPitchEnvSustain.setValue(dialval)
          self.ui.dsbPitchEnvSustain.setValue(map_dict.get(k))
        case "pit_env_release":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialPitchEnvRelease.setValue(dialval)
          self.ui.dsbPitchEnvRelease.setValue(map_dict.get(k))

        ## OPCODES
        case "opcode_notepad":
          self.ui.txtOpcodes.setPlainText(map_dict.get(k))

    # /// WIDGET MONITORING
    # Spinboxes
    # self.map_objects[self.ui.listMap.currentRow()])
    self.ui.sbxKeyLo.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxKeyHi.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxVelLo.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxVelHi.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxCc.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxCcLo.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxCcHi.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxOutput.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxPolyphony.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxNotePolyphony.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxKeyswitchCount.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxUsePitchKeycenter4All.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbRtDecay.valueChanged.connect(self.onUiValueChanged)

    self.ui.sbxWaveUnison.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxWaveQuality.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxWavePhase.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxWaveModDepth.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxWaveModDepthCc.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxWaveModDepthCcVal.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxWaveDetune.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxWaveDetuneCc.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxWaveDetuneCcVal.valueChanged.connect(self.onUiValueChanged)

    self.ui.dsbSampleMapDelay.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxSampleQuality.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxSampleOffsetValue.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxSampleOffsetRandom.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxSampleOffsetVelocity.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxSampleTransposePitch.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxSampleTransposeNote.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxGroup.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxOffBy.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbOffTime.valueChanged.connect(self.onUiValueChanged)

    self.ui.sbxPanKeycenter.valueChanged.connect(self.onUiValueChanged)

    self.ui.sbxAmpKeycenter.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxAmpVelFloor.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxAmpVelAttack.valueChanged.connect(self.onUiValueChanged)

    self.ui.sbxFilterKeycenter.valueChanged.connect(self.onUiValueChanged)

    # Checkboxes
    self.ui.chkNoteOn.stateChanged.connect(self.onUiValueChanged)
    self.ui.chkRandom.stateChanged.connect(self.onUiValueChanged)
    self.ui.chkPolyphony.stateChanged.connect(self.onUiValueChanged)
    self.ui.chkNotePolyphony.stateChanged.connect(self.onUiValueChanged)
    self.ui.chkNoteSelfmask.stateChanged.connect(self.onUiValueChanged)
    self.ui.chkKeyswitchCount.stateChanged.connect(self.onUiValueChanged)
    self.ui.chkRtDead.stateChanged.connect(self.onUiValueChanged)
    self.ui.chkRtDecay.stateChanged.connect(self.onUiValueChanged)
    self.ui.chkUseGlobalPitchKeycenter.stateChanged.connect(self.onUiValueChanged)
    self.ui.chkUseKey.stateChanged.connect(self.onUiValueChanged)
    self.ui.chkSampleOffsetValue.stateChanged.connect(self.onUiValueChanged)
    self.ui.chkRegionExclusiveClass.stateChanged.connect(self.onUiValueChanged)

    self.ui.gbxPan.toggled.connect(self.onUiValueChanged)

    self.ui.chkAmpVelFloor.stateChanged.connect(self.onUiValueChanged)
    self.ui.chkAmpVelAttack.stateChanged.connect(self.onUiValueChanged)
    self.ui.gbxAmpLfo.toggled.connect(self.onUiValueChanged)
    self.ui.gbxAmpEnv.toggled.connect(self.onUiValueChanged)

    self.ui.gbxFilterGeneral.toggled.connect(self.onUiValueChanged)
    self.ui.gbxFilterLfo.toggled.connect(self.onUiValueChanged)
    self.ui.gbxFilEnv.toggled.connect(self.onUiValueChanged)

    self.ui.gbxPitch.toggled.connect(self.onUiValueChanged)
    self.ui.gbxPitchLfo.toggled.connect(self.onUiValueChanged)
    self.ui.gbxPitchEnv.toggled.connect(self.onUiValueChanged)

    # ComboBoxes
    self.ui.cbxWave.currentIndexChanged.connect(self.onUiValueChanged)
    self.ui.cbxWaveMode.currentIndexChanged.connect(self.onUiValueChanged)

    self.ui.cbxTriggerMode.currentIndexChanged.connect(self.onUiValueChanged)

    self.ui.cbxLoopMode.currentIndexChanged.connect(self.onUiValueChanged)
    self.ui.cbxDirection.currentIndexChanged.connect(self.onUiValueChanged)

    self.ui.cbxOffMode.currentIndexChanged.connect(self.onUiValueChanged)

    self.ui.cbxFilterType.currentIndexChanged.connect(self.onUiValueChanged)

    # Text
    self.ui.txtKeyswitchLabel.textEdited.connect(self.onUiValueChanged)
    self.ui.txtOpcodes.textChanged.connect(self.onUiValueChanged)

    # KNOBS / DIALS
    self.ui.dialPan.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbPan.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialPanKeytrack.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbPanKeytrack.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialPanVeltrack.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbPanVeltrack.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialPanRandom.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbPanRandom.valueChanged.connect(self.onUiValueChanged)

    self.ui.dialAmpKeytrack.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbAmpKeytrack.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialAmpVeltrack.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbAmpVeltrack.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialAmpRandom.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbAmpRandom.valueChanged.connect(self.onUiValueChanged)

    self.ui.dialAmpLfoDelay.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbAmpLfoDelay.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialAmpLfoFade.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbAmpLfoFade.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialAmpLfoDepth.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbAmpLfoDepth.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialAmpLfoFreq.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbAmpLfoFreq.valueChanged.connect(self.onUiValueChanged)

    self.ui.sldAmpEnvStart.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialAmpEnvDelay.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbAmpEnvDelay.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialAmpEnvAttack.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbAmpEnvAttack.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialAmpEnvAttackShape.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbAmpEnvAttackShape.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialAmpEnvHold.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbAmpEnvHold.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialAmpEnvDecay.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbAmpEnvDecay.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialAmpEnvDecayShape.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbAmpEnvDecayShape.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialAmpEnvSustain.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbAmpEnvSustain.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialAmpEnvRelease.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbAmpEnvRelease.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialAmpEnvReleaseShape.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbAmpEnvReleaseShape.valueChanged.connect(self.onUiValueChanged)

    self.ui.dialFilterCutoff.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxFilterCutoff.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialFilterResonance.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbFilterResonance.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialFilterKeytrack.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxFilterKeytrack.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialFilterVeltrack.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxFilterVeltrack.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialFilterRandom.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxFilterRandom.valueChanged.connect(self.onUiValueChanged)

    self.ui.dialFilterLfoDelay.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbFilterLfoDelay.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialFilterLfoFade.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbFilterLfoFade.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialFilterLfoDepth.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbFilterLfoDepth.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialFilterLfoFreq.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbFilterLfoFreq.valueChanged.connect(self.onUiValueChanged)

    self.ui.dialFilEnvDepth.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxFilEnvDepth.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialFilEnvDepthVel.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxFilEnvDepthVel.valueChanged.connect(self.onUiValueChanged)

    self.ui.sldFilEnvStart.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialFilEnvDelay.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbFilEnvDelay.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialFilEnvAttack.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbFilEnvAttack.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialFilEnvAttackShape.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbFilEnvAttackShape.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialFilEnvHold.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbFilEnvHold.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialFilEnvDecay.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbFilEnvDecay.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialFilEnvDecayShape.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbFilEnvDecayShape.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialFilEnvSustain.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbFilEnvSustain.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialFilEnvRelease.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbFilEnvRelease.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialFilEnvReleaseShape.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbFilEnvReleaseShape.valueChanged.connect(self.onUiValueChanged)

    self.ui.dialPitchKeytrack.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxPitchKeytrack.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialPitchVeltrack.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxPitchVeltrack.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialPitchRandom.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxPitchRandom.valueChanged.connect(self.onUiValueChanged)

    self.ui.dialPitchLfoDelay.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbPitchLfoDelay.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialPitchLfoFade.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbPitchLfoFade.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialPitchLfoDepth.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbPitchLfoDepth.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialPitchLfoFreq.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbPitchLfoFreq.valueChanged.connect(self.onUiValueChanged)

    self.ui.sldPitchEnvStart.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialPitchEnvDelay.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbPitchEnvDelay.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialPitchEnvAttack.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbPitchEnvAttack.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialPitchEnvHold.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbPitchEnvHold.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialPitchEnvDecay.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbPitchEnvDecay.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialPitchEnvSustain.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbPitchEnvSustain.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialPitchEnvRelease.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbPitchEnvRelease.valueChanged.connect(self.onUiValueChanged)

    self.ui.cbxAmpEnvAttackShapeEnable.stateChanged.connect(self.onUiValueChanged)
    self.ui.cbxAmpEnvDecayShapeEnable.stateChanged.connect(self.onUiValueChanged)
    self.ui.cbxAmpEnvReleaseShapeEnable.stateChanged.connect(self.onUiValueChanged)

    self.ui.cbxFilEnvAttackShapeEnable.stateChanged.connect(self.onUiValueChanged)
    self.ui.cbxFilEnvDecayShapeEnable.stateChanged.connect(self.onUiValueChanged)
    self.ui.cbxFilEnvReleaseShapeEnable.stateChanged.connect(self.onUiValueChanged)

    self.ui.pbnAmpEnvAttackShapeReset.clicked.connect(self.onUiValueChanged)
    self.ui.pbnAmpEnvDecayShapeReset.clicked.connect(self.onUiValueChanged)
    self.ui.pbnAmpEnvReleaseShapeReset.clicked.connect(self.onUiValueChanged)
    self.ui.pbnFilEnvAttackShapeReset.clicked.connect(self.onUiValueChanged)
    self.ui.pbnFilEnvDecayShapeReset.clicked.connect(self.onUiValueChanged)
    self.ui.pbnFilEnvReleaseShapeReset.clicked.connect(self.onUiValueChanged)

  # UPDATE WIDGET -> OBJECT
  def onUiValueChanged(self):
    obj = self.map_objects[self.ui.listMap.currentRow()]
    match self.sender().objectName():
      # SPINBOXES
      case "sbxKeyLo":
        obj.change_value("map_key_range", [self.sender().value(), obj.map_key_range[1]])
      case "sbxKeyHi":
        obj.change_value("map_key_range", [obj.map_key_range[0], self.sender().value()])
      case "sbxVelLo":
        obj.change_value("map_vel_range", [self.sender().value(), obj.map_vel_range[1]])
      case "sbxVelHi":
        obj.change_value("map_vel_range", [obj.map_vel_range[0], self.sender().value()])
      case "sbxCc":
        obj.change_value("on_cc_range", [self.sender().value(), obj.on_cc_range[1], obj.on_cc_range[2]])
      case "sbxCcLo":
        obj.change_value("on_cc_range", [obj.on_cc_range[0], self.sender().value(), obj.on_cc_range[2]])
      case "sbxCcHi":
        obj.change_value("on_cc_range", [obj.on_cc_range[0], obj.on_cc_range[1], self.sender().value()])
      case "sbxCcLo":
        obj.change_value("on_cc_range", [obj.on_cc_range[0], self.sender().value(), obj.on_cc_range[2]])
      case "dsbRandomLo":
        obj.change_value("random_range", [self.sender().value(), obj.random_range[1]])
      case "dsbRandomHi":
        obj.change_value("random_range", [obj.random_range[0], self.sender().value()])
      case "sbxOutput":
        obj.change_value("output", self.sender().value())
      case "sbxPolyphony":
        obj.change_value("poly", self.sender().value())
      case "sbxNotePolyphony":
        obj.change_value("note_poly", self.sender().value())
      case "sbxKeyswitchCount":
        obj.change_value("keyswitch", self.sender().value())
      case "sbxUsePitchKeycenter4All":
        obj.change_value("keycenter", self.sender().value())
      case "dsbRtDecay":
        obj.change_value("rt_decay", self.sender().value())
      # wavetable
      case "sbxWaveUnison":
        obj.change_value("wave_unison", self.sender().value())
      case "sbxWaveQuality":
        obj.change_value("wave_quality", self.sender().value())
      case "sbxWavePhase":
        obj.change_value("wave_phase", self.sender().value())
      case "sbxWaveModDepth":
        obj.change_value("wave_mod_depth", self.sender().value())
      case "sbxWaveModDepthCc":
        obj.change_value("wave_mod_depth_cc", [self.sender().value(), obj.wave_mod_depth_cc[1]])
      case "sbxWaveModDepthCcVal":
        obj.change_value("wave_mod_depth_cc", [obj.wave_mod_depth_cc[0], self.sender().value()])
      case "sbxWaveDetune":
        obj.change_value("wave_detune", self.sender().value())
      case "sbxWaveDetuneCc":
        obj.change_value("wave_detune_cc", [self.sender().value(), obj.wave_detune_cc[1]])
      case "sbxWaveDetuneCcVal":
        obj.change_value("wave_detune_cc", [obj.wave_detune_cc[0], self.sender().value()])
      # sample
      case "dsbSampleMapDelay":
        obj.change_value("delay", self.sender().value())
      case "sbxSampleQuality":
        obj.change_value("quality", self.sender().value())
      case "sbxSampleOffsetValue":
        obj.change_value("offset", self.sender().value())
      case "sbxSampleOffsetRandom":
        obj.change_value("offset_random", self.sender().value())
      case "sbxSampleOffsetVelocity":
        obj.change_value("vel2offset", self.sender().value())
      case "sbxSampleTransposePitch":
        obj.change_value("pitch_transpose", self.sender().value())
      case "sbxSampleTransposeNote":
        obj.change_value("note_offset", self.sender().value())
      # exclusive class
      case "sbxGroup":
        obj.change_value("group", self.sender().value())
      case "sbxOffBy":
        obj.change_value("off_by", self.sender().value())
      case "dsbOffTime":
        obj.change_value("off_time", self.sender().value())
      # pan
      case "sbxPanKeycenter":
        obj.change_value("pan_keycenter", self.sender().value())
      # amp
      case "sbxAmpKeycenter":
        obj.change_value("amp_keycenter", self.sender().value())
      case "sbxAmpVelFloor":
        obj.change_value("amp_velfloor", self.sender().value())
      case "sbxAmpVelAttack":
        obj.change_value("amp_env_vel2attack", self.sender().value())
      case "sbxFilterKeycenter":
        obj.change_value("fil_keycenter", self.sender().value())

      # BOOLEANS
      case "chkNoteOn":
        obj.change_value("on_cc_rangebool", self.sender().isChecked())
      case "chkRandom":
        obj.change_value("random_rangebool", self.sender().isChecked())
      case "chkPolyphony":
        obj.change_value("polybool", self.sender().isChecked())
      case "chkNotePolyphony":
        obj.change_value("note_polybool", self.sender().isChecked())
      case "chkNoteSelfmask":
        obj.change_value("note_selfmask", self.sender().isChecked())
      case "chkKeyswitchCount":
        obj.change_value("keyswitchbool", self.sender().isChecked())
      case "chkRtDead":
        obj.change_value("rt_dead", self.sender().isChecked())
      case "chkRtDecay":
        obj.change_value("rt_decaybool", self.sender().isChecked())
      case "chkUseGlobalPitchKeycenter":
        obj.change_value("keycenterbool", self.sender().isChecked())
      case "chkUseKey":
        obj.change_value("key_opcode", self.sender().isChecked())
      case "chkSampleOffsetValue":
        obj.change_value("offsetbool", self.sender().isChecked())
      case "chkRegionExclusiveClass":
        obj.change_value("exclass", self.sender().isChecked())
      case "gbxPan":
        obj.change_value("panbool", self.sender().isChecked())
      case "chkAmpVelFloor":
        obj.change_value("amp_velfloorbool", self.sender().isChecked())
      case "chkAmpVelAttack":
        obj.change_value("amp_env_vel2attackbool", self.sender().isChecked())
      case "gbxAmpLfo":
        obj.change_value("amp_lfo", self.sender().isChecked())
      case "gbxAmpEnv":
        obj.change_value("amp_env", self.sender().isChecked())
      case "gbxFilterGeneral":
        obj.change_value("fil", self.sender().isChecked())
      case "gbxFilterLfo":
        obj.change_value("fil_lfo", self.sender().isChecked())
      case "gbxFilEnv":
        obj.change_value("fil_env", self.sender().isChecked())
      case "gbxPitch":
        obj.change_value("pitch", self.sender().isChecked())
      case "gbxPitchLfo":
        obj.change_value("pit_lfo", self.sender().isChecked())
      case "gbxPitchEnv":
        obj.change_value("pit_env", self.sender().isChecked())

      case "cbxAmpEnvAttackShapeEnable":
        obj.change_value("amp_env_attack_shapebool", self.sender().isChecked())
      case "cbxAmpEnvDecayShapeEnable":
        obj.change_value("amp_env_decay_shapebool", self.sender().isChecked())
      case "cbxAmpEnvReleaseShapeEnable":
        obj.change_value("amp_env_release_shapebool", self.sender().isChecked())

      case "cbxFilEnvAttackShapeEnable":
        obj.change_value("fil_env_attack_shapebool", self.sender().isChecked())
      case "cbxFilEnvDecayShapeEnable":
        obj.change_value("fil_env_decay_shapebool", self.sender().isChecked())
      case "cbxFilEnvReleaseShapeEnable":
        obj.change_value("fil_env_release_shapebool", self.sender().isChecked())

      # COMBO BOXES
      case "cbxWave":
        obj.change_value("wave", wavetables[self.sender().currentIndex()])
      case "cbxWaveMode":
        obj.change_value("wave_mode", wave_modes[self.sender().currentIndex()])
      case "cbxTriggerMode":
        obj.change_value("trigger", trigger_modes[self.sender().currentIndex()])
      case "cbxLoopMode":
        obj.change_value("loop_mode", loop_modes[self.sender().currentIndex()])
      case "cbxDirection":
        obj.change_value("direction", loop_directions[self.sender().currentIndex()])
      case "cbxOffMode":
        obj.change_value("off_mode", off_modes[self.sender().currentIndex()])
      case "cbxFilterType":
        obj.change_value("fil_type", filter_type[self.sender().currentIndex()])

      # TEXT
      case "txtKeyswitchLabel":
        obj.change_value("sw_label", self.sender().text())
      case "txtOpcodes":
        obj.change_value("opcode_notepad", f"'{self.sender().toPlainText()}'")

      # KNOBS / DIALS
      # PAN
      case "dialPan":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbPan.setValue(val)
        obj.change_value("pan_value", val)
      case "dsbPan":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialPan.setValue(val)
        obj.change_value("pan_value", val)
      case "dialPanKeytrack":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbPanKeytrack.setValue(val)
        obj.change_value("pan_keytrack", val)
      case "dsbPanKeytrack":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialPanKeytrack.setValue(val)
        obj.change_value("pan_keytrack", val)
      case "dialPanVeltrack":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbPanVeltrack.setValue(val)
        obj.change_value("pan_veltrack", val)
      case "dsbPanVeltrack":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialPanVeltrack.setValue(val)
        obj.change_value("pan_veltrack", val)
      case "dialPanRandom":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbPanRandom.setValue(val)
        obj.change_value("pan_random", val)
      case "dsbPanRandom":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialPanRandom.setValue(val)
        obj.change_value("pan_random", val)

      # AMP
      case "dialAmpKeytrack":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpKeytrack.setValue(val)
        obj.change_value("amp_keytrack", val)
      case "dsbAmpKeytrack":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpKeytrack.setValue(val)
        obj.change_value("amp_keytrack", val)
      case "dialAmpVeltrack":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpVeltrack.setValue(val)
        obj.change_value("amp_veltrack", val)
      case "dsbAmpVeltrack":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpVeltrack.setValue(val)
        obj.change_value("amp_veltrack", val)
      case "dialAmpRandom":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpRandom.setValue(val)
        obj.change_value("amp_random", val)
      case "dsbAmpRandom":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpRandom.setValue(val)
        obj.change_value("amp_random", val)

      # AMP LFO
      case "dialAmpLfoDelay":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpLfoDelay.setValue(val)
        obj.change_value("amp_lfo_delay", val)
      case "dsbAmpLfoDelay":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpLfoDelay.setValue(val)
        obj.change_value("amp_lfo_delay", val)
      case "dialAmpLfoFade":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpLfoFade.setValue(val)
        obj.change_value("amp_lfo_fade", val)
      case "dsbAmpLfoFade":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpLfoFade.setValue(val)
        obj.change_value("amp_lfo_fade", val)
      case "dialAmpLfoDepth":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpLfoDepth.setValue(val)
        obj.change_value("amp_lfo_depth", val)
      case "dsbAmpLfoDepth":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpLfoDepth.setValue(val)
        obj.change_value("amp_lfo_depth", val)
      case "dialAmpLfoFreq":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpLfoFreq.setValue(val)
        obj.change_value("amp_lfo_freq", val)
      case "dsbAmpLfoFreq":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpLfoFreq.setValue(val)
        obj.change_value("amp_lfo_freq", val)

      # AMP ENVELOPE
      case "sldAmpEnvStart":
        obj.change_value("amp_env_start", self.sender().value())

      case "dialAmpEnvDelay":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpEnvDelay.setValue(val)
        obj.change_value("amp_env_delay", val)
      case "dsbAmpEnvDelay":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpEnvDelay.setValue(val)
        obj.change_value("amp_env_delay", val)

      case "dialAmpEnvAttack":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpEnvAttack.setValue(val)
        obj.change_value("amp_env_attack", val)
      case "dsbAmpEnvAttack":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpEnvAttack.setValue(val)
        obj.change_value("amp_env_attack", val)

      case "dialAmpEnvAttackShape":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpEnvAttackShape.setValue(val)
        obj.change_value("amp_env_attack_shape", val)
      case "dsbAmpEnvAttackShape":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpEnvAttackShape.setValue(val)
        obj.change_value("amp_env_attack_shape", val)

      case "dialAmpEnvHold":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpEnvHold.setValue(val)
        obj.change_value("amp_env_hold", val)
      case "dsbAmpEnvHold":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpEnvHold.setValue(val)
        obj.change_value("amp_env_hold", val)

      case "dialAmpEnvDecay":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpEnvDecay.setValue(val)
        obj.change_value("amp_env_decay", val)
      case "dsbAmpEnvDecay":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpEnvDecay.setValue(val)
        obj.change_value("amp_env_decay", val)

      case "dialAmpEnvDecayShape":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpEnvDecayShape.setValue(val)
        obj.change_value("amp_env_decay_shape", val)
      case "dsbAmpEnvDecayShape":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpEnvDecayShape.setValue(val)
        obj.change_value("amp_env_decay_shape", val)

      case "dialAmpEnvSustain":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpEnvSustain.setValue(val)
        obj.change_value("amp_env_sustain", val)
      case "dsbAmpEnvSustain":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpEnvSustain.setValue(val)
        obj.change_value("amp_env_sustain", val)

      case "dialAmpEnvRelease":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpEnvRelease.setValue(val)
        obj.change_value("amp_env_sustain", val)
      case "dsbAmpEnvRelease":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpEnvRelease.setValue(val)
        obj.change_value("amp_env_sustain", val)

      case "dialAmpEnvReleaseShape":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpEnvReleaseShape.setValue(val)
        obj.change_value("amp_env_sustain", val)
      case "dsbAmpEnvReleaseShape":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpEnvReleaseShape.setValue(val)
        obj.change_value("amp_env_sustain", val)

      # FILTER
      case "dialFilterCutoff":
        self.ui.sbxFilterCutoff.setValue(self.sender().value())
        obj.change_value("cutoff", self.sender().value())
      case "sbxFilterCutoff":
        self.ui.dialFilterCutoff.setValue(self.sender().value())
        obj.change_value("cutoff", self.sender().value())

      case "dialFilterResonance":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbFilterResonance.setValue(val)
        obj.change_value("resonance", val)
      case "dsbFilterResonance":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialFilterResonance.setValue(val)
        obj.change_value("resonance", val)

      case "dialFilterKeytrack":
        self.ui.sbxFilterKeytrack.setValue(self.sender().value())
        obj.change_value("fil_keytrack", self.sender().value())
      case "sbxFilterKeytrack":
        self.ui.dialFilterKeytrack.setValue(self.sender().value())
        obj.change_value("fil_keytrack", self.sender().value())
      case "dialFilterVeltrack":
        self.ui.sbxFilterVeltrack.setValue(self.sender().value())
        obj.change_value("fil_veltrack", self.sender().value())
      case "sbxFilterVeltrack":
        self.ui.dialFilterVeltrack.setValue(self.sender().value())
        obj.change_value("fil_veltrack", self.sender().value())
      case "dialFilterRandom":
        self.ui.sbxFilterRandom.setValue(self.sender().value())
        obj.change_value("fil_random", self.sender().value())
      case "sbxFilterRandom":
        self.ui.dialFilterRandom.setValue(self.sender().value())
        obj.change_value("fil_random", self.sender().value())

      # FILTER LFO
      case "dialFilterLfoDelay":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpLfoDelay.setValue(val)
        obj.change_value("fil_lfo_delay", val)
      case "dsbFilterLfoDelay":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpLfoDelay.setValue(val)
        obj.change_value("fil_lfo_delay", val)
      case "dialFilterLfoFade":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbFilterLfoFade.setValue(val)
        obj.change_value("fil_lfo_fade", val)
      case "dsbFilterLfoFade":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialFilterLfoFade.setValue(val)
        obj.change_value("fil_lfo_fade", val)
      case "dialFilterLfoDepth":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbFilterLfoDepth.setValue(val)
        obj.change_value("fil_lfo_depth", val)
      case "dsbFilterLfoDepth":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialFilterLfoDepth.setValue(val)
        obj.change_value("fil_lfo_depth", val)
      case "dialFilterLfoFreq":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbFilterLfoFreq.setValue(val)
        obj.change_value("fil_lfo_freq", val)
      case "dsbFilterLfoFreq":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialFilterLfoFreq.setValue(val)
        obj.change_value("fil_lfo_freq", val)

      # FILTER ENVELOPE
      case "dialFilEnvDepth":
        self.ui.sbxFilEnvDepth.setValue(self.sender().value())
        obj.change_value("fil_env_depth", self.sender().value())
      case "sbxFilEnvDepth":
        self.ui.dialFilEnvDepth.setValue(self.sender().value())
        obj.change_value("fil_env_depth", self.sender().value())

      case "dialFilEnvDepthVel":
        self.ui.sbxFilEnvDepthVel.setValue(self.sender().value())
        obj.change_value("fil_vel2depth", self.sender().value())
      case "sbxFilEnvDepthVel":
        self.ui.dialFilEnvDepthVel.setValue(self.sender().value())
        obj.change_value("fil_vel2depth", self.sender().value())

      case "sldFilEnvStart":
        obj.change_value("fil_env_start", self.sender().value())

      case "dialFilEnvDelay":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbFilEnvDelay.setValue(val)
        obj.change_value("fil_env_delay", val)
      case "dsbFilEnvDelay":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialFilEnvDelay.setValue(val)
        obj.change_value("fil_env_delay", val)

      case "dialFilEnvAttack":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbFilEnvAttack.setValue(val)
        obj.change_value("fil_env_attack", val)
      case "dsbFilEnvAttack":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialFilEnvAttack.setValue(val)
        obj.change_value("fil_env_attack", val)

      case "dialFilEnvAttackShape":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbFilEnvAttackShape.setValue(val)
        obj.change_value("fil_env_attack_shape", val)
      case "dsbFilEnvAttackShape":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialFilEnvAttackShape.setValue(val)
        obj.change_value("fil_env_attack_shape", val)

      case "dialFilEnvHold":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbFilEnvHold.setValue(val)
        obj.change_value("fil_env_hold", val)
      case "dsbFilEnvHold":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialFilEnvHold.setValue(val)
        obj.change_value("fil_env_hold", val)

      case "dialFilEnvDecay":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbFilEnvDecay.setValue(val)
        obj.change_value("fil_env_decay", val)
      case "dsbFilEnvDecay":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialFilEnvDecay.setValue(val)
        obj.change_value("fil_env_decay", val)

      case "dialFilEnvDecayShape":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbFilEnvDecayShape.setValue(val)
        obj.change_value("fil_env_decay_shape", val)
      case "dsbFilEnvDecayShape":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialFilEnvDecayShape.setValue(val)
        obj.change_value("fil_env_decay_shape", val)

      case "dialFilEnvSustain":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbFilEnvSustain.setValue(val)
        obj.change_value("fil_env_sustain", val)
      case "dsbFilEnvSustain":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialFilEnvSustain.setValue(val)
        obj.change_value("fil_env_sustain", val)

      case "dialFilEnvRelease":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbFilEnvRelease.setValue(val)
        obj.change_value("fil_env_sustain", val)
      case "dsbFilEnvRelease":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialFilEnvRelease.setValue(val)
        obj.change_value("fil_env_sustain", val)

      case "dialFilEnvReleaseShape":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbFilEnvReleaseShape.setValue(val)
        obj.change_value("fil_env_sustain", val)
      case "dsbFilEnvReleaseShape":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialFilEnvReleaseShape.setValue(val)
        obj.change_value("fil_env_sustain", val)

      # PITCH
      case "dialPitchKeytrack":
        self.ui.sbxPitchKeytrack.setValue(self.sender().value())
        obj.change_value("pitch_keytrack", self.sender().value())
      case "sbxPitchKeytrack":
        self.ui.dialPitchKeytrack.setValue(self.sender().value())
        obj.change_value("pitch_keytrack", self.sender().value())
      case "dialPitchVeltrack":
        self.ui.sbxPitchVeltrack.setValue(self.sender().value())
        obj.change_value("pitch_veltrack", self.sender().value())
      case "sbxPitchVeltrack":
        self.ui.dialPitchVeltrack.setValue(self.sender().value())
        obj.change_value("pitch_veltrack", self.sender().value())
      case "dialPitchRandom":
        self.ui.sbxPitchRandom.setValue(self.sender().value())
        obj.change_value("pitch_random", self.sender().value())
      case "sbxPitchRandom":
        self.ui.dialPitchRandom.setValue(self.sender().value())
        obj.change_value("pitch_random", self.sender().value())

      # PITCH LFO
      case "dialPitchLfoDelay":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpLfoDelay.setValue(val)
        obj.change_value("pit_lfo_delay", val)
      case "dsbPitchLfoDelay":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpLfoDelay.setValue(val)
        obj.change_value("pit_lfo_delay", val)
      case "dialPitchLfoFade":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbPitchLfoFade.setValue(val)
        obj.change_value("pit_lfo_fade", val)
      case "dsbPitchLfoFade":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialPitchLfoFade.setValue(val)
        obj.change_value("pit_lfo_fade", val)
      case "dialPitchLfoDepth":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbPitchLfoDepth.setValue(val)
        obj.change_value("pit_lfo_depth", val)
      case "dsbPitchLfoDepth":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialPitchLfoDepth.setValue(val)
        obj.change_value("pit_lfo_depth", val)
      case "dialPitchLfoFreq":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbPitchLfoFreq.setValue(val)
        obj.change_value("pit_lfo_freq", val)
      case "dsbPitchLfoFreq":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialPitchLfoFreq.setValue(val)
        obj.change_value("pit_lfo_freq", val)

      # PITCH ENVELOPE
      case "dialPitchEnvDepth":
        self.ui.sbxPitchEnvDepth.setValue(self.sender().value())
        obj.change_value("pit_env_depth", self.sender().value())
      case "sbxPitchEnvDepth":
        self.ui.dialPitchEnvDepth.setValue(self.sender().value())
        obj.change_value("pit_env_depth", self.sender().value())

      case "sldPitchEnvStart":
        obj.change_value("pit_env_start", self.sender().value())

      case "dialPitchEnvDelay":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbPitchEnvDelay.setValue(val)
        obj.change_value("pit_env_delay", val)
      case "dsbPitchEnvDelay":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialPitchEnvDelay.setValue(val)
        obj.change_value("pit_env_delay", val)

      case "dialPitchEnvAttack":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbPitchEnvAttack.setValue(val)
        obj.change_value("pit_env_attack", val)
      case "dsbPitchEnvAttack":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialPitchEnvAttack.setValue(val)
        obj.change_value("pit_env_attack", val)

      case "dialPitchEnvHold":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbPitchEnvHold.setValue(val)
        obj.change_value("pit_env_hold", val)
      case "dsbPitchEnvHold":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialPitchEnvHold.setValue(val)
        obj.change_value("pit_env_hold", val)

      case "dialPitchEnvDecay":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbPitchEnvDecay.setValue(val)
        obj.change_value("pit_env_decay", val)
      case "dsbPitchEnvDecay":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialPitchEnvDecay.setValue(val)
        obj.change_value("pit_env_decay", val)

      case "dialPitchEnvSustain":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbPitchEnvSustain.setValue(val)
        obj.change_value("pit_env_sustain", val)
      case "dsbPitchEnvSustain":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialPitchEnvSustain.setValue(val)
        obj.change_value("pit_env_sustain", val)

      case "dialPitchEnvRelease":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbPitchEnvRelease.setValue(val)
        obj.change_value("pit_env_sustain", val)
      case "dsbPitchEnvRelease":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialPitchEnvRelease.setValue(val)
        obj.change_value("pit_env_sustain", val)

      # Reset buttons
      case "pbnAmpEnvAttackShapeReset":
        self.ui.dialAmpEnvAttackShape.setValue(0)
        self.ui.dsbAmpEnvAttackShape.setValue(0.0)
        obj.change_value("amp_env_attack_shape", 0)
      case "pbnAmpEnvDecayShapeReset":
        val = float_to_int(-10.361, 3)
        self.ui.dialAmpEnvDecayShape.setValue(val)
        self.ui.dsbAmpEnvDecayShape.setValue(-10.361)
        obj.change_value("amp_env_decay_shape", val)
      case "pbnAmpEnvReleaseShapeReset":
        val = float_to_int(-10.361, 3)
        self.ui.dialAmpEnvReleaseShape.setValue(val)
        self.ui.dsbAmpEnvReleaseShape.setValue(-10.361)
        obj.change_value("amp_env_release_shape", val)

      case "pbnFilEnvAttackShapeReset":
        self.ui.dialFilEnvAttackShape.setValue(0)
        self.ui.dsbFilEnvAttackShape.setValue(0.0)
        obj.change_value("fil_env_attack_shape", 0)
      case "pbnFilEnvDecayShapeReset":
        self.ui.dialFilEnvDecayShape.setValue(0)
        self.ui.dsbFilEnvDecayShape.setValue(0.0)
        obj.change_value("fil_env_decay_shape", 0)
      case "pbnFilEnvReleaseShapeReset":
        self.ui.dialFilEnvReleaseShape.setValue(0)
        self.ui.dsbFilEnvReleaseShape.setValue(0.0)
        obj.change_value("fil_env_release_shape", 0)

      case _:
        None

