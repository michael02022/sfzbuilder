# Copyright (c) 2024 Andrea Zanellato, michael02022
# SPDX-License-Identifier: BSD-3-Clause

# This Python file uses the following encoding: utf-8
from PySide6.QtCore           import QSettings, Qt, QEvent
from PySide6.QtGui            import QIcon, QCursor, QAction, QHoverEvent
from PySide6.QtWidgets        import QMainWindow, QFileDialog, QMessageBox, QApplication, QButtonGroup, QMenu
from .ui_mainwindow           import Ui_MainWindow
#from .tabpan                 import setupKnobs
from .rc_resources            import *
from collections              import defaultdict
from utils.functions          import *
from utils.classes.mapping    import Mapping
from utils.classes.sfzglobal  import SfzGlobal
from utils.enums              import *
from utils.constants          import *
import os
import copy
import math

class MainWindow(QMainWindow):
  def __init__(self, app, parent=None):
    super().__init__(parent)
    self._window = parent

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
    #self.ui.actSave.setIcon(QIcon.fromTheme("document-save",      QIcon(":/document-save")))
    #self.ui.actSaveAs.setIcon(QIcon.fromTheme("document-save-as", QIcon(":/document-save-as")))
    self.ui.actQuit.setIcon(QIcon.fromTheme("application-exit",   QIcon(":/application-exit")))

    self.ui.pbnMapAdd.setIcon(QIcon.fromTheme("list-add",            QIcon(":/list-add")))
    self.ui.pbnMapClone.setIcon(QIcon.fromTheme("edit-copy",         QIcon(":/edit-copy")))
    self.ui.pbnMapDelete.setIcon(QIcon.fromTheme("list-remove",      QIcon(":/list-remove")))
    self.ui.pbnMapDown.setIcon(QIcon.fromTheme("go-down",            QIcon(":/go-down")))
    self.ui.pbnMapImport.setIcon(QIcon.fromTheme("emblem-downloads", QIcon(":/import")))
    self.ui.pbnMapUp.setIcon(QIcon.fromTheme("go-up",                QIcon(":/go-up")))

    # init comboxes
    self.ui.cbxOversampling.clear();self.ui.cbxOversampling.addItems(oversamplings)
    self.ui.cbxTriggerMode.clear();self.ui.cbxTriggerMode.addItems(trigger_modes)
    self.ui.cbxWave.clear();self.ui.cbxWave.addItems(wavetables)
    self.ui.cbxWaveMode.clear();self.ui.cbxWaveMode.addItems(wave_modes)
    self.ui.cbxLoopMode.clear();self.ui.cbxLoopMode.addItems(loop_modes)
    self.ui.cbxDirection.clear();self.ui.cbxDirection.addItems(loop_directions)
    self.ui.cbxOffMode.clear();self.ui.cbxOffMode.addItems(off_modes)
    self.ui.cbxAmpEnvVer.clear();self.ui.cbxAmpEnvVer.addItems(eg_types)
    self.ui.cbxFilterType.clear();self.ui.cbxFilterType.addItems(filter_type)
    self.ui.cbxFilterEnvVer.clear();self.ui.cbxFilterEnvVer.addItems(eg_types)

    self.ui.cbxPanLfoWave.clear();self.ui.cbxPanLfoWave.addItems(lfo_waves)
    self.ui.cbxAmpLfoWave.clear();self.ui.cbxAmpLfoWave.addItems(lfo_waves)
    self.ui.cbxFilterLfoWave.clear();self.ui.cbxFilterLfoWave.addItems(lfo_waves)
    self.ui.cbxPitchLfoWave.clear();self.ui.cbxPitchLfoWave.addItems(lfo_waves)

    self.ui.cbxTwWave.clear();self.ui.cbxTwWave.addItems(tablewarp_wave)
    self.ui.cbxTwWarp.clear();self.ui.cbxTwWarp.addItems(tablewarp_warp)
    self.ui.cbxTwWaveLfoWave.clear();self.ui.cbxTwWaveLfoWave.addItems(lfo_waves)
    self.ui.cbxTwWarpLfoWave.clear();self.ui.cbxTwWarpLfoWave.addItems(lfo_waves)

    # Init folders and mapping dictionary
    self.ui.pbnMainFolder.clicked.connect(self.onMainFolder)
    #self.ui.pbnPresetFolder.clicked.connect(self.onPresetFolder)
    if self.settings.value("mainfolderpath") is not None:
      self.ui.txtMainFolder.setText(self.settings.value("mainfolderpath"))
      #self.ui.lblPresetPrefix.setText(f"{self.settings.value('presetfolderpath')}/")
      self.mappings_dict = get_mappings(self.settings.value("mainfolderpath"))
      self.enable_edit = True
      #print(self.mappings_dict)

    # init global header
    self.global_header = SfzGlobal()
    self.get_global_values()

    self.chk_group.buttonClicked.connect(self.onCheckboxesWavetables)

    self.ui.pbnMapAdd.clicked.connect(self.onMapAdd)
    self.ui.pbnMapDelete.clicked.connect(self.onMapDelete)
    self.ui.pbnMapUp.clicked.connect(self.onMapUp)
    self.ui.pbnMapDown.clicked.connect(self.onMapDown)
    self.ui.pbnMapClone.clicked.connect(self.onMapClone)

    self.ui.cbxPack.activated.connect(self.onPackChanged)
    self.ui.cbxMap.activated.connect(self.onMapChanged)
    self.ui.listMap.itemClicked.connect(self.onItemMap)

    self.ui.btnAutoname.clicked.connect(self.onAutoname)

    # ENVELOPES
    #self.ui.knbPan.setMinimum(-100.0)
    #self.ui.knbPan.setMaximum(100.0)

    self.ui.cbxAmpEnvAttackShapeEnable.stateChanged.connect(self.onAmpEnvAttackShapeEnabled)
    self.ui.cbxAmpEnvDecayShapeEnable.stateChanged.connect(self.onAmpEnvDecayShapeEnabled)
    self.ui.cbxAmpEnvReleaseShapeEnable.stateChanged.connect(self.onAmpEnvReleaseShapeEnabled)

    self.ui.cbxFilEnvAttackShapeEnable.stateChanged.connect(self.onFilEnvAttackShapeEnabled)
    self.ui.cbxFilEnvDecayShapeEnable.stateChanged.connect(self.onFilEnvDecayShapeEnabled)
    self.ui.cbxFilEnvReleaseShapeEnable.stateChanged.connect(self.onFilEnvReleaseShapeEnabled)

    # COLORS
    sfizz_synth_color = "GoldenRod"
    fx_color = "LightSkyBlue"
    self.ui.lblWaveMode.setStyleSheet(f"color : {sfizz_synth_color};")
    self.ui.lblWaveUnison.setStyleSheet(f"color : {sfizz_synth_color};")
    self.ui.lblWaveQuality.setStyleSheet(f"color : {sfizz_synth_color};")
    self.ui.lblWaveModDepth.setStyleSheet(f"color : {sfizz_synth_color};")
    self.ui.lblWaveDetune.setStyleSheet(f"color : {sfizz_synth_color};")
    self.ui.lblWavePhase.setStyleSheet(f"color : {sfizz_synth_color};")
    self.ui.cbxWaveModDepthCc.setStyleSheet(f"color : {sfizz_synth_color};")
    self.ui.cbxWaveDetuneCc.setStyleSheet(f"color : {sfizz_synth_color};")

    self.ui.sbxFxMode.setStyleSheet(f"color : {fx_color};")
    self.ui.lblFx1.setStyleSheet(f"color : {fx_color};")
    self.ui.lblFx2.setStyleSheet(f"color : {fx_color};")
    self.ui.lblFx3.setStyleSheet(f"color : {fx_color};")
    self.ui.lblFx4.setStyleSheet(f"color : {fx_color};")
    self.ui.lblFx5.setStyleSheet(f"color : {fx_color};")
    self.ui.lblFx6.setStyleSheet(f"color : {fx_color};")

    # MENUS
    self.save_menu = QMenu(self)
    save_temp_sfz = self.save_menu.addAction("Save TEMP SFZ")
    self.save_menu.addSeparator()
    save_as_sfz = self.save_menu.addAction("Save as SFZ")
    save_project = self.save_menu.addAction("Save as Project") # 🟩
    self.save_menu.addSeparator()
    open_proj = self.save_menu.addAction("Open Project")

    save_as_sfz.setIcon(QIcon.fromTheme("Save as SFZ", QIcon(":/x-office-document")))
    save_project.setIcon(QIcon.fromTheme("Save as Project", QIcon(":/document-save-as")))
    open_proj.setIcon(QIcon.fromTheme("Open Project", QIcon(":/document-open")))

    save_temp_sfz.triggered.connect(self.onSaveTempfz)
    save_as_sfz.triggered.connect(self.onSaveAsSfz)
    save_project.triggered.connect(self.onSaveProject)

    open_proj.triggered.connect(self.onOpenProject)
    self.ui.actOpen.triggered.connect(self.onOpenProject)

    self.ui.actNew.triggered.connect(self.onNew)

    # cc menu
    self.cc_menu = QMenu(self)
    self.cc_submenu_1 = self.cc_menu.addMenu("0-19")
    self.cc_submenu_2 = self.cc_menu.addMenu("20-31")
    self.cc_submenu_3 = self.cc_menu.addMenu("32-45")
    self.cc_submenu_4 = self.cc_menu.addMenu("46-63")
    self.cc_submenu_5 = self.cc_menu.addMenu("64-79")
    self.cc_submenu_6 = self.cc_menu.addMenu("80-90")
    self.cc_submenu_7 = self.cc_menu.addMenu("91-101")
    self.cc_submenu_8 = self.cc_menu.addMenu("102-119")
    self.cc_submenu_9 = self.cc_menu.addMenu("120-127")
    self.cc_submenu_10 = self.cc_menu.addMenu("SFZ CCs")

    for i in range(len(cc_list)):
      if i <= 19:
        self.btn_action = QAction(self, text=str(cc_list[i]))
        self.cc_submenu_1.addAction(self.btn_action)
      if 20 <= i <= 31:
        self.btn_action = QAction(self, text=str(cc_list[i]))
        self.cc_submenu_2.addAction(self.btn_action)
      if 32 <= i <= 45:
        self.btn_action = QAction(self, text=str(cc_list[i]))
        self.cc_submenu_3.addAction(self.btn_action)
      if 46 <= i <= 63:
        self.btn_action = QAction(self, text=str(cc_list[i]))
        self.cc_submenu_4.addAction(self.btn_action)
      if 64 <= i <= 79:
        self.btn_action = QAction(self, text=str(cc_list[i]))
        self.cc_submenu_5.addAction(self.btn_action)
      if 80 <= i <= 90:
        self.btn_action = QAction(self, text=str(cc_list[i]))
        self.cc_submenu_6.addAction(self.btn_action)
      if 91 <= i <= 101:
        self.btn_action = QAction(self, text=str(cc_list[i]))
        self.cc_submenu_7.addAction(self.btn_action)
      if 102 <= i <= 119:
        self.btn_action = QAction(self, text=str(cc_list[i]))
        self.cc_submenu_8.addAction(self.btn_action)
      if 120 <= i <= 127:
        self.btn_action = QAction(self, text=str(cc_list[i]))
        self.cc_submenu_9.addAction(self.btn_action)
      if 128 <= i <= 137:
        self.btn_action = QAction(self, text=str(cc_list[i]))
        self.cc_submenu_10.addAction(self.btn_action)

    # drum menu
    self.drum_menu = QMenu(self)
    self.drum_submenu_1 = self.drum_menu.addMenu("Low Perc (XG)")
    for i in range(len(xg_list_1)):
        self.prc_action = QAction(self, text=str(xg_list_1[i]))
        self.drum_submenu_1.addAction(self.prc_action)
    self.drum_submenu_2 = self.drum_menu.addMenu("Low Perc (GS)")
    for i in range(len(gs_list_1)):
        self.prc_action = QAction(self, text=str(gs_list_1[i]))
        self.drum_submenu_2.addAction(self.prc_action)
    self.drum_submenu_3 = self.drum_menu.addMenu("GM Drums")
    for i in range(len(gm_list_drums)):
        self.prc_action = QAction(self, text=str(gm_list_drums[i]))
        self.drum_submenu_3.addAction(self.prc_action)
    self.drum_submenu_4 = self.drum_menu.addMenu("GM Cymbals")
    for i in range(len(gm_list_cym)):
        self.prc_action = QAction(self, text=str(gm_list_cym[i]))
        self.drum_submenu_4.addAction(self.prc_action)
    self.drum_submenu_5 = self.drum_menu.addMenu("GM Perc")
    for i in range(len(gm_list_perc)):
      self.prc_action = QAction(self, text=str(gm_list_perc[i]))
      self.drum_submenu_5.addAction(self.prc_action)

    # Connect
    self.drum_menu.triggered.connect(self.onPercMenu)

    #self.cc_menu.triggered.connect(self.onCcMenu)

    # Event filter
    self.ui.chkUseGlobalPitchKeycenter.installEventFilter(self)
    #self.ui.lblCc.installEventFilter(self)
    #self.ui.cbxWaveModDepthCc.installEventFilter(self)
    #self.ui.cbxWaveDetuneCc.installEventFilter(self)

    self.pitch_keycenter_hover = False
    self.cc_hover = False

  def eventFilter(self, obj, event):
    #print(self.window)
    #print(obj)
    #print(event)
    #print(event.type())
    #print(obj.className())
    #if event.type() == QEvent.MouseButtonRelease:
    if event.type() == QHoverEvent.HoverEnter:
      match obj.objectName():
        case "chkUseGlobalPitchKeycenter":
          self.pitch_keycenter_hover = True
        case s if s in ("lblCc", "cbxWaveModDepthCc", "cbxWaveDetuneCc"):
          self.cc_hover = True

    elif event.type() == QHoverEvent.HoverLeave:
      match obj.objectName():
        case "chkUseGlobalPitchKeycenter":
          self.pitch_keycenter_hover = False
        case s if s in ("lblCc", "cbxWaveModDepthCc", "cbxWaveDetuneCc"):
          self.cc_hover = False
      #print(self.pitch_keycenter_hover

    if obj.objectName().find("dial") and event.type() == QEvent.MouseButtonRelease:
      None
      #print("button released")
    return super().eventFilter(obj, event)

  def mousePressEvent(self, QMouseEvent):
    if QMouseEvent.button() == Qt.RightButton:
      if self.pitch_keycenter_hover:
        self.pitch_keycenter_hover = False
        self.drum_menu.exec(QCursor.pos())
      elif self.cc_hover:
        self.cc_hover = False
        self.cc_menu.exec(QCursor.pos())
      else:
        self.save_menu.exec(QCursor.pos())
      #self.cc_menu.exec(QCursor.pos())
      #self.drum_menu.exec(QCursor.pos())

  def onPercMenu(self, action):
    val = int(only_nums(action.text()[:3]))
    self.ui.sbxUsePitchKeycenter4All.setValue(val)
  '''
  def onCcMenu(self, action, event):
    val = int(only_nums(action.text()[:3]))
    print(event)
  '''

  def onMainFolder(self):
    main_folder_path = QFileDialog.getExistingDirectory(parent=self, caption="Select a SFZBuilder folder", options=QFileDialog.ShowDirsOnly)
    if False in (os.path.exists(f"{main_folder_path}/MappingPool"), os.path.exists(f"{main_folder_path}/Presets"), os.path.exists(f"{main_folder_path}/Projects")):
      self.msgbox_ok.setText("This is not a valid folder. It must include MappingPool, Presets, Projects and Wavetables folders.")
      self.msgbox_ok.exec()
    else:
      self.ui.txtMainFolder.setText(main_folder_path)
      self.settings.setValue("mainfolderpath", main_folder_path)

  def onPresetFolder(self):
    preset_folder_path = QFileDialog.getExistingDirectory(parent=self, caption="Select a preset folder", options=QFileDialog.ShowDirsOnly, dir=f"{self.settings.value('mainfolderpath')}/Presets")
    self.ui.lblPresetPrefix.setText(f"{preset_folder_path}/")
    if preset_folder_path != "":
      self.settings.setValue("presetfolderpath", preset_folder_path)

  def onNew(self):
    self.msgbox_yesno = QMessageBox(self); self.msgbox_yesno.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    self.msgbox_yesno.setText(f"Are you sure you want to make a new project?")
    answer = self.msgbox_yesno.exec()
    match answer:
      case QMessageBox.Yes:
        self.map_objects.clear()
        self.ui.listMap.clear()
      case QMessageBox.No:
        None

  def onMapAdd(self):
    if self.enable_edit:
      self.current_pack_dict = which_pack(self.mappings_dict, self.ui.chkPercussion.isChecked(), self.ui.chkWavetable.isChecked())

      self.pack_ls = list(self.current_pack_dict)

      self.ui.cbxPack.clear(); self.ui.cbxPack.addItems(self.pack_ls)
      self.map_ls = self.current_pack_dict[self.pack_ls[0]]
      self.ui.cbxMap.clear(); self.ui.cbxMap.addItems(reformat_string_paths(self.map_ls))

      # Mapping object creation
      self.sfz_map = Mapping(which_pack(self.mappings_dict, self.ui.chkPercussion.isChecked(), self.ui.chkWavetable.isChecked()))
      self.sfz_map.set_map(list(self.current_pack_dict)[0], self.map_ls[0])
      self.sfz_map.change_type(which_pack_str(self.ui.chkPercussion.isChecked(), self.ui.chkWavetable.isChecked()))
      self.map_objects.append(self.sfz_map)

      self.ui.listMap.clear(); self.ui.listMap.addItems(get_map_names(self.map_objects))
      #print(self.map_objects)
    else:
      self.msgbox_ok.setText("Please select a SFZBuilder folder.")
      self.msgbox_ok.exec()

  def onCheckboxesWavetables(self):
    if self.ui.listMap.count() != 0:
      self.current_pack_dict = which_pack(self.mappings_dict, self.ui.chkPercussion.isChecked(), self.ui.chkWavetable.isChecked())

      self.pack_ls = list(self.current_pack_dict)

      self.ui.cbxPack.clear(); self.ui.cbxPack.addItems(self.pack_ls)
      self.map_ls = self.current_pack_dict[self.pack_ls[0]]
      self.ui.cbxMap.clear(); self.ui.cbxMap.addItems(reformat_string_paths(self.map_ls))

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

  def onMapClone(self):
    if self.ui.listMap.count() != 0:
      idx = self.ui.listMap.currentRow()
      element = copy.deepcopy(self.map_objects[idx])
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
    self.ui.cbxMap.clear(); self.ui.cbxMap.addItems(reformat_string_paths(self.map_ls))

    # update
    if self.ui.listMap.count() != 0:
      idx = self.ui.listMap.currentRow()
      pk_idx = self.ui.cbxPack.currentIndex()
      mp_idx = self.ui.cbxMap.currentIndex()

      self.map_objects[idx].set_map(list(self.current_pack_dict)[pk_idx], self.map_ls[mp_idx])

      self.ui.listMap.clear(); self.ui.listMap.addItems(get_map_names(self.map_objects))
      self.ui.listMap.setCurrentRow(idx)
      # the most horrible line of code I have ever wrote, basically says if the tuned version of the map exists
      if Path(f"""{self.settings.value("mainfolderpath")}/MappingPool/{str(pathlib.Path(f"{self.map_objects[idx].pack}/{self.map_objects[idx].map}").parent).replace(os.sep, '/')}/{pathlib.Path(self.map_objects[idx].map).stem} --TN.sfz""").is_file():
        self.map_objects[idx].change_value("tuned_checkbox", True)
        self.ui.chkTunedVersion.setEnabled(True)
      else:
        self.map_objects[idx].change_value("tuned_checkbox", False)
        self.ui.chkTunedVersion.setEnabled(False)
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
      # the most horrible line of code I have ever wrote
      if Path(f"""{self.settings.value("mainfolderpath")}/MappingPool/{str(pathlib.Path(f"{self.map_objects[idx].pack}/{self.map_objects[idx].map}").parent).replace(os.sep, '/')}/{pathlib.Path(self.map_objects[idx].map).stem} --TN.sfz""").is_file():
        self.map_objects[idx].change_value("tuned_checkbox", True)
        self.ui.chkTunedVersion.setEnabled(True)
      else:
        self.map_objects[idx].change_value("tuned_checkbox", False)
        self.ui.chkTunedVersion.setEnabled(False)
    else:
      None

  def onItemMap(self):
    idx = self.ui.listMap.currentRow()
    # check if the pack/map exist
    try:
      list(get_pack(self.mappings_dict[self.map_objects[idx].type])).index(self.map_objects[idx].pack) # check if pack exist
      get_pack(self.mappings_dict[self.map_objects[idx].type])[self.map_objects[idx].pack].index(self.map_objects[idx].map) # check if map exist
    except ValueError:
      self.msgbox_ok.setText(f"""The pack-map "{self.map_objects[idx].pack}/{self.map_objects[idx].map}" was not found.\nPlease check if the pack exists or the sfz mapping exists.""")
      self.msgbox_ok.exec()
      pk_idx = 0
      mp_idx = 0

      self.current_pack_dict = get_pack(self.mappings_dict[self.map_objects[idx].type])
      self.pack_ls = list(self.current_pack_dict)
      self.map_ls = self.current_pack_dict[self.pack_ls[pk_idx]]

      self.ui.cbxPack.clear(); self.ui.cbxPack.addItems(self.pack_ls)
      self.ui.cbxMap.clear(); self.ui.cbxMap.addItems(reformat_string_paths(self.map_ls))
      self.map_objects[idx].set_map(list(self.current_pack_dict)[pk_idx], self.map_ls[mp_idx])
      self.ui.listMap.clear(); self.ui.listMap.addItems(get_map_names(self.map_objects))
      self.ui.listMap.setCurrentRow(idx)

    # just update the pack/map comboboxes
    match self.map_objects[idx].type:
      case "MSamples":
        self.ui.chkMap.setChecked(True)
      case "PSamples":
        self.ui.chkPercussion.setChecked(True)
      case "Wavetables":
        self.ui.chkWavetable.setChecked(True)

    self.current_pack_dict =  get_pack(self.mappings_dict[self.map_objects[idx].type])

    self.pack_ls = list(self.current_pack_dict)

    self.ui.cbxPack.clear(); self.ui.cbxPack.addItems(self.pack_ls) # add pack list
    self.ui.cbxPack.setCurrentIndex(self.pack_ls.index(self.map_objects[idx].pack)) # set the pack

    self.map_ls = self.current_pack_dict[self.pack_ls[self.ui.cbxPack.currentIndex()]] # add map list
    self.ui.cbxMap.clear(); self.ui.cbxMap.addItems(reformat_string_paths(self.map_ls))
    self.ui.cbxMap.setCurrentIndex(self.map_ls.index(self.map_objects[idx].map)) # set map list
    #mappings_dict
    self.get_map_values()
    # the most horrible line of code I have ever wrote
    if Path(f"""{self.settings.value("mainfolderpath")}/MappingPool/{str(pathlib.Path(f"{self.map_objects[idx].pack}/{self.map_objects[idx].map}").parent).replace(os.sep, '/')}/{pathlib.Path(self.map_objects[idx].map).stem} --TN.sfz""").is_file():
      self.map_objects[idx].change_value("tuned_checkbox", True)
      self.ui.chkTunedVersion.setEnabled(True)
    else:
      self.map_objects[idx].change_value("tuned_checkbox", False)
      self.ui.chkTunedVersion.setEnabled(False)

  def onAutoname(self):
    idx = self.ui.listMap.currentRow()
    self.ui.txtPreset.setText(self.map_objects[idx].get_name_b())

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
  def get_global_values(self):
    global_dict = vars(self.global_header)
    for k in global_dict:
      match k:
        case "keysw":
          self.ui.chkKeyswitch.setChecked(global_dict.get(k))
        case "keysw_range":
          self.ui.sbxKeyswitchLo.setValue(global_dict.get(k)[0])
          self.ui.sbxKeyswitchHi.setValue(global_dict.get(k)[1])
        case "sw_default":
          self.ui.sbxKeyswitchDefault.setValue(global_dict.get(k))
        case "oversampling":
          self.ui.cbxOversampling.setCurrentIndex(oversamplings.index(global_dict.get(k)))

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
        case "wave_mod_depth_ccbool":
          self.ui.cbxWaveModDepthCc.setChecked(map_dict.get(k))
        case "wave_mod_depth_cc":
          self.ui.sbxWaveModDepthCc.setValue(map_dict.get(k)[0])
          self.ui.sbxWaveModDepthCcVal.setValue(map_dict.get(k)[1])
        case "wave_detune":
          self.ui.sbxWaveDetune.setValue(map_dict.get(k))
        case "wave_detune_ccbool":
          self.ui.cbxWaveDetuneCc.setChecked(map_dict.get(k))
        case "wave_detune_cc":
          self.ui.sbxWaveDetuneCc.setValue(map_dict.get(k)[0])
          self.ui.sbxWaveDetuneCcVal.setValue(map_dict.get(k)[1])

        # FX
        case "fx_mode":
          self.ui.sbxFxMode.setValue(map_dict.get(k))
          match map_dict.get(k):
            case 2:
              self.ui.lblFx1.setText("WavePhase:")
            case _:
              self.ui.lblFx1.setText("PanEffect:")
        case "fx_pan":
          self.ui.sbxFxPan.setValue(map_dict.get(k))
        case "fx_detune":
          self.ui.sbxFxDetune.setValue(map_dict.get(k))
        case "fx_delay":
          self.ui.dsbFxDelay.setValue(map_dict.get(k))
        case "fx_speed":
          self.ui.dsbFxSpeed.setValue(map_dict.get(k))
        case "fx_depth":
          self.ui.sbxFxDepth.setValue(map_dict.get(k))
        case "fx_wave":
          self.ui.sbxFxWave.setValue(map_dict.get(k))
        ## MAP
        case "mute":
          self.ui.cbxMapMute.setChecked(map_dict.get(k))
        case "tuned":
          self.ui.chkTunedVersion.setChecked(map_dict.get(k))
        case "tuned_checkbox":
          self.ui.chkTunedVersion.setEnabled(map_dict.get(k))
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
        case "width":
          self.ui.sbxWidth.setValue(map_dict.get(k))
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
        case "tunebool":
          self.ui.cbxTune.setChecked(map_dict.get(k))
        case "tune":
          self.ui.sbxTune.setValue(map_dict.get(k))

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
        case "qualitybool":
          self.ui.chkSampleQuality.setChecked(map_dict.get(k))
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

        ## PAN LFO
        case "pan_lfo":
          self.ui.gbxPanLfo.setChecked(map_dict.get(k))
        case "pan_lfo_delay":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialPanLfoDelay.setValue(dialval)
          self.ui.dsbPanLfoDelay.setValue(map_dict.get(k))
        case "pan_lfo_fade":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialPanLfoFade.setValue(dialval)
          self.ui.dsbPanLfoFade.setValue(map_dict.get(k))
        case "pan_lfo_depth":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialPanLfoDepth.setValue(dialval)
          self.ui.dsbPanLfoDepth.setValue(map_dict.get(k))
        case "pan_lfo_freq":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialPanLfoFreq.setValue(dialval)
          self.ui.dsbPanLfoFreq.setValue(map_dict.get(k))
        case "pan_lfo_wave":
          #print(map_dict.get(k))
          self.ui.cbxPanLfoWave.setCurrentIndex(lfo_waves.index(map_dict.get(k)))

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
        case "amp_lfo_wave":
          self.ui.cbxAmpLfoWave.setCurrentIndex(lfo_waves.index(map_dict.get(k)))

        ## AMP ENV
        case "amp_env":
          self.ui.gbxAmpEnv.setChecked(map_dict.get(k))
        case "amp_env_ver":
          self.ui.cbxAmpEnvVer.setCurrentIndex(map_dict.get(k))
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
        case "amp_env_attack_shapebool":
          self.ui.cbxAmpEnvAttackShapeEnable.setChecked(map_dict.get(k))
        case "amp_env_hold":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialAmpEnvHold.setValue(dialval)
          self.ui.dsbAmpEnvHold.setValue(map_dict.get(k))
        case "amp_env_decay":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialAmpEnvDecay.setValue(dialval)
          self.ui.dsbAmpEnvDecay.setValue(map_dict.get(k))
        case "amp_env_decay_shapebool":
          self.ui.cbxAmpEnvDecayShapeEnable.setChecked(map_dict.get(k))
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
        case "amp_env_release_shapebool":
          self.ui.cbxAmpEnvReleaseShapeEnable.setChecked(map_dict.get(k))
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
        case "fil_lfo_wave":
          self.ui.cbxFilterLfoWave.setCurrentIndex(lfo_waves.index(map_dict.get(k)))

        ## FILTER ENV
        case "fil_env":
          self.ui.gbxFilEnv.setChecked(map_dict.get(k))
        case "fil_env_ver":
          self.ui.cbxFilterEnvVer.setCurrentIndex(map_dict.get(k))

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
        case "fil_env_attack_shapebool":
          self.ui.cbxFilEnvAttackShapeEnable.setChecked(map_dict.get(k))
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
        case "fil_env_decay_shapebool":
          self.ui.cbxFilEnvDecayShapeEnable.setChecked(map_dict.get(k))
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
        case "fil_env_release_shapebool":
          self.ui.cbxFilEnvReleaseShapeEnable.setChecked(map_dict.get(k))
        case "fil_env_release_shape":
          dialval = float_to_int(map_dict.get(k), 3)
          self.ui.dialFilEnvReleaseShape.setValue(dialval)
          self.ui.dsbFilEnvReleaseShape.setValue(map_dict.get(k))

        ## PITCH
        case "pitch":
          self.ui.gbxPitch.setChecked(map_dict.get(k))
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
        case "pit_lfo_wave":
          self.ui.cbxPitchLfoWave.setCurrentIndex(lfo_waves.index(map_dict.get(k)))

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

        ## TABLEWARP
        case "tw_waveform":
          self.ui.cbxTwWave.setCurrentIndex(tablewarp_wave.index(map_dict.get(k)))
        case "tw_waveform_offset":
          self.ui.dsbTwWave.setValue(map_dict.get(k))
        case "tw_warp":
          self.ui.cbxTwWarp.setCurrentIndex(tablewarp_warp.index(map_dict.get(k)))
        case "tw_warp_offset":
          self.ui.dsbTwWarp.setValue(map_dict.get(k))

        case "tw_waveform_eg":
          self.ui.gbxTwEgWave.setChecked(map_dict.get(k))
        case "tw_waveform_eg_depth":
          self.ui.dsbTwEgWaveDepth.setValue(map_dict.get(k))
          #print(map_dict.get(k))
        case "tw_waveform_eg_start":
          self.ui.dsbTwEgWaveStart.setValue(map_dict.get(k))
        case "tw_waveform_eg_delay":
          self.ui.dsbTwEgWaveDelay.setValue(map_dict.get(k))
        case "tw_waveform_eg_attack":
          self.ui.dsbTwEgWaveAttack.setValue(map_dict.get(k))
        case "tw_waveform_eg_attack_shape":
          self.ui.dsbTwEgWaveAttackShape.setValue(map_dict.get(k))
        case "tw_waveform_eg_hold":
          self.ui.dsbTwEgWaveHold.setValue(map_dict.get(k))
        case "tw_waveform_eg_decay":
          self.ui.dsbTwEgWaveDecay.setValue(map_dict.get(k))
        case "tw_waveform_eg_decay_shape":
          self.ui.dsbTwEgWaveDecayShape.setValue(map_dict.get(k))
        case "tw_waveform_eg_sustain":
          self.ui.dsbTwEgWaveSustain.setValue(map_dict.get(k))
        case "tw_waveform_eg_release":
          self.ui.dsbTwEgWaveRelease.setValue(map_dict.get(k))
        case "tw_waveform_eg_release_shape":
          self.ui.dsbTwEgWaveReleaseShape.setValue(map_dict.get(k))

        case "tw_waveform_lfo":
          self.ui.gbxTwLfoWave.setChecked(map_dict.get(k))
        case "tw_waveform_lfo_wave":
          self.ui.cbxTwWaveLfoWave.setCurrentIndex(lfo_waves.index(map_dict.get(k)))
        case "tw_waveform_lfo_delay":
          self.ui.dsbTwWaveLfoDelay.setValue(map_dict.get(k))
        case "tw_waveform_lfo_fade":
          self.ui.dsbTwWaveLfoFade.setValue(map_dict.get(k))
        case "tw_waveform_lfo_depth":
          self.ui.dsbTwWaveLfoDepth.setValue(map_dict.get(k))
        case "tw_waveform_lfo_freq":
          self.ui.dsbTwWaveLfoFreq.setValue(map_dict.get(k))

        case "tw_warp_eg":
          self.ui.gbxTwEgWarp.setChecked(map_dict.get(k))
        case "tw_warp_eg_depth":
          self.ui.dsbTwEgWarpDepth.setValue(map_dict.get(k))
        case "tw_warp_eg_start":
          self.ui.dsbTwEgWarpStart.setValue(map_dict.get(k))
        case "tw_warp_eg_delay":
          self.ui.dsbTwEgWarpDelay.setValue(map_dict.get(k))
        case "tw_warp_eg_attack":
          self.ui.dsbTwEgWarpAttack.setValue(map_dict.get(k))
        case "tw_warp_eg_attack_shape":
          self.ui.dsbTwEgWarpAttackShape.setValue(map_dict.get(k))
        case "tw_warp_eg_hold":
          self.ui.dsbTwEgWarpHold.setValue(map_dict.get(k))
        case "tw_warp_eg_decay":
          self.ui.dsbTwEgWarpDecay.setValue(map_dict.get(k))
        case "tw_warp_eg_decay_shape":
          self.ui.dsbTwEgWarpDecayShape.setValue(map_dict.get(k))
        case "tw_warp_eg_sustain":
          self.ui.dsbTwEgWarpSustain.setValue(map_dict.get(k))
        case "tw_warp_eg_release":
          self.ui.dsbTwEgWarpRelease.setValue(map_dict.get(k))
        case "tw_warp_eg_release_shape":
          self.ui.dsbTwEgWarpReleaseShape.setValue(map_dict.get(k))

        case "tw_warp_lfo":
          self.ui.gbxTwLfoWarp.setChecked(map_dict.get(k))
        case "tw_warp_lfo_wave":
          self.ui.cbxTwWarpLfoWave.setCurrentIndex(lfo_waves.index(map_dict.get(k)))
        case "tw_warp_lfo_delay":
          self.ui.dsbTwWarpLfoDelay.setValue(map_dict.get(k))
        case "tw_warp_lfo_fade":
          self.ui.dsbTwWarpLfoFade.setValue(map_dict.get(k))
        case "tw_warp_lfo_depth":
          self.ui.dsbTwWarpLfoDepth.setValue(map_dict.get(k))
        case "tw_warp_lfo_freq":
          self.ui.dsbTwWarpLfoFreq.setValue(map_dict.get(k))

        ## OPCODES
        case "opcode_notepad":
          self.ui.txtOpcodes.setPlainText(map_dict.get(k))
        case "comment":
          self.ui.txtComment.setText(map_dict.get(k))

    # /// WIDGET MONITORING
    # global header
    self.ui.chkKeyswitch.stateChanged.connect(self.onUiValueChanged)
    self.ui.sbxKeyswitchLo.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxKeyswitchHi.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxKeyswitchDefault.valueChanged.connect(self.onUiValueChanged)
    self.ui.cbxOversampling.currentIndexChanged.connect(self.onUiValueChanged)

    # Spinboxes
    self.ui.dsbVolume.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxKeyLo.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxKeyHi.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxVelLo.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxVelHi.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxCc.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxCcLo.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxCcHi.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbRandomLo.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbRandomHi.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxOutput.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxWidth.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxPolyphony.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxNotePolyphony.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxKeyswitchCount.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxUsePitchKeycenter4All.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbRtDecay.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxTune.valueChanged.connect(self.onUiValueChanged)

    self.ui.sbxWaveUnison.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxWaveQuality.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxWavePhase.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxWaveModDepth.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxWaveModDepthCc.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxWaveModDepthCcVal.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxWaveDetune.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxWaveDetuneCc.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxWaveDetuneCcVal.valueChanged.connect(self.onUiValueChanged)

    self.ui.sbxFxMode.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxFxPan.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxFxDetune.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbFxDelay.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbFxSpeed.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxFxWave.valueChanged.connect(self.onUiValueChanged)
    self.ui.sbxFxDepth.valueChanged.connect(self.onUiValueChanged)

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

    self.ui.dsbTwWave.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbTwWarp.valueChanged.connect(self.onUiValueChanged)

    self.ui.dsbTwEgWaveDepth.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbTwEgWaveStart.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbTwEgWaveDelay.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbTwEgWaveAttack.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbTwEgWaveAttackShape.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbTwEgWaveHold.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbTwEgWaveDecay.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbTwEgWaveDecayShape.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbTwEgWaveSustain.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbTwEgWaveRelease.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbTwEgWaveReleaseShape.valueChanged.connect(self.onUiValueChanged)

    self.ui.dsbTwWaveLfoDelay.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbTwWaveLfoFade.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbTwWaveLfoDepth.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbTwWaveLfoFreq.valueChanged.connect(self.onUiValueChanged)

    self.ui.dsbTwEgWarpDepth.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbTwEgWarpStart.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbTwEgWarpDelay.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbTwEgWarpAttack.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbTwEgWarpAttackShape.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbTwEgWarpHold.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbTwEgWarpDecay.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbTwEgWarpDecayShape.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbTwEgWarpSustain.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbTwEgWarpRelease.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbTwEgWarpReleaseShape.valueChanged.connect(self.onUiValueChanged)

    self.ui.dsbTwWarpLfoDelay.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbTwWarpLfoFade.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbTwWarpLfoDepth.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbTwWarpLfoFreq.valueChanged.connect(self.onUiValueChanged)

    # Checkboxes
    self.ui.cbxMapMute.stateChanged.connect(self.onUiValueChanged)
    self.ui.chkTunedVersion.stateChanged.connect(self.onUiValueChanged)
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
    self.ui.cbxWaveModDepthCc.stateChanged.connect(self.onUiValueChanged)
    self.ui.cbxWaveDetuneCc.stateChanged.connect(self.onUiValueChanged)
    self.ui.cbxTune.stateChanged.connect(self.onUiValueChanged)
    self.ui.chkSampleQuality.stateChanged.connect(self.onUiValueChanged)

    self.ui.gbxPan.toggled.connect(self.onUiValueChanged)
    self.ui.gbxPanLfo.toggled.connect(self.onUiValueChanged)

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

    self.ui.gbxTwEgWave.toggled.connect(self.onUiValueChanged)
    self.ui.gbxTwLfoWave.toggled.connect(self.onUiValueChanged)
    self.ui.gbxTwEgWarp.toggled.connect(self.onUiValueChanged)
    self.ui.gbxTwLfoWarp.toggled.connect(self.onUiValueChanged)

    # ComboBoxes
    self.ui.cbxWave.currentIndexChanged.connect(self.onUiValueChanged)
    self.ui.cbxWaveMode.currentIndexChanged.connect(self.onUiValueChanged)

    self.ui.cbxTriggerMode.currentIndexChanged.connect(self.onUiValueChanged)

    self.ui.cbxLoopMode.currentIndexChanged.connect(self.onUiValueChanged)
    self.ui.cbxDirection.currentIndexChanged.connect(self.onUiValueChanged)

    self.ui.cbxOffMode.currentIndexChanged.connect(self.onUiValueChanged)

    self.ui.cbxFilterType.currentIndexChanged.connect(self.onUiValueChanged)

    self.ui.cbxAmpEnvVer.currentIndexChanged.connect(self.onUiValueChanged)
    self.ui.cbxFilterEnvVer.currentIndexChanged.connect(self.onUiValueChanged)

    self.ui.cbxPanLfoWave.currentIndexChanged.connect(self.onUiValueChanged)
    self.ui.cbxAmpLfoWave.currentIndexChanged.connect(self.onUiValueChanged)
    self.ui.cbxFilterLfoWave.currentIndexChanged.connect(self.onUiValueChanged)
    self.ui.cbxPitchLfoWave.currentIndexChanged.connect(self.onUiValueChanged)

    self.ui.cbxTwWave.currentIndexChanged.connect(self.onUiValueChanged)
    self.ui.cbxTwWarp.currentIndexChanged.connect(self.onUiValueChanged)
    self.ui.cbxTwWaveLfoWave.currentIndexChanged.connect(self.onUiValueChanged)
    self.ui.cbxTwWarpLfoWave.currentIndexChanged.connect(self.onUiValueChanged)

    # Text
    self.ui.txtKeyswitchLabel.textEdited.connect(self.onUiValueChanged)
    self.ui.txtOpcodes.textChanged.connect(self.onUiValueChanged)
    self.ui.txtComment.textChanged.connect(self.onUiValueChanged)

    # KNOBS / DIALS
    self.ui.dialPan.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbPan.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialPanKeytrack.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbPanKeytrack.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialPanVeltrack.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbPanVeltrack.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialPanRandom.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbPanRandom.valueChanged.connect(self.onUiValueChanged)

    self.ui.dialPanLfoDelay.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbPanLfoDelay.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialPanLfoFade.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbPanLfoFade.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialPanLfoDepth.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbPanLfoDepth.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialPanLfoFreq.valueChanged.connect(self.onUiValueChanged)
    self.ui.dsbPanLfoFreq.valueChanged.connect(self.onUiValueChanged)

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

    self.ui.sbxPitchEnvDepth.valueChanged.connect(self.onUiValueChanged)
    self.ui.dialPitchEnvDepth.valueChanged.connect(self.onUiValueChanged)

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
      # GLOBAL HEADER
      case "chkKeyswitch":
        self.global_header.change_value("keysw", self.sender().isChecked())
      case "sbxKeyswitchLo":
        self.global_header.change_value("keysw_range", [self.sender().value(), self.global_header.keysw_range[1]])
      case "sbxKeyswitchHi":
        self.global_header.change_value("keysw_range", [self.global_header.keysw_range[0], self.sender().value()])
      case "sbxKeyswitchDefault":
        self.global_header.change_value("sw_default", self.sender().value())
      case "cbxOversampling":
        self.global_header.change_value("oversampling", oversamplings[self.sender().currentIndex()])
      # SPINBOXES
      case "dsbVolume":
        obj.change_value("volume", self.sender().value())
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
      case "sbxWidth":
        obj.change_value("width", self.sender().value())
      case "sbxPolyphony":
        obj.change_value("poly", self.sender().value())
      case "sbxNotePolyphony":
        obj.change_value("note_poly", self.sender().value())
      case "sbxKeyswitchCount":
        obj.change_value("keyswitch", self.sender().value())
      case "sbxUsePitchKeycenter4All":
        obj.change_value("keycenter", self.sender().value())
        idx = self.ui.listMap.currentRow()
        self.ui.listMap.clear(); self.ui.listMap.addItems(get_map_names(self.map_objects))
        self.ui.listMap.setCurrentRow(idx)
      case "dsbRtDecay":
        obj.change_value("rt_decay", self.sender().value())
      case "sbxTune":
        obj.change_value("tune", self.sender().value())
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

      # fx
      case "sbxFxMode":
        obj.change_value("fx_mode", self.sender().value())
        match obj.fx_mode:
          case 2:
            self.ui.lblFx1.setText("WavePhase:")
          case 3:
            self.ui.lblFx1.setText("WavePhase:")
          case 4:
            self.ui.lblFx1.setText("WavePhase:")
          case _:
            self.ui.lblFx1.setText("PanEffect:")
      case "sbxFxPan":
        obj.change_value("fx_pan", self.sender().value())
      case "sbxFxDetune":
        obj.change_value("fx_detune", self.sender().value())
      case "dsbFxDelay":
        obj.change_value("fx_delay", self.sender().value())
      case "dsbFxSpeed":
        obj.change_value("fx_speed", self.sender().value())
      case "sbxFxWave":
        obj.change_value("fx_wave", self.sender().value())
      case "sbxFxDepth":
        obj.change_value("fx_depth", self.sender().value())

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

      # tablewarp
      case "dsbTwWave":
        obj.change_value("tw_waveform_offset", self.sender().value())
      case "dsbTwWarp":
        obj.change_value("tw_warp_offset", self.sender().value())

      case "dsbTwEgWaveDepth":
        obj.change_value("tw_waveform_eg_depth", self.sender().value())
      case "dsbTwEgWaveStart":
        obj.change_value("tw_waveform_eg_start", self.sender().value())
      case "dsbTwEgWaveDelay":
        obj.change_value("tw_waveform_eg_delay", self.sender().value())
      case "dsbTwEgWaveAttack":
        obj.change_value("tw_waveform_eg_attack", self.sender().value())
      case "dsbTwEgWaveAttackShape":
        obj.change_value("tw_waveform_eg_attack_shape", self.sender().value())
      case "dsbTwEgWaveHold":
        obj.change_value("tw_waveform_eg_hold", self.sender().value())
      case "dsbTwEgWaveDecay":
        obj.change_value("tw_waveform_eg_decay", self.sender().value())
      case "dsbTwEgWaveDecayShape":
        obj.change_value("tw_waveform_eg_decay_shape", self.sender().value())
      case "dsbTwEgWaveSustain":
        obj.change_value("tw_waveform_eg_sustain", self.sender().value())
      case "dsbTwEgWaveRelease":
        obj.change_value("tw_waveform_eg_release", self.sender().value())
      case "dsbTwEgWaveReleaseShape":
        obj.change_value("tw_waveform_eg_release_shape", self.sender().value())

      case "dsbTwWaveLfoDelay":
        obj.change_value("tw_waveform_lfo_delay", self.sender().value())
      case "dsbTwWaveLfoFade":
        obj.change_value("tw_waveform_lfo_fade", self.sender().value())
      case "dsbTwWaveLfoDepth":
        obj.change_value("tw_waveform_lfo_depth", self.sender().value())
      case "dsbTwWaveLfoFreq":
        obj.change_value("tw_waveform_lfo_freq", self.sender().value())

      case "dsbTwEgWarpDepth":
        obj.change_value("tw_warp_eg_depth", self.sender().value())
        #print(self.sender().value())
      case "dsbTwEgWarpStart":
        obj.change_value("tw_warp_eg_start", self.sender().value())
      case "dsbTwEgWarpDelay":
        obj.change_value("tw_warp_eg_delay", self.sender().value())
      case "dsbTwEgWarpAttack":
        obj.change_value("tw_warp_eg_attack", self.sender().value())
      case "dsbTwEgWarpAttackShape":
        obj.change_value("tw_warp_eg_attack_shape", self.sender().value())
      case "dsbTwEgWarpHold":
        obj.change_value("tw_warp_eg_hold", self.sender().value())
      case "dsbTwEgWarpDecay":
        obj.change_value("tw_warp_eg_decay", self.sender().value())
      case "dsbTwEgWarpDecayShape":
        obj.change_value("tw_warp_eg_decay_shape", self.sender().value())
      case "dsbTwEgWarpSustain":
        obj.change_value("tw_warp_eg_sustain", self.sender().value())
      case "dsbTwEgWarpRelease":
        obj.change_value("tw_warp_eg_release", self.sender().value())
      case "dsbTwEgWarpReleaseShape":
        obj.change_value("tw_warp_eg_release_shape", self.sender().value())

      case "dsbTwWarpLfoDelay":
        obj.change_value("tw_warp_lfo_delay", self.sender().value())
      case "dsbTwWarpLfoFade":
        obj.change_value("tw_warp_lfo_fade", self.sender().value())
      case "dsbTwWarpLfoDepth":
        obj.change_value("tw_warp_lfo_depth", self.sender().value())
      case "dsbTwWarpLfoFreq":
        obj.change_value("tw_warp_lfo_freq", self.sender().value())

      # BOOLEANS
      case "cbxMapMute":
        obj.change_value("mute", self.sender().isChecked())
      case "chkTunedVersion":
        #print(f"checkbox {self.sender().isEnabled()} value {self.sender().isChecked()}")
        obj.change_value("tuned_checkbox", self.sender().isEnabled())
        obj.change_value("tuned", self.sender().isChecked())
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
      case "cbxTune":
        obj.change_value("tunebool", self.sender().isChecked())
      case "chkSampleQuality":
        obj.change_value("qualitybool", self.sender().isChecked())
      case "cbxWaveModDepthCc":
        obj.change_value("wave_mod_depth_ccbool", self.sender().isChecked())
      case "cbxWaveDetuneCc":
        obj.change_value("wave_detune_ccbool", self.sender().isChecked())
      case "chkSampleOffsetValue":
        obj.change_value("offsetbool", self.sender().isChecked())
      case "chkRegionExclusiveClass":
        obj.change_value("exclass", self.sender().isChecked())
      case "gbxPan":
        obj.change_value("panbool", self.sender().isChecked())
      case "gbxPanLfo":
        obj.change_value("pan_lfo", self.sender().isChecked())
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

      case "gbxTwEgWave":
        obj.change_value("tw_waveform_eg", self.sender().isChecked())
      case "gbxTwLfoWave":
        obj.change_value("tw_waveform_lfo", self.sender().isChecked())
      case "gbxTwEgWarp":
        obj.change_value("tw_warp_eg", self.sender().isChecked())
      case "gbxTwLfoWarp":
        obj.change_value("tw_warp_lfo", self.sender().isChecked())

      # COMBO BOXES
      case "cbxWave":
        obj.change_value("wave", wavetables[self.sender().currentIndex()])

        idx = self.ui.listMap.currentRow()
        self.ui.listMap.clear(); self.ui.listMap.addItems(get_map_names(self.map_objects))
        self.ui.listMap.setCurrentRow(idx)
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
      case "cbxAmpEnvVer":
        obj.change_value("amp_env_ver", self.sender().currentIndex())
      case "cbxFilterEnvVer":
        obj.change_value("fil_env_ver", self.sender().currentIndex())
      case "cbxPanLfoWave":
        obj.change_value("pan_lfo_wave", self.sender().currentIndex())
      case "cbxAmpLfoWave":
        obj.change_value("amp_lfo_wave", self.sender().currentIndex())
      case "cbxFilterLfoWave":
        obj.change_value("fil_lfo_wave", self.sender().currentIndex())
      case "cbxPitchLfoWave":
        obj.change_value("pit_lfo_wave", self.sender().currentIndex())

      case "cbxTwWave":
        obj.change_value("tw_waveform", tablewarp_wave[self.sender().currentIndex()])
      case "cbxTwWarp":
        obj.change_value("tw_warp", tablewarp_warp[self.sender().currentIndex()])

      case "cbxTwWaveLfoWave":
        obj.change_value("tw_waveform_lfo_wave", lfo_waves[self.sender().currentIndex()])
      case "cbxTwWarpLfoWave":
        obj.change_value("tw_warp_lfo_wave", lfo_waves[self.sender().currentIndex()])

      # TEXT
      case "txtKeyswitchLabel":
        obj.change_value("sw_label", self.sender().text())
      case "txtOpcodes":
        obj.change_value("opcode_notepad", self.sender().toPlainText())
      case "txtComment":
        obj.change_value("comment", self.sender().text())

      # KNOBS / DIALS
      # PAN
      case "dialPan":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbPan.setValue(val)
        obj.change_value("pan_value", val)
      case "dsbPan":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialPan.setValue(val)
        obj.change_value("pan_value", self.sender().value())
      case "dialPanKeytrack":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbPanKeytrack.setValue(val)
        obj.change_value("pan_keytrack", val)
      case "dsbPanKeytrack":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialPanKeytrack.setValue(val)
        obj.change_value("pan_keytrack", self.sender().value())
      case "dialPanVeltrack":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbPanVeltrack.setValue(val)
        obj.change_value("pan_veltrack", val)
      case "dsbPanVeltrack":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialPanVeltrack.setValue(val)
        obj.change_value("pan_veltrack", self.sender().value())
      case "dialPanRandom":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbPanRandom.setValue(val)
        obj.change_value("pan_random", val)
      case "dsbPanRandom":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialPanRandom.setValue(val)
        obj.change_value("pan_random", self.sender().value())

      # PAN LFO
      case "dialPanLfoDelay":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbPanLfoDelay.setValue(val)
        obj.change_value("pan_lfo_delay", val)
      case "dsbPanLfoDelay":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialPanLfoDelay.setValue(val)
        obj.change_value("pan_lfo_delay", self.sender().value())
      case "dialPanLfoFade":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbPanLfoFade.setValue(val)
        obj.change_value("pan_lfo_fade", val)
      case "dsbPanLfoFade":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialPanLfoFade.setValue(val)
        obj.change_value("pan_lfo_fade", self.sender().value())
      case "dialPanLfoDepth":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbPanLfoDepth.setValue(val)
        obj.change_value("pan_lfo_depth", val)
      case "dsbPanLfoDepth":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialPanLfoDepth.setValue(val)
        obj.change_value("pan_lfo_depth", self.sender().value())
      case "dialPanLfoFreq":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbPanLfoFreq.setValue(val)
        obj.change_value("pan_lfo_freq", val)
      case "dsbPanLfoFreq":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialPanLfoFreq.setValue(val)
        obj.change_value("pan_lfo_freq", self.sender().value())

      # AMP
      case "dialAmpKeytrack":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpKeytrack.setValue(val)
        obj.change_value("amp_keytrack", val)
      case "dsbAmpKeytrack":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpKeytrack.setValue(val)
        obj.change_value("amp_keytrack", self.sender().value())
      case "dialAmpVeltrack":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpVeltrack.setValue(val)
        obj.change_value("amp_veltrack", val)
      case "dsbAmpVeltrack":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpVeltrack.setValue(val)
        obj.change_value("amp_veltrack", self.sender().value())
      case "dialAmpRandom":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpRandom.setValue(val)
        obj.change_value("amp_random", val)
      case "dsbAmpRandom":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpRandom.setValue(val)
        obj.change_value("amp_random", self.sender().value())

      # AMP LFO
      case "dialAmpLfoDelay":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpLfoDelay.setValue(val)
        obj.change_value("amp_lfo_delay", val)
      case "dsbAmpLfoDelay":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpLfoDelay.setValue(val)
        obj.change_value("amp_lfo_delay", self.sender().value())
      case "dialAmpLfoFade":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpLfoFade.setValue(val)
        obj.change_value("amp_lfo_fade", val)
      case "dsbAmpLfoFade":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpLfoFade.setValue(val)
        obj.change_value("amp_lfo_fade", self.sender().value())
      case "dialAmpLfoDepth":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpLfoDepth.setValue(val)
        obj.change_value("amp_lfo_depth", val)
      case "dsbAmpLfoDepth":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpLfoDepth.setValue(val)
        obj.change_value("amp_lfo_depth", self.sender().value())
      case "dialAmpLfoFreq":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpLfoFreq.setValue(val)
        obj.change_value("amp_lfo_freq", val)
      case "dsbAmpLfoFreq":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpLfoFreq.setValue(val)
        obj.change_value("amp_lfo_freq", self.sender().value())

      # AMP ENVELOPE
      case "sldAmpEnvStart":
        self.ui.lblAmpEnvStart.setText(str(self.sender().value()))
        obj.change_value("amp_env_start", self.sender().value())

      case "dialAmpEnvDelay":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpEnvDelay.setValue(val)
        obj.change_value("amp_env_delay", val)
      case "dsbAmpEnvDelay":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpEnvDelay.setValue(val)
        obj.change_value("amp_env_delay", self.sender().value())

      case "dialAmpEnvAttack":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpEnvAttack.setValue(val)
        obj.change_value("amp_env_attack", val)
      case "dsbAmpEnvAttack":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpEnvAttack.setValue(val)
        obj.change_value("amp_env_attack", self.sender().value())

      case "dialAmpEnvAttackShape":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpEnvAttackShape.setValue(val)
        obj.change_value("amp_env_attack_shape", val)
      case "dsbAmpEnvAttackShape":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpEnvAttackShape.setValue(val)
        obj.change_value("amp_env_attack_shape", self.sender().value())

      case "dialAmpEnvHold":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpEnvHold.setValue(val)
        obj.change_value("amp_env_hold", val)
      case "dsbAmpEnvHold":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpEnvHold.setValue(val)
        obj.change_value("amp_env_hold", self.sender().value())

      case "dialAmpEnvDecay":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpEnvDecay.setValue(val)
        obj.change_value("amp_env_decay", val)
      case "dsbAmpEnvDecay":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpEnvDecay.setValue(val)
        obj.change_value("amp_env_decay", self.sender().value())

      case "dialAmpEnvDecayShape":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpEnvDecayShape.setValue(val)
        obj.change_value("amp_env_decay_shape", val)
      case "dsbAmpEnvDecayShape":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpEnvDecayShape.setValue(val)
        obj.change_value("amp_env_decay_shape", self.sender().value())

      case "dialAmpEnvSustain":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpEnvSustain.setValue(val)
        obj.change_value("amp_env_sustain", val)
      case "dsbAmpEnvSustain":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpEnvSustain.setValue(val)
        obj.change_value("amp_env_sustain", self.sender().value())

      case "dialAmpEnvRelease":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpEnvRelease.setValue(val)
        obj.change_value("amp_env_release", val)
      case "dsbAmpEnvRelease":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpEnvRelease.setValue(val)
        obj.change_value("amp_env_release", self.sender().value())

      case "dialAmpEnvReleaseShape":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbAmpEnvReleaseShape.setValue(val)
        obj.change_value("amp_env_release_shape", val)
      case "dsbAmpEnvReleaseShape":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialAmpEnvReleaseShape.setValue(val)
        obj.change_value("amp_env_release_shape", self.sender().value())

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
        obj.change_value("resonance", self.sender().value())

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
        obj.change_value("fil_lfo_delay", self.sender().value())
      case "dialFilterLfoFade":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbFilterLfoFade.setValue(val)
        obj.change_value("fil_lfo_fade", val)
      case "dsbFilterLfoFade":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialFilterLfoFade.setValue(val)
        obj.change_value("fil_lfo_fade", self.sender().value())
      case "dialFilterLfoDepth":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbFilterLfoDepth.setValue(val)
        obj.change_value("fil_lfo_depth", val)
      case "dsbFilterLfoDepth":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialFilterLfoDepth.setValue(val)
        obj.change_value("fil_lfo_depth", self.sender().value())
      case "dialFilterLfoFreq":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbFilterLfoFreq.setValue(val)
        obj.change_value("fil_lfo_freq", val)
      case "dsbFilterLfoFreq":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialFilterLfoFreq.setValue(val)
        obj.change_value("fil_lfo_freq", self.sender().value())

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
        self.ui.lblFilEnvStart.setText(str(self.sender().value()))
        obj.change_value("fil_env_start", self.sender().value())

      case "dialFilEnvDelay":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbFilEnvDelay.setValue(val)
        obj.change_value("fil_env_delay", val)
      case "dsbFilEnvDelay":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialFilEnvDelay.setValue(val)
        obj.change_value("fil_env_delay", self.sender().value())

      case "dialFilEnvAttack":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbFilEnvAttack.setValue(val)
        obj.change_value("fil_env_attack", val)
      case "dsbFilEnvAttack":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialFilEnvAttack.setValue(val)
        obj.change_value("fil_env_attack", self.sender().value())

      case "dialFilEnvAttackShape":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbFilEnvAttackShape.setValue(val)
        obj.change_value("fil_env_attack_shape", val)
      case "dsbFilEnvAttackShape":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialFilEnvAttackShape.setValue(val)
        obj.change_value("fil_env_attack_shape", self.sender().value())

      case "dialFilEnvHold":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbFilEnvHold.setValue(val)
        obj.change_value("fil_env_hold", val)
      case "dsbFilEnvHold":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialFilEnvHold.setValue(val)
        obj.change_value("fil_env_hold", self.sender().value())

      case "dialFilEnvDecay":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbFilEnvDecay.setValue(val)
        obj.change_value("fil_env_decay", val)
      case "dsbFilEnvDecay":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialFilEnvDecay.setValue(val)
        obj.change_value("fil_env_decay", self.sender().value())

      case "dialFilEnvDecayShape":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbFilEnvDecayShape.setValue(val)
        obj.change_value("fil_env_decay_shape", val)
      case "dsbFilEnvDecayShape":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialFilEnvDecayShape.setValue(val)
        obj.change_value("fil_env_decay_shape", self.sender().value())

      case "dialFilEnvSustain":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbFilEnvSustain.setValue(val)
        obj.change_value("fil_env_sustain", val)
      case "dsbFilEnvSustain":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialFilEnvSustain.setValue(val)
        obj.change_value("fil_env_sustain", self.sender().value())

      case "dialFilEnvRelease":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbFilEnvRelease.setValue(val)
        obj.change_value("fil_env_release", val)
      case "dsbFilEnvRelease":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialFilEnvRelease.setValue(val)
        obj.change_value("fil_env_release", self.sender().value())

      case "dialFilEnvReleaseShape":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbFilEnvReleaseShape.setValue(val)
        obj.change_value("fil_env_release_shape", val)
      case "dsbFilEnvReleaseShape":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialFilEnvReleaseShape.setValue(val)
        obj.change_value("fil_env_release_shape", self.sender().value())

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
        self.ui.dsbPitchLfoDelay.setValue(val)
        obj.change_value("pit_lfo_delay", val)
      case "dsbPitchLfoDelay":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialPitchLfoDelay.setValue(val)
        obj.change_value("pit_lfo_delay", self.sender().value())
      case "dialPitchLfoFade":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbPitchLfoFade.setValue(val)
        obj.change_value("pit_lfo_fade", val)
      case "dsbPitchLfoFade":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialPitchLfoFade.setValue(val)
        obj.change_value("pit_lfo_fade", self.sender().value())
      case "dialPitchLfoDepth":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbPitchLfoDepth.setValue(val)
        obj.change_value("pit_lfo_depth", val)
      case "dsbPitchLfoDepth":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialPitchLfoDepth.setValue(val)
        obj.change_value("pit_lfo_depth", self.sender().value())
      case "dialPitchLfoFreq":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbPitchLfoFreq.setValue(val)
        obj.change_value("pit_lfo_freq", val)
      case "dsbPitchLfoFreq":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialPitchLfoFreq.setValue(val)
        obj.change_value("pit_lfo_freq", self.sender().value())

      # PITCH ENVELOPE
      case "dialPitchEnvDepth":
        self.ui.sbxPitchEnvDepth.setValue(self.sender().value())
        obj.change_value("pit_env_depth", self.sender().value())
      case "sbxPitchEnvDepth":
        self.ui.dialPitchEnvDepth.setValue(self.sender().value())
        obj.change_value("pit_env_depth", self.sender().value())

      case "sldPitchEnvStart":
        self.ui.lblPitchEnvStart.setText(str(self.sender().value()))
        obj.change_value("pit_env_start", self.sender().value())

      case "dialPitchEnvDelay":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbPitchEnvDelay.setValue(val)
        obj.change_value("pit_env_delay", val)
      case "dsbPitchEnvDelay":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialPitchEnvDelay.setValue(val)
        obj.change_value("pit_env_delay", self.sender().value())

      case "dialPitchEnvAttack":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbPitchEnvAttack.setValue(val)
        obj.change_value("pit_env_attack", val)
      case "dsbPitchEnvAttack":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialPitchEnvAttack.setValue(val)
        obj.change_value("pit_env_attack", self.sender().value())

      case "dialPitchEnvHold":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbPitchEnvHold.setValue(val)
        obj.change_value("pit_env_hold", val)
      case "dsbPitchEnvHold":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialPitchEnvHold.setValue(val)
        obj.change_value("pit_env_hold", self.sender().value())

      case "dialPitchEnvDecay":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbPitchEnvDecay.setValue(val)
        obj.change_value("pit_env_decay", val)
      case "dsbPitchEnvDecay":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialPitchEnvDecay.setValue(val)
        obj.change_value("pit_env_decay", self.sender().value())

      case "dialPitchEnvSustain":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbPitchEnvSustain.setValue(val)
        obj.change_value("pit_env_sustain", val)
      case "dsbPitchEnvSustain":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialPitchEnvSustain.setValue(val)
        obj.change_value("pit_env_sustain", self.sender().value())

      case "dialPitchEnvRelease":
        val = int_to_float(self.sender().value(), 3)
        self.ui.dsbPitchEnvRelease.setValue(val)
        obj.change_value("pit_env_release", val)
      case "dsbPitchEnvRelease":
        val = float_to_int(self.sender().value(), 3)
        self.ui.dialPitchEnvRelease.setValue(val)
        obj.change_value("pit_env_release", self.sender().value())

      # Reset buttons
      case "pbnAmpEnvAttackShapeReset":
        self.ui.dialAmpEnvAttackShape.setValue(0)
        self.ui.dsbAmpEnvAttackShape.setValue(0.0)
        obj.change_value("amp_env_attack_shape", 0)
      case "pbnAmpEnvDecayShapeReset":
        val = float_to_int(DECAY_CURVE_B, 3)
        self.ui.dialAmpEnvDecayShape.setValue(val)
        self.ui.dsbAmpEnvDecayShape.setValue(-7.16)
        obj.change_value("amp_env_decay_shape", -7.16)
      case "pbnAmpEnvReleaseShapeReset":
        val = float_to_int(DECAY_CURVE_B, 3)
        self.ui.dialAmpEnvReleaseShape.setValue(val)
        self.ui.dsbAmpEnvReleaseShape.setValue(DECAY_CURVE_B)
        obj.change_value("amp_env_release_shape", DECAY_CURVE_B)

      case "pbnFilEnvAttackShapeReset":
        self.ui.dialFilEnvAttackShape.setValue(0)
        self.ui.dsbFilEnvAttackShape.setValue(0.0)
        obj.change_value("fil_env_attack_shape", 0)
      case "pbnFilEnvDecayShapeReset":
        self.ui.dialFilEnvDecayShape.setValue(0)
        self.ui.dsbFilEnvDecayShape.setValue(0.0)
        obj.change_value("fil_env_decay_shape", DECAY_CURVE_B)
      case "pbnFilEnvReleaseShapeReset":
        self.ui.dialFilEnvReleaseShape.setValue(0)
        self.ui.dsbFilEnvReleaseShape.setValue(0.0)
        obj.change_value("fil_env_release_shape", DECAY_CURVE_B)

      case _:
        None

  def onSaveAsSfz(self):
    if len(self.map_objects) == 0:
      self.msgbox_ok.setText("Please add a mapping.")
      self.msgbox_ok.exec()
    else:
      projectpath = QFileDialog.getSaveFileName(parent=self, caption="Save SFZ Preset", dir=f"{self.settings.value('mainfolderpath')}/Presets/{self.ui.txtPreset.text()}", filter="SFZ(*.sfz)")
      if projectpath[0] != "":
        #print(projectpath[0])
        self.save_sfz(os.path.dirname(projectpath[0]), os.path.splitext(os.path.basename(projectpath[0]))[0], self.global_header, self.map_objects)
  '''
  def onSaveSfz(self):
    if len(self.map_objects) == 0:
      self.msgbox_ok.setText("Please add a mapping.")
      self.msgbox_ok.exec()
    else:
      self.save_sfz(self.global_header, self.map_objects)
  '''
  def onSaveTempfz(self):
    if len(self.map_objects) == 0:
      self.msgbox_ok.setText("Please add a mapping.")
      self.msgbox_ok.exec()
    else:
      self.save_sfz("", "", self.global_header, self.map_objects, True)

  def save_sfz(self, path, name, global_obj, mappings, temp=False):
    if len(mappings) == 0:
      self.msgbox_ok.setText("Please add a mapping.")
      self.msgbox_ok.exec()
    else:
      self.ui.lblLog.setText(f"Generating SFZ...")
      lfo_idx = 1
      eg_idx = 1

      # calculate the dots for relative path
      config_path = self.settings.value("mainfolderpath")
      if temp:
        preset_path = f"{config_path}/Presets"
      else:
        preset_path = path
        #preset_path = self.settings.value("presetfolderpath")

      common_path = os.path.commonprefix([config_path, preset_path])
      dots = (len(os.path.normpath(preset_path).split(os.sep)) - (len(os.path.normpath(common_path).split(os.sep)) - 1)) - 1
      r = ""
      for i in range(dots):
          r += f"../"
      define_userpath = r[:-1]
      if temp:
        pathstr = f"{preset_path}/!TEMP"
      else:
        pathstr = f"{preset_path}/{name}"
      #print(define_userpath)
      #print(pathstr)

      # generating sfz
      sfz_content = f"//THIS SFZ WAS GENERATED BY SFZBUILDER 0.1.0\n\n"
      sfz_content += f"<control>\n#define $USERPATH {define_userpath}\n"
      if global_obj.oversampling != "x1":
        sfz_content += f"hint_min_samplerate={44100 * (int(oversamplings.index(global_obj.oversampling)) + 1)}\n"
      sfz_content += "\n"

      if global_obj.keysw:
        sfz_global = f"<global>\nsw_lokey={global_obj.keysw_range[0]} sw_hikey={global_obj.keysw_range[1]} sw_default={global_obj.sw_default}\n\n-"
        sfz_content += sfz_global

      for m in mappings:
        if m.mute:
          None
        else:
          sfz_content += f"<master>\n"
          sfz_content += f"lobend={m.bend_range[0]} hibend={m.bend_range[1]}\n"
          sfz_content += f"bend_down={m.pitch_bend_range[0]} bend_up={m.pitch_bend_range[1]}\n\n"
          sfz_content += f"locc133={m.map_key_range[0]} hicc133={m.map_key_range[1]}\n"
          sfz_content += f"locc131={m.map_vel_range[0]} hicc131={m.map_vel_range[1]}\n"
          if m.on_cc_rangebool:
            sfz_content += f"on_locc{m.on_cc_range[0]}={m.on_cc_range[1]} on_hicc{m.on_cc_range[0]}={m.on_cc_range[2]}\n"
          if m.random_rangebool:
            sfz_content += f"lorand={m.random_range[0]} hirand={m.random_range[0]}\n"
          sfz_content += f"volume={m.volume}\n\n"

          # MAP
          if m.polybool:
            sfz_content += f"polyphony={m.poly}\n"
          if m.note_polybool:
            sfz_content += f"note_polyphony={m.note_poly}\n"

          sfz_content += f"output={m.output}\n"
          sfz_content += f"width={m.width}\n"
          sfz_content += f"trigger={m.trigger}\n"
          if m.rt_dead:
            sfz_content += f"rt_dead=on\n"
          if m.rt_decaybool:
            sfz_content += f"rt_decay={m.rt_decay}\n"
          if m.keyswitchbool:
            sfz_content += f"sw_last={m.keyswitch}\n"
            sfz_content += f"sw_label={m.sw_label}\n"
          if m.keycenterbool:
            if m.key_opcode:
              sfz_content += f"key={m.keycenter}\n"
            else:
              sfz_content += f"pitch_keycenter={m.keycenter}\n"
          if m.tunebool:
            sfz_content += f"pitch_oncc119={m.tune}\n"
          # SAMPLE
          #if m.offsetbool:
          sfz_content += f"offset_cc118={m.offset}\n"
          sfz_content += f"offset_random={m.offset_random}\n"
          sfz_content += f"offset_cc131={m.vel2offset}\n\n"
          sfz_content += f"delay={m.delay}\n\n"
          sfz_content += f"transpose={m.pitch_transpose}\n"
          if m.qualitybool:
            sfz_content += f"sample_quality={m.quality}\n"
          if m.loop_mode != "None":
            sfz_content += f"loop_mode={m.loop_mode}\n"
          else:
              pass
          if m.direction != "None":
            sfz_content += f"direction={m.direction}\n"

          if m.exclass:
            sfz_content += "\n\n"
            sfz_content += f"group={m.group}\n"
            sfz_content += f"off_by={m.off_by}\n"
            sfz_content += f"off_mode={m.off_mode}\n"
            sfz_content += f"off_time={m.off_time}\n"

          # PAN
          if m.panbool:
            sfz_content += "\n\n"
            sfz_content += f"pan={m.pan_value}\n"
            sfz_content += f"pan_keycenter={m.pan_keycenter}\n"
            sfz_content += f"pan_keytrack={m.pan_keytrack}\n"
            sfz_content += f"pan_veltrack={m.pan_veltrack}\n"
            sfz_content += f"pan_random={m.pan_random}\n"

            if m.pan_lfo:
              sfz_content += f"lfo{lfo_idx}_delay={m.pan_lfo_delay}\n"
              sfz_content += f"lfo{lfo_idx}_fade={m.pan_lfo_fade}\n"
              sfz_content += f"lfo{lfo_idx}_pan={m.pan_lfo_depth}\n"
              sfz_content += f"lfo{lfo_idx}_freq={m.pan_lfo_freq}\n"
              sfz_content += f"lfo{lfo_idx}_wave={m.pan_lfo_wave}\n"

          # AMP
          sfz_content += "\n\n"
          sfz_content += f"amp_keycenter={m.amp_keycenter}\n"
          sfz_content += f"amp_keytrack={m.amp_keytrack}\n"
          sfz_content += f"amp_veltrack={m.amp_veltrack}\n"
          sfz_content += f"amp_random={m.amp_random}\n"

          if m.amp_lfo:
            sfz_content += "\n\n"
            sfz_content += f"lfo{lfo_idx+1}_delay={m.amp_lfo_delay}\n"
            sfz_content += f"lfo{lfo_idx+1}_fade={m.amp_lfo_fade}\n"
            sfz_content += f"lfo{lfo_idx+1}_volume={m.amp_lfo_depth}\n"
            sfz_content += f"lfo{lfo_idx+1}_freq={m.amp_lfo_freq}\n"
            sfz_content += f"lfo{lfo_idx+1}_wave={m.amp_lfo_wave}\n"
          if m.amp_velfloorbool:
            sfz_content += f"amp_velcurve_1={m.amp_velfloor}\n"
          if m.amp_env_vel2attackbool:
            sfz_content += f"ampeg_vel2attack={m.amp_env_vel2attack}\n"

          if m.amp_env:
            eg_ver = m.amp_env_ver
            shplst = [[m.amp_env_attack_shapebool, m.amp_env_attack_shape], [m.amp_env_decay_shapebool, m.amp_env_decay_shape], [m.amp_env_release_shapebool, m.amp_env_release_shape]]
            sfz_content += generate_eg(eg_ver, "amp", eg_idx, m.amp_env_start, m.amp_env_delay, m.amp_env_attack, m.amp_env_hold, m.amp_env_decay, m.amp_env_sustain, m.amp_env_release, shplst)

          # FILTER
          if m.fil:
            sfz_content += "\n\n"
            sfz_content += f"fil_type={m.fil_type}\n"
            sfz_content += f"cutoff={m.cutoff}\n" # TODO Make the knob exponential for better GUI behavior
            sfz_content += f"resonance={m.resonance}\n\n"

            sfz_content += f"fil_keycenter={m.fil_keycenter}\n"
            sfz_content += f"fil_keytrack={m.fil_keytrack}\n"
            sfz_content += f"fil_veltrack={m.fil_veltrack}\n"
            sfz_content += f"fil_random={m.fil_random}\n"

            if m.fil_lfo:
              sfz_content += "\n\n"
              sfz_content += f"lfo{lfo_idx+2}_delay={m.fil_lfo_delay}\n"
              sfz_content += f"lfo{lfo_idx+2}_fade={m.fil_lfo_fade}\n"
              sfz_content += f"lfo{lfo_idx+2}_cutoff={m.fil_lfo_depth}\n" # Hz
              sfz_content += f"lfo{lfo_idx+2}_freq={m.fil_lfo_freq}\n"
              sfz_content += f"lfo{lfo_idx+2}_wave={m.fil_lfo_wave}\n"

            if m.fil_env:
              eg_ver = m.fil_env_ver
              match m.fil_env_ver:
                case 0:
                  sfz_content += f"fileg_depth={m.fil_env_depth}\n"
                  sfz_content += f"fileg_vel2depth={m.fil_vel2depth}\n"
                case 1:
                  sfz_content += f"eg{eg_idx+2}_cutoff={m.fil_env_depth}\n"
                  sfz_content += f"eg{eg_idx+2}_cutoff_oncc131={m.fil_vel2depth}\n"

              shplst = [[m.fil_env_attack_shapebool, m.fil_env_attack_shape], [m.fil_env_decay_shapebool, m.fil_env_decay_shape], [m.fil_env_release_shapebool, m.fil_env_release_shape]]
              sfz_content += generate_eg(eg_ver, "fil", eg_idx, m.fil_env_start, m.fil_env_delay, m.fil_env_attack, m.fil_env_hold, m.fil_env_decay, m.fil_env_sustain, m.fil_env_release, shplst)

          if m.pitch:
            sfz_content += "\n\n"
            sfz_content += f"pitch_keytrack={m.pitch_keytrack}\n"
            sfz_content += f"pitch_veltrack={m.pitch_veltrack}\n"
            sfz_content += f"pitch_random={m.pitch_random}\n"

            if m.pit_lfo:
              sfz_content += "\n\n"
              sfz_content += f"lfo{lfo_idx+3}_delay={m.pit_lfo_delay}\n"
              sfz_content += f"lfo{lfo_idx+3}_fade={m.pit_lfo_fade}\n"
              sfz_content += f"lfo{lfo_idx+3}_pitch={m.pit_lfo_depth}\n"
              sfz_content += f"lfo{lfo_idx+3}_freq={m.pit_lfo_freq}\n"
              sfz_content += f"lfo{lfo_idx+3}_wave={m.pit_lfo_wave}\n"

            if m.pit_env:
              eg_ver = m.pit_env_ver
              match m.pit_env_ver:
                case 0:
                  sfz_content += f"pitcheg_depth={m.pit_env_depth}\n"
                case 1:
                  sfz_content += f"eg{eg_idx+3}_pitch={m.pit_env_depth}\n"

              #shplst = [[m.pit_env_attack_shapebool, m.pit_env_attack_shape], [m.pit_env_decay_shapebool, m.pit_env_decay_shape], [m.pit_env_release_shapebool, m.pit_env_release_shape]]
              sfz_content += generate_eg(eg_ver, "pit", eg_idx, m.pit_env_start, m.pit_env_delay, m.pit_env_attack, m.pit_env_hold, m.pit_env_decay, m.pit_env_sustain, m.pit_env_release)

          sfz_content += "\n\n"
          sfz_content += "// ADDITIONAL OPCODES\n"
          sfz_content += f"{notepad_opcode_filter(m.opcode_notepad, lfo_idx, eg_idx)}\n\n"

          sfz_content += "//MAPPING\n"
          sfz_content += f"<control>\n"
          # tune
          sfz_content += f"label_cc119=PleaseSetMe127\n"
          sfz_content += f"set_cc119=127\n"
          # offset
          sfz_content += f"label_cc118=PleaseSetMe127\n"
          sfz_content += f"set_cc118=127\n"

          # ###
          if m.type == "Wavetables":
            match m.fx_mode:
              case 0: # NO FX
                sfz_content += f"<group>\n"
                if m.wave == "TableWarp2":
                  sfz_content += f"<region> sample={m.get_wave()}\n"
                  sfz_content += f"sample_dyn_param03={(tablewarp_switch[tablewarp_wave.index(m.tw_waveform)] * 15.875) / 100}\n"
                  sfz_content += f"sample_dyn_param01={m.tw_waveform_offset}\n"

                  if m.tw_waveform_eg:
                    #print(eg_idx)
                    sfz_content += f"eg{eg_idx+4}_sample_dyn_param01={m.tw_waveform_eg_depth}\n"
                    sfz_content += generate_eg_tw(eg_idx+4, m.tw_waveform_eg_start, m.tw_waveform_eg_delay, m.tw_waveform_eg_attack, m.tw_waveform_eg_attack_shape, m.tw_waveform_eg_hold, m.tw_waveform_eg_decay, m.tw_waveform_eg_decay_shape, m.tw_waveform_eg_sustain, m.tw_waveform_eg_release, m.tw_waveform_eg_release_shape)
                  if m.tw_waveform_lfo:
                    sfz_content += "\n\n"
                    sfz_content += f"lfo{lfo_idx+5}_delay={m.tw_waveform_lfo_delay}\n"
                    sfz_content += f"lfo{lfo_idx+5}_fade={m.tw_waveform_lfo_fade}\n"
                    sfz_content += f"lfo{lfo_idx+5}_sample_dyn_param01={m.tw_waveform_lfo_depth / 100}\n"
                    sfz_content += f"lfo{lfo_idx+5}_freq={m.tw_waveform_lfo_freq}\n"
                    sfz_content += f"lfo{lfo_idx+5}_wave={m.tw_waveform_lfo_wave}\n\n"

                  sfz_content += f"sample_dyn_param04={(tablewarp_switch[tablewarp_warp.index(m.tw_warp)] * 15.875) / 100}\n"
                  sfz_content += f"sample_dyn_param02={m.tw_warp_offset}\n"

                  if m.tw_warp_eg:
                    sfz_content += f"eg{eg_idx+5}_sample_dyn_param02={m.tw_warp_eg_depth}\n"
                    sfz_content += generate_eg_tw(eg_idx+5, m.tw_warp_eg_start, m.tw_warp_eg_delay, m.tw_warp_eg_attack, m.tw_warp_eg_attack_shape, m.tw_warp_eg_hold, m.tw_warp_eg_decay, m.tw_warp_eg_decay_shape, m.tw_warp_eg_sustain, m.tw_warp_eg_release, m.tw_warp_eg_release_shape)
                  if m.tw_warp_lfo:
                    sfz_content += "\n\n"
                    sfz_content += f"lfo{lfo_idx+6}_delay={m.tw_warp_lfo_delay}\n"
                    sfz_content += f"lfo{lfo_idx+6}_fade={m.tw_warp_lfo_fade}\n"
                    sfz_content += f"lfo{lfo_idx+6}_sample_dyn_param02={m.tw_warp_lfo_depth / 100}\n"
                    sfz_content += f"lfo{lfo_idx+6}_freq={m.tw_warp_lfo_freq}\n"
                    sfz_content += f"lfo{lfo_idx+6}_wave={m.tw_warp_lfo_wave}\n"
                  sfz_content += "\n"
                else:
                  if m.wave == "Sample":
                    sfz_content += f"<region> sample=$USERPATH/Wavetables/{m.pack}/{m.get_wave()}\n"
                    sfz_content += f"oscillator=on\n"
                  else:
                    sfz_content += f"<region> sample={m.get_wave()}\n"

                  sfz_content += f"oscillator_mode={wave_modes.index(m.wave_mode)} oscillator_quality={m.wave_quality} oscillator_multi={m.wave_unison} oscillator_phase={m.wave_phase / 100}\n"
                  sfz_content += f"oscillator_detune={m.wave_detune}\n"
                  if m.wave_detune_ccbool:
                    sfz_content += f"oscillator_detune_oncc{m.wave_detune_cc[0]}={m.wave_detune_cc[1]}\n"
                  if m.wave_mod_depth_ccbool:
                    sfz_content += f"oscillator_mod_depth_oncc{m.wave_mod_depth_cc[0]}={m.wave_mod_depth_cc[1]}\n"
                  sfz_content += f"oscillator_mod_depth={m.wave_mod_depth}\n\n"
              case 1: # UNISON
                sfz_content += f"<control>\n"
                sfz_content += f"label_cc89=PleaseSetMe127\n" # # FX delay
                sfz_content += f"label_cc90=PleaseSetMe127\n" # # FX tune
                sfz_content += f"set_cc89=127\n"
                sfz_content += f"set_cc90=127\n"
                # OSC 1
                sfz_content += f"<group>\n"
                sfz_content += f"pitch_oncc90={int(m.fx_detune)}\n"
                if m.fx_pan > 0:
                  sfz_content += f"pan={int(m.fx_pan)}\n"
                if m.wave == "TableWarp2":
                  sfz_content += f"<region> sample={m.get_wave()}\n"
                  sfz_content += f"sample_dyn_param03={(tablewarp_switch[tablewarp_wave.index(m.tw_waveform)] * 15.875) / 100}\n"
                  sfz_content += f"sample_dyn_param01={m.tw_waveform_offset}\n"

                  if m.tw_waveform_eg:
                    #print(eg_idx)
                    sfz_content += f"eg{eg_idx+4}_sample_dyn_param01={m.tw_waveform_eg_depth}\n"
                    sfz_content += generate_eg_tw(eg_idx+4, m.tw_waveform_eg_start, m.tw_waveform_eg_delay, m.tw_waveform_eg_attack, m.tw_waveform_eg_attack_shape, m.tw_waveform_eg_hold, m.tw_waveform_eg_decay, m.tw_waveform_eg_decay_shape, m.tw_waveform_eg_sustain, m.tw_waveform_eg_release, m.tw_waveform_eg_release_shape)
                  if m.tw_waveform_lfo:
                    sfz_content += "\n\n"
                    sfz_content += f"lfo{lfo_idx+5}_delay={m.tw_waveform_lfo_delay}\n"
                    sfz_content += f"lfo{lfo_idx+5}_fade={m.tw_waveform_lfo_fade}\n"
                    sfz_content += f"lfo{lfo_idx+5}_sample_dyn_param01={m.tw_waveform_lfo_depth / 100}\n"
                    sfz_content += f"lfo{lfo_idx+5}_freq={m.tw_waveform_lfo_freq}\n"
                    sfz_content += f"lfo{lfo_idx+5}_wave={m.tw_waveform_lfo_wave}\n\n"

                  sfz_content += f"sample_dyn_param04={(tablewarp_switch[tablewarp_warp.index(m.tw_warp)] * 15.875) / 100}\n"
                  sfz_content += f"sample_dyn_param02={m.tw_warp_offset}\n"

                  if m.tw_warp_eg:
                    sfz_content += f"eg{eg_idx+5}_sample_dyn_param02={m.tw_warp_eg_depth}\n"
                    sfz_content += generate_eg_tw(eg_idx+5, m.tw_warp_eg_start, m.tw_warp_eg_delay, m.tw_warp_eg_attack, m.tw_warp_eg_attack_shape, m.tw_warp_eg_hold, m.tw_warp_eg_decay, m.tw_warp_eg_decay_shape, m.tw_warp_eg_sustain, m.tw_warp_eg_release, m.tw_warp_eg_release_shape)
                  if m.tw_warp_lfo:
                    sfz_content += "\n\n"
                    sfz_content += f"lfo{lfo_idx+6}_delay={m.tw_warp_lfo_delay}\n"
                    sfz_content += f"lfo{lfo_idx+6}_fade={m.tw_warp_lfo_fade}\n"
                    sfz_content += f"lfo{lfo_idx+6}_sample_dyn_param02={m.tw_warp_lfo_depth / 100}\n"
                    sfz_content += f"lfo{lfo_idx+6}_freq={m.tw_warp_lfo_freq}\n"
                    sfz_content += f"lfo{lfo_idx+6}_wave={m.tw_warp_lfo_wave}\n"
                  sfz_content += "\n"
                else:
                  if m.wave == "Sample":
                    sfz_content += f"<region> sample=$USERPATH/Wavetables/{m.pack}/{m.get_wave()}\n"
                    sfz_content += f"oscillator=on\n"
                  else:
                    sfz_content += f"<region> sample={m.get_wave()}\n"

                  sfz_content += f"oscillator_mode={wave_modes.index(m.wave_mode)} oscillator_quality={m.wave_quality} oscillator_multi={m.wave_unison} oscillator_phase={m.wave_phase / 100}\n"
                  sfz_content += f"oscillator_detune={m.wave_detune}\n"
                  if m.wave_detune_ccbool:
                    sfz_content += f"oscillator_detune_oncc{m.wave_detune_cc[0]}={m.wave_detune_cc[1]}\n"
                  if m.wave_mod_depth_ccbool:
                    sfz_content += f"oscillator_mod_depth_oncc{m.wave_mod_depth_cc[0]}={m.wave_mod_depth_cc[1]}\n"
                  sfz_content += f"oscillator_mod_depth={m.wave_mod_depth}\n\n"

                # OSC 2
                sfz_content += f"<group>\n"
                sfz_content += f"pitch_oncc90={-abs(int(m.fx_detune))}\n"
                if m.fx_pan > 0:
                  sfz_content += f"pan={-abs(int(m.fx_pan))}\n"
                if m.fx_delay > 0:
                  sfz_content += f"delay_oncc{cc_sw(89, m.fx_delay)}={m.fx_delay}\n"
                if m.wave == "TableWarp2":
                  sfz_content += f"<region> sample={m.get_wave()}\n"
                  sfz_content += f"sample_dyn_param03={(tablewarp_switch[tablewarp_wave.index(m.tw_waveform)] * 15.875) / 100}\n"
                  sfz_content += f"sample_dyn_param01={m.tw_waveform_offset}\n"

                  if m.tw_waveform_eg:
                    #print(eg_idx)
                    sfz_content += f"eg{eg_idx+4}_sample_dyn_param01={m.tw_waveform_eg_depth}\n"
                    sfz_content += generate_eg_tw(eg_idx+4, m.tw_waveform_eg_start, m.tw_waveform_eg_delay, m.tw_waveform_eg_attack, m.tw_waveform_eg_attack_shape, m.tw_waveform_eg_hold, m.tw_waveform_eg_decay, m.tw_waveform_eg_decay_shape, m.tw_waveform_eg_sustain, m.tw_waveform_eg_release, m.tw_waveform_eg_release_shape)
                  if m.tw_waveform_lfo:
                    sfz_content += "\n\n"
                    sfz_content += f"lfo{lfo_idx+5}_delay={m.tw_waveform_lfo_delay}\n"
                    sfz_content += f"lfo{lfo_idx+5}_fade={m.tw_waveform_lfo_fade}\n"
                    sfz_content += f"lfo{lfo_idx+5}_sample_dyn_param01={m.tw_waveform_lfo_depth / 100}\n"
                    sfz_content += f"lfo{lfo_idx+5}_freq={m.tw_waveform_lfo_freq}\n"
                    sfz_content += f"lfo{lfo_idx+5}_wave={m.tw_waveform_lfo_wave}\n\n"

                  sfz_content += f"sample_dyn_param04={(tablewarp_switch[tablewarp_warp.index(m.tw_warp)] * 15.875) / 100}\n"
                  sfz_content += f"sample_dyn_param02={m.tw_warp_offset}\n"

                  if m.tw_warp_eg:
                    sfz_content += f"eg{eg_idx+5}_sample_dyn_param02={m.tw_warp_eg_depth}\n"
                    sfz_content += generate_eg_tw(eg_idx+5, m.tw_warp_eg_start, m.tw_warp_eg_delay, m.tw_warp_eg_attack, m.tw_warp_eg_attack_shape, m.tw_warp_eg_hold, m.tw_warp_eg_decay, m.tw_warp_eg_decay_shape, m.tw_warp_eg_sustain, m.tw_warp_eg_release, m.tw_warp_eg_release_shape)
                  if m.tw_warp_lfo:
                    sfz_content += "\n\n"
                    sfz_content += f"lfo{lfo_idx+6}_delay={m.tw_warp_lfo_delay}\n"
                    sfz_content += f"lfo{lfo_idx+6}_fade={m.tw_warp_lfo_fade}\n"
                    sfz_content += f"lfo{lfo_idx+6}_sample_dyn_param02={m.tw_warp_lfo_depth / 100}\n"
                    sfz_content += f"lfo{lfo_idx+6}_freq={m.tw_warp_lfo_freq}\n"
                    sfz_content += f"lfo{lfo_idx+6}_wave={m.tw_warp_lfo_wave}\n"
                  sfz_content += "\n"
                else:
                  if m.wave == "Sample":
                    sfz_content += f"<region> sample=$USERPATH/Wavetables/{m.pack}/{m.get_wave()}\n"
                    sfz_content += f"oscillator=on\n"
                  else:
                    sfz_content += f"<region> sample={m.get_wave()}\n"

                  sfz_content += f"oscillator_mode={wave_modes.index(m.wave_mode)} oscillator_quality={m.wave_quality} oscillator_multi={m.wave_unison} oscillator_phase={m.wave_phase / 100}\n"
                  sfz_content += f"oscillator_detune={m.wave_detune}\n"
                  if m.wave_detune_ccbool:
                    sfz_content += f"oscillator_detune_oncc{m.wave_detune_cc[0]}={m.wave_detune_cc[1]}\n"
                  if m.wave_mod_depth_ccbool:
                    sfz_content += f"oscillator_mod_depth_oncc{m.wave_mod_depth_cc[0]}={m.wave_mod_depth_cc[1]}\n"
                  sfz_content += f"oscillator_mod_depth={m.wave_mod_depth}\n\n"
              case 2: # MONO CHORUS
                sfz_content += f"<control>\n"
                #sfz_content += f"label_cc118=PleaseSetMe127\n" # lfo FX tune
                #sfz_content += f"set_cc118=127\n"
                sfz_content += f"label_cc117=PleaseSetMe127\n" # lfo FX phase
                sfz_content += f"set_cc117=127\n"
                sfz_content += f"label_cc89=PleaseSetMe127\n" # FX delay
                sfz_content += f"set_cc89=127\n"
                sfz_content += f"label_cc90=PleaseSetMe127\n" # lfo FX tune
                sfz_content += f"set_cc90=127\n"

                # OSC 1
                sfz_content += f"<group>\n"
                if m.fx_delay > 0:
                  sfz_content += f"delay_oncc{cc_sw(89, m.fx_delay)}={m.fx_delay}\n"
                sfz_content += f"tune_oncc{cc_sw(90,m.fx_detune)}={-abs(int(m.fx_detune))} lfo{lfo_idx+4}_pitch={m.fx_depth} lfo{lfo_idx+4}_freq={m.fx_speed} lfo{lfo_idx+4}_wave={m.fx_wave} lfo{lfo_idx+4}_phase_oncc{cc_sw(117,m.fx_pan)}={int(m.fx_pan) / 100}\n"

                if m.wave == "TableWarp2":
                  sfz_content += f"<region> sample={m.get_wave()}\n"
                  sfz_content += f"sample_dyn_param03={(tablewarp_switch[tablewarp_wave.index(m.tw_waveform)] * 15.875) / 100}\n"
                  sfz_content += f"sample_dyn_param01={m.tw_waveform_offset}\n"

                  if m.tw_waveform_eg:
                    #print(eg_idx)
                    sfz_content += f"eg{eg_idx+4}_sample_dyn_param01={m.tw_waveform_eg_depth}\n"
                    sfz_content += generate_eg_tw(eg_idx+4, m.tw_waveform_eg_start, m.tw_waveform_eg_delay, m.tw_waveform_eg_attack, m.tw_waveform_eg_attack_shape, m.tw_waveform_eg_hold, m.tw_waveform_eg_decay, m.tw_waveform_eg_decay_shape, m.tw_waveform_eg_sustain, m.tw_waveform_eg_release, m.tw_waveform_eg_release_shape)
                  if m.tw_waveform_lfo:
                    sfz_content += "\n\n"
                    sfz_content += f"lfo{lfo_idx+5}_delay={m.tw_waveform_lfo_delay}\n"
                    sfz_content += f"lfo{lfo_idx+5}_fade={m.tw_waveform_lfo_fade}\n"
                    sfz_content += f"lfo{lfo_idx+5}_sample_dyn_param01={m.tw_waveform_lfo_depth / 100}\n"
                    sfz_content += f"lfo{lfo_idx+5}_freq={m.tw_waveform_lfo_freq}\n"
                    sfz_content += f"lfo{lfo_idx+5}_wave={m.tw_waveform_lfo_wave}\n\n"

                  sfz_content += f"sample_dyn_param04={(tablewarp_switch[tablewarp_warp.index(m.tw_warp)] * 15.875) / 100}\n"
                  sfz_content += f"sample_dyn_param02={m.tw_warp_offset}\n"

                  if m.tw_warp_eg:
                    sfz_content += f"eg{eg_idx+5}_sample_dyn_param02={m.tw_warp_eg_depth}\n"
                    sfz_content += generate_eg_tw(eg_idx+5, m.tw_warp_eg_start, m.tw_warp_eg_delay, m.tw_warp_eg_attack, m.tw_warp_eg_attack_shape, m.tw_warp_eg_hold, m.tw_warp_eg_decay, m.tw_warp_eg_decay_shape, m.tw_warp_eg_sustain, m.tw_warp_eg_release, m.tw_warp_eg_release_shape)
                  if m.tw_warp_lfo:
                    sfz_content += "\n\n"
                    sfz_content += f"lfo{lfo_idx+6}_delay={m.tw_warp_lfo_delay}\n"
                    sfz_content += f"lfo{lfo_idx+6}_fade={m.tw_warp_lfo_fade}\n"
                    sfz_content += f"lfo{lfo_idx+6}_sample_dyn_param02={m.tw_warp_lfo_depth / 100}\n"
                    sfz_content += f"lfo{lfo_idx+6}_freq={m.tw_warp_lfo_freq}\n"
                    sfz_content += f"lfo{lfo_idx+6}_wave={m.tw_warp_lfo_wave}\n"
                  sfz_content += "\n"
                else:
                  if m.wave == "Sample":
                    sfz_content += f"<region> sample=$USERPATH/Wavetables/{m.pack}/{m.get_wave()}\n"
                    sfz_content += f"oscillator=on\n"
                  else:
                    sfz_content += f"<region> sample={m.get_wave()}\n"

                  sfz_content += f"oscillator_mode={wave_modes.index(m.wave_mode)} oscillator_quality={m.wave_quality} oscillator_multi={m.wave_unison} oscillator_phase={m.wave_phase / 100}\n"
                  sfz_content += f"oscillator_detune={m.wave_detune}\n"
                  if m.wave_detune_ccbool:
                    sfz_content += f"oscillator_detune_oncc{m.wave_detune_cc[0]}={m.wave_detune_cc[1]}\n"
                  if m.wave_mod_depth_ccbool:
                    sfz_content += f"oscillator_mod_depth_oncc{m.wave_mod_depth_cc[0]}={m.wave_mod_depth_cc[1]}\n"
                  sfz_content += f"oscillator_mod_depth={m.wave_mod_depth}\n\n"

                # OSC 2
                sfz_content += f"<group>\n"
                if m.wave == "TableWarp2":
                  sfz_content += f"<region> sample={m.get_wave()}\n"
                  sfz_content += f"sample_dyn_param03={(tablewarp_switch[tablewarp_wave.index(m.tw_waveform)] * 15.875) / 100}\n"
                  sfz_content += f"sample_dyn_param01={m.tw_waveform_offset}\n"

                  if m.tw_waveform_eg:
                    #print(eg_idx)
                    sfz_content += f"eg{eg_idx+4}_sample_dyn_param01={m.tw_waveform_eg_depth}\n"
                    sfz_content += generate_eg_tw(eg_idx+4, m.tw_waveform_eg_start, m.tw_waveform_eg_delay, m.tw_waveform_eg_attack, m.tw_waveform_eg_attack_shape, m.tw_waveform_eg_hold, m.tw_waveform_eg_decay, m.tw_waveform_eg_decay_shape, m.tw_waveform_eg_sustain, m.tw_waveform_eg_release, m.tw_waveform_eg_release_shape)
                  if m.tw_waveform_lfo:
                    sfz_content += "\n\n"
                    sfz_content += f"lfo{lfo_idx+5}_delay={m.tw_waveform_lfo_delay}\n"
                    sfz_content += f"lfo{lfo_idx+5}_fade={m.tw_waveform_lfo_fade}\n"
                    sfz_content += f"lfo{lfo_idx+5}_sample_dyn_param01={m.tw_waveform_lfo_depth / 100}\n"
                    sfz_content += f"lfo{lfo_idx+5}_freq={m.tw_waveform_lfo_freq}\n"
                    sfz_content += f"lfo{lfo_idx+5}_wave={m.tw_waveform_lfo_wave}\n\n"

                  sfz_content += f"sample_dyn_param04={(tablewarp_switch[tablewarp_warp.index(m.tw_warp)] * 15.875) / 100}\n"
                  sfz_content += f"sample_dyn_param02={m.tw_warp_offset}\n"

                  if m.tw_warp_eg:
                    sfz_content += f"eg{eg_idx+5}_sample_dyn_param02={m.tw_warp_eg_depth}\n"
                    sfz_content += generate_eg_tw(eg_idx+5, m.tw_warp_eg_start, m.tw_warp_eg_delay, m.tw_warp_eg_attack, m.tw_warp_eg_attack_shape, m.tw_warp_eg_hold, m.tw_warp_eg_decay, m.tw_warp_eg_decay_shape, m.tw_warp_eg_sustain, m.tw_warp_eg_release, m.tw_warp_eg_release_shape)
                  if m.tw_warp_lfo:
                    sfz_content += "\n\n"
                    sfz_content += f"lfo{lfo_idx+6}_delay={m.tw_warp_lfo_delay}\n"
                    sfz_content += f"lfo{lfo_idx+6}_fade={m.tw_warp_lfo_fade}\n"
                    sfz_content += f"lfo{lfo_idx+6}_sample_dyn_param02={m.tw_warp_lfo_depth / 100}\n"
                    sfz_content += f"lfo{lfo_idx+6}_freq={m.tw_warp_lfo_freq}\n"
                    sfz_content += f"lfo{lfo_idx+6}_wave={m.tw_warp_lfo_wave}\n"
                  sfz_content += "\n"
                else:
                  if m.wave == "Sample":
                    sfz_content += f"<region> sample=$USERPATH/Wavetables/{m.pack}/{m.get_wave()}\n"
                    sfz_content += f"oscillator=on\n"
                  else:
                    sfz_content += f"<region> sample={m.get_wave()}\n"

                  sfz_content += f"oscillator_mode={wave_modes.index(m.wave_mode)} oscillator_quality={m.wave_quality} oscillator_multi={m.wave_unison} oscillator_phase={m.wave_phase / 100}\n"
                  sfz_content += f"oscillator_detune={m.wave_detune}\n"
                  if m.wave_detune_ccbool:
                    sfz_content += f"oscillator_detune_oncc{m.wave_detune_cc[0]}={m.wave_detune_cc[1]}\n"
                  if m.wave_mod_depth_ccbool:
                    sfz_content += f"oscillator_mod_depth_oncc{m.wave_mod_depth_cc[0]}={m.wave_mod_depth_cc[1]}\n"
                  sfz_content += f"oscillator_mod_depth={m.wave_mod_depth}\n\n"
              case 3: # STEREO CHORUS (WET)
                sfz_content += f"<control>\n"
                sfz_content += f"label_cc117=PleaseSetMe127\n"
                sfz_content += f"set_cc117=127\n"
                sfz_content += f"label_cc89=PleaseSetMe127\n" # FX delay
                sfz_content += f"set_cc89=127\n"
                sfz_content += f"label_cc90=PleaseSetMe127\n"
                sfz_content += f"set_cc90=127\n"

                # OSC 1
                sfz_content += f"<group>\n"
                if m.fx_delay > 0:
                  sfz_content += f"delay_oncc{cc_sw(89, m.fx_delay)}={m.fx_delay}\n"
                sfz_content += f"tune_oncc90={int(m.fx_depth) * 2} lfo{lfo_idx+4}_pitch={-abs(m.fx_depth)} lfo{lfo_idx+4}_freq={m.fx_speed} lfo{lfo_idx+4}_wave={m.fx_wave} lfo{lfo_idx+4}_phase_oncc{cc_sw(117,m.fx_pan)}={int(m.fx_pan) / 100} pan=-100\n"
                if m.wave == "TableWarp2":
                  sfz_content += f"<region> sample={m.get_wave()}\n"
                  sfz_content += f"sample_dyn_param03={(tablewarp_switch[tablewarp_wave.index(m.tw_waveform)] * 15.875) / 100}\n"
                  sfz_content += f"sample_dyn_param01={m.tw_waveform_offset}\n"

                  if m.tw_waveform_eg:
                    #print(eg_idx)
                    sfz_content += f"eg{eg_idx+4}_sample_dyn_param01={m.tw_waveform_eg_depth}\n"
                    sfz_content += generate_eg_tw(eg_idx+4, m.tw_waveform_eg_start, m.tw_waveform_eg_delay, m.tw_waveform_eg_attack, m.tw_waveform_eg_attack_shape, m.tw_waveform_eg_hold, m.tw_waveform_eg_decay, m.tw_waveform_eg_decay_shape, m.tw_waveform_eg_sustain, m.tw_waveform_eg_release, m.tw_waveform_eg_release_shape)
                  if m.tw_waveform_lfo:
                    sfz_content += "\n\n"
                    sfz_content += f"lfo{lfo_idx+5}_delay={m.tw_waveform_lfo_delay}\n"
                    sfz_content += f"lfo{lfo_idx+5}_fade={m.tw_waveform_lfo_fade}\n"
                    sfz_content += f"lfo{lfo_idx+5}_sample_dyn_param01={m.tw_waveform_lfo_depth / 100}\n"
                    sfz_content += f"lfo{lfo_idx+5}_freq={m.tw_waveform_lfo_freq}\n"
                    sfz_content += f"lfo{lfo_idx+5}_wave={m.tw_waveform_lfo_wave}\n\n"

                  sfz_content += f"sample_dyn_param04={(tablewarp_switch[tablewarp_warp.index(m.tw_warp)] * 15.875) / 100}\n"
                  sfz_content += f"sample_dyn_param02={m.tw_warp_offset}\n"

                  if m.tw_warp_eg:
                    sfz_content += f"eg{eg_idx+5}_sample_dyn_param02={m.tw_warp_eg_depth}\n"
                    sfz_content += generate_eg_tw(eg_idx+5, m.tw_warp_eg_start, m.tw_warp_eg_delay, m.tw_warp_eg_attack, m.tw_warp_eg_attack_shape, m.tw_warp_eg_hold, m.tw_warp_eg_decay, m.tw_warp_eg_decay_shape, m.tw_warp_eg_sustain, m.tw_warp_eg_release, m.tw_warp_eg_release_shape)
                  if m.tw_warp_lfo:
                    sfz_content += "\n\n"
                    sfz_content += f"lfo{lfo_idx+6}_delay={m.tw_warp_lfo_delay}\n"
                    sfz_content += f"lfo{lfo_idx+6}_fade={m.tw_warp_lfo_fade}\n"
                    sfz_content += f"lfo{lfo_idx+6}_sample_dyn_param02={m.tw_warp_lfo_depth / 100}\n"
                    sfz_content += f"lfo{lfo_idx+6}_freq={m.tw_warp_lfo_freq}\n"
                    sfz_content += f"lfo{lfo_idx+6}_wave={m.tw_warp_lfo_wave}\n"
                  sfz_content += "\n"
                else:
                  if m.wave == "Sample":
                    sfz_content += f"<region> sample=$USERPATH/Wavetables/{m.pack}/{m.get_wave()}\n"
                    sfz_content += f"oscillator=on\n"
                  else:
                    sfz_content += f"<region> sample={m.get_wave()}\n"

                  sfz_content += f"oscillator_mode={wave_modes.index(m.wave_mode)} oscillator_quality={m.wave_quality} oscillator_multi={m.wave_unison} oscillator_phase={m.wave_phase / 100}\n"
                  sfz_content += f"oscillator_detune={m.wave_detune}\n"
                  if m.wave_detune_ccbool:
                    sfz_content += f"oscillator_detune_oncc{m.wave_detune_cc[0]}={m.wave_detune_cc[1]}\n"
                  if m.wave_mod_depth_ccbool:
                    sfz_content += f"oscillator_mod_depth_oncc{m.wave_mod_depth_cc[0]}={m.wave_mod_depth_cc[1]}\n"
                  sfz_content += f"oscillator_mod_depth={m.wave_mod_depth}\n\n"

                # OSC 2
                sfz_content += f"<group>\n"

                if m.fx_delay > 0:
                  sfz_content += f"delay_oncc{cc_sw(89, m.fx_delay)}={m.fx_delay}\n"
                sfz_content += f"tune_oncc90={-abs(int(m.fx_depth) * 2)} lfo{lfo_idx+4}_pitch={m.fx_depth} lfo{lfo_idx+4}_freq={m.fx_speed} lfo{lfo_idx+4}_wave={m.fx_wave} lfo{lfo_idx+4}_phase_oncc{cc_sw(117,m.fx_pan)}={int(m.fx_pan) / 100} pan=100\n"

                if m.wave == "TableWarp2":
                  sfz_content += f"<region> sample={m.get_wave()}\n"
                  sfz_content += f"sample_dyn_param03={(tablewarp_switch[tablewarp_wave.index(m.tw_waveform)] * 15.875) / 100}\n"
                  sfz_content += f"sample_dyn_param01={m.tw_waveform_offset}\n"

                  if m.tw_waveform_eg:
                    #print(eg_idx)
                    sfz_content += f"eg{eg_idx+4}_sample_dyn_param01={m.tw_waveform_eg_depth}\n"
                    sfz_content += generate_eg_tw(eg_idx+4, m.tw_waveform_eg_start, m.tw_waveform_eg_delay, m.tw_waveform_eg_attack, m.tw_waveform_eg_attack_shape, m.tw_waveform_eg_hold, m.tw_waveform_eg_decay, m.tw_waveform_eg_decay_shape, m.tw_waveform_eg_sustain, m.tw_waveform_eg_release, m.tw_waveform_eg_release_shape)
                  if m.tw_waveform_lfo:
                    sfz_content += "\n\n"
                    sfz_content += f"lfo{lfo_idx+5}_delay={m.tw_waveform_lfo_delay}\n"
                    sfz_content += f"lfo{lfo_idx+5}_fade={m.tw_waveform_lfo_fade}\n"
                    sfz_content += f"lfo{lfo_idx+5}_sample_dyn_param01={m.tw_waveform_lfo_depth / 100}\n"
                    sfz_content += f"lfo{lfo_idx+5}_freq={m.tw_waveform_lfo_freq}\n"
                    sfz_content += f"lfo{lfo_idx+5}_wave={m.tw_waveform_lfo_wave}\n\n"

                  sfz_content += f"sample_dyn_param04={(tablewarp_switch[tablewarp_warp.index(m.tw_warp)] * 15.875) / 100}\n"
                  sfz_content += f"sample_dyn_param02={m.tw_warp_offset}\n"

                  if m.tw_warp_eg:
                    sfz_content += f"eg{eg_idx+5}_sample_dyn_param02={m.tw_warp_eg_depth}\n"
                    sfz_content += generate_eg_tw(eg_idx+5, m.tw_warp_eg_start, m.tw_warp_eg_delay, m.tw_warp_eg_attack, m.tw_warp_eg_attack_shape, m.tw_warp_eg_hold, m.tw_warp_eg_decay, m.tw_warp_eg_decay_shape, m.tw_warp_eg_sustain, m.tw_warp_eg_release, m.tw_warp_eg_release_shape)
                  if m.tw_warp_lfo:
                    sfz_content += "\n\n"
                    sfz_content += f"lfo{lfo_idx+6}_delay={m.tw_warp_lfo_delay}\n"
                    sfz_content += f"lfo{lfo_idx+6}_fade={m.tw_warp_lfo_fade}\n"
                    sfz_content += f"lfo{lfo_idx+6}_sample_dyn_param02={m.tw_warp_lfo_depth / 100}\n"
                    sfz_content += f"lfo{lfo_idx+6}_freq={m.tw_warp_lfo_freq}\n"
                    sfz_content += f"lfo{lfo_idx+6}_wave={m.tw_warp_lfo_wave}\n"
                  sfz_content += "\n"
                else:
                  if m.wave == "Sample":
                    sfz_content += f"<region> sample=$USERPATH/Wavetables/{m.pack}/{m.get_wave()}\n"
                    sfz_content += f"oscillator=on\n"
                  else:
                    sfz_content += f"<region> sample={m.get_wave()}\n"

                  sfz_content += f"oscillator_mode={wave_modes.index(m.wave_mode)} oscillator_quality={m.wave_quality} oscillator_multi={m.wave_unison} oscillator_phase={m.wave_phase / 100}\n"
                  sfz_content += f"oscillator_detune={m.wave_detune}\n"
                  if m.wave_detune_ccbool:
                    sfz_content += f"oscillator_detune_oncc{m.wave_detune_cc[0]}={m.wave_detune_cc[1]}\n"
                  if m.wave_mod_depth_ccbool:
                    sfz_content += f"oscillator_mod_depth_oncc{m.wave_mod_depth_cc[0]}={m.wave_mod_depth_cc[1]}\n"
                  sfz_content += f"oscillator_mod_depth={m.wave_mod_depth}\n\n"
              case 4: # STEREO CHORUS (WET+DRY)
                sfz_content += f"<control>\n"
                sfz_content += f"label_cc117=PleaseSetMe127\n"
                sfz_content += f"set_cc117=127\n"
                sfz_content += f"label_cc89=PleaseSetMe127\n" # FX delay
                sfz_content += f"set_cc89=127\n"
                sfz_content += f"label_cc90=PleaseSetMe127\n"
                sfz_content += f"set_cc90=127\n"

                # OSC 1
                sfz_content += f"<group>\n"
                if m.fx_delay > 0:
                  sfz_content += f"delay_oncc{cc_sw(89, m.fx_delay)}={m.fx_delay}\n"
                sfz_content += f"tune_oncc90={int(m.fx_depth) * 2} lfo{lfo_idx+4}_pitch={-abs(m.fx_depth)} lfo{lfo_idx+4}_freq={m.fx_speed} lfo{lfo_idx+4}_wave={m.fx_wave} lfo{lfo_idx+4}_phase_oncc{cc_sw(117,m.fx_pan)}={int(m.fx_pan) / 100} pan=-100\n"

                if m.wave == "TableWarp2":
                  sfz_content += f"<region> sample={m.get_wave()}\n"
                  sfz_content += f"sample_dyn_param03={(tablewarp_switch[tablewarp_wave.index(m.tw_waveform)] * 15.875) / 100}\n"
                  sfz_content += f"sample_dyn_param01={m.tw_waveform_offset}\n"

                  if m.tw_waveform_eg:
                    #print(eg_idx)
                    sfz_content += f"eg{eg_idx+4}_sample_dyn_param01={m.tw_waveform_eg_depth}\n"
                    sfz_content += generate_eg_tw(eg_idx+4, m.tw_waveform_eg_start, m.tw_waveform_eg_delay, m.tw_waveform_eg_attack, m.tw_waveform_eg_attack_shape, m.tw_waveform_eg_hold, m.tw_waveform_eg_decay, m.tw_waveform_eg_decay_shape, m.tw_waveform_eg_sustain, m.tw_waveform_eg_release, m.tw_waveform_eg_release_shape)
                  if m.tw_waveform_lfo:
                    sfz_content += "\n\n"
                    sfz_content += f"lfo{lfo_idx+5}_delay={m.tw_waveform_lfo_delay}\n"
                    sfz_content += f"lfo{lfo_idx+5}_fade={m.tw_waveform_lfo_fade}\n"
                    sfz_content += f"lfo{lfo_idx+5}_sample_dyn_param01={m.tw_waveform_lfo_depth / 100}\n"
                    sfz_content += f"lfo{lfo_idx+5}_freq={m.tw_waveform_lfo_freq}\n"
                    sfz_content += f"lfo{lfo_idx+5}_wave={m.tw_waveform_lfo_wave}\n\n"

                  sfz_content += f"sample_dyn_param04={(tablewarp_switch[tablewarp_warp.index(m.tw_warp)] * 15.875) / 100}\n"
                  sfz_content += f"sample_dyn_param02={m.tw_warp_offset}\n"

                  if m.tw_warp_eg:
                    sfz_content += f"eg{eg_idx+5}_sample_dyn_param02={m.tw_warp_eg_depth}\n"
                    sfz_content += generate_eg_tw(eg_idx+5, m.tw_warp_eg_start, m.tw_warp_eg_delay, m.tw_warp_eg_attack, m.tw_warp_eg_attack_shape, m.tw_warp_eg_hold, m.tw_warp_eg_decay, m.tw_warp_eg_decay_shape, m.tw_warp_eg_sustain, m.tw_warp_eg_release, m.tw_warp_eg_release_shape)
                  if m.tw_warp_lfo:
                    sfz_content += "\n\n"
                    sfz_content += f"lfo{lfo_idx+6}_delay={m.tw_warp_lfo_delay}\n"
                    sfz_content += f"lfo{lfo_idx+6}_fade={m.tw_warp_lfo_fade}\n"
                    sfz_content += f"lfo{lfo_idx+6}_sample_dyn_param02={m.tw_warp_lfo_depth / 100}\n"
                    sfz_content += f"lfo{lfo_idx+6}_freq={m.tw_warp_lfo_freq}\n"
                    sfz_content += f"lfo{lfo_idx+6}_wave={m.tw_warp_lfo_wave}\n"
                  sfz_content += "\n"
                else:
                  if m.wave == "Sample":
                    sfz_content += f"<region> sample=$USERPATH/Wavetables/{m.pack}/{m.get_wave()}\n"
                    sfz_content += f"oscillator=on\n"
                  else:
                    sfz_content += f"<region> sample={m.get_wave()}\n"

                  sfz_content += f"oscillator_mode={wave_modes.index(m.wave_mode)} oscillator_quality={m.wave_quality} oscillator_multi={m.wave_unison} oscillator_phase={m.wave_phase / 100}\n"
                  sfz_content += f"oscillator_detune={m.wave_detune}\n"
                  if m.wave_detune_ccbool:
                    sfz_content += f"oscillator_detune_oncc{m.wave_detune_cc[0]}={m.wave_detune_cc[1]}\n"
                  if m.wave_mod_depth_ccbool:
                    sfz_content += f"oscillator_mod_depth_oncc{m.wave_mod_depth_cc[0]}={m.wave_mod_depth_cc[1]}\n"
                  sfz_content += f"oscillator_mod_depth={m.wave_mod_depth}\n\n"

                # OSC 2
                sfz_content += f"<group>\n"

                if m.fx_delay > 0:
                  sfz_content += f"delay_oncc{cc_sw(89, m.fx_delay)}={m.fx_delay}\n"
                sfz_content += f"tune_oncc90={-abs(int(m.fx_depth) * 2)} lfo{lfo_idx+4}_pitch={m.fx_depth} lfo{lfo_idx+4}_freq={m.fx_speed} lfo{lfo_idx+4}_wave={m.fx_wave} lfo{lfo_idx+4}_phase_oncc{cc_sw(117,m.fx_pan)}={int(m.fx_pan) / 100} pan=100\n"

                if m.wave == "TableWarp2":
                  sfz_content += f"<region> sample={m.get_wave()}\n"
                  sfz_content += f"sample_dyn_param03={(tablewarp_switch[tablewarp_wave.index(m.tw_waveform)] * 15.875) / 100}\n"
                  sfz_content += f"sample_dyn_param01={m.tw_waveform_offset}\n"

                  if m.tw_waveform_eg:
                    #print(eg_idx)
                    sfz_content += f"eg{eg_idx+4}_sample_dyn_param01={m.tw_waveform_eg_depth}\n"
                    sfz_content += generate_eg_tw(eg_idx+4, m.tw_waveform_eg_start, m.tw_waveform_eg_delay, m.tw_waveform_eg_attack, m.tw_waveform_eg_attack_shape, m.tw_waveform_eg_hold, m.tw_waveform_eg_decay, m.tw_waveform_eg_decay_shape, m.tw_waveform_eg_sustain, m.tw_waveform_eg_release, m.tw_waveform_eg_release_shape)
                  if m.tw_waveform_lfo:
                    sfz_content += "\n\n"
                    sfz_content += f"lfo{lfo_idx+5}_delay={m.tw_waveform_lfo_delay}\n"
                    sfz_content += f"lfo{lfo_idx+5}_fade={m.tw_waveform_lfo_fade}\n"
                    sfz_content += f"lfo{lfo_idx+5}_sample_dyn_param01={m.tw_waveform_lfo_depth / 100}\n"
                    sfz_content += f"lfo{lfo_idx+5}_freq={m.tw_waveform_lfo_freq}\n"
                    sfz_content += f"lfo{lfo_idx+5}_wave={m.tw_waveform_lfo_wave}\n\n"

                  sfz_content += f"sample_dyn_param04={(tablewarp_switch[tablewarp_warp.index(m.tw_warp)] * 15.875) / 100}\n"
                  sfz_content += f"sample_dyn_param02={m.tw_warp_offset}\n"

                  if m.tw_warp_eg:
                    sfz_content += f"eg{eg_idx+5}_sample_dyn_param02={m.tw_warp_eg_depth}\n"
                    sfz_content += generate_eg_tw(eg_idx+5, m.tw_warp_eg_start, m.tw_warp_eg_delay, m.tw_warp_eg_attack, m.tw_warp_eg_attack_shape, m.tw_warp_eg_hold, m.tw_warp_eg_decay, m.tw_warp_eg_decay_shape, m.tw_warp_eg_sustain, m.tw_warp_eg_release, m.tw_warp_eg_release_shape)
                  if m.tw_warp_lfo:
                    sfz_content += "\n\n"
                    sfz_content += f"lfo{lfo_idx+6}_delay={m.tw_warp_lfo_delay}\n"
                    sfz_content += f"lfo{lfo_idx+6}_fade={m.tw_warp_lfo_fade}\n"
                    sfz_content += f"lfo{lfo_idx+6}_sample_dyn_param02={m.tw_warp_lfo_depth / 100}\n"
                    sfz_content += f"lfo{lfo_idx+6}_freq={m.tw_warp_lfo_freq}\n"
                    sfz_content += f"lfo{lfo_idx+6}_wave={m.tw_warp_lfo_wave}\n"
                  sfz_content += "\n"
                else:
                  if m.wave == "Sample":
                    sfz_content += f"<region> sample=$USERPATH/Wavetables/{m.pack}/{m.get_wave()}\n"
                    sfz_content += f"oscillator=on\n"
                  else:
                    sfz_content += f"<region> sample={m.get_wave()}\n"

                  sfz_content += f"oscillator_mode={wave_modes.index(m.wave_mode)} oscillator_quality={m.wave_quality} oscillator_multi={m.wave_unison} oscillator_phase={m.wave_phase / 100}\n"
                  sfz_content += f"oscillator_detune={m.wave_detune}\n"
                  if m.wave_detune_ccbool:
                    sfz_content += f"oscillator_detune_oncc{m.wave_detune_cc[0]}={m.wave_detune_cc[1]}\n"
                  if m.wave_mod_depth_ccbool:
                    sfz_content += f"oscillator_mod_depth_oncc{m.wave_mod_depth_cc[0]}={m.wave_mod_depth_cc[1]}\n"
                  sfz_content += f"oscillator_mod_depth={m.wave_mod_depth}\n\n"

                # OSC 3 (DRY)
                sfz_content += f"<group>\n"
                if m.wave == "TableWarp2":
                  sfz_content += f"<region> sample={m.get_wave()}\n"
                  sfz_content += f"sample_dyn_param03={(tablewarp_switch[tablewarp_wave.index(m.tw_waveform)] * 15.875) / 100}\n"
                  sfz_content += f"sample_dyn_param01={m.tw_waveform_offset}\n"

                  if m.tw_waveform_eg:
                    #print(eg_idx)
                    sfz_content += f"eg{eg_idx+4}_sample_dyn_param01={m.tw_waveform_eg_depth}\n"
                    sfz_content += generate_eg_tw(eg_idx+4, m.tw_waveform_eg_start, m.tw_waveform_eg_delay, m.tw_waveform_eg_attack, m.tw_waveform_eg_attack_shape, m.tw_waveform_eg_hold, m.tw_waveform_eg_decay, m.tw_waveform_eg_decay_shape, m.tw_waveform_eg_sustain, m.tw_waveform_eg_release, m.tw_waveform_eg_release_shape)
                  if m.tw_waveform_lfo:
                    sfz_content += "\n\n"
                    sfz_content += f"lfo{lfo_idx+5}_delay={m.tw_waveform_lfo_delay}\n"
                    sfz_content += f"lfo{lfo_idx+5}_fade={m.tw_waveform_lfo_fade}\n"
                    sfz_content += f"lfo{lfo_idx+5}_sample_dyn_param01={m.tw_waveform_lfo_depth / 100}\n"
                    sfz_content += f"lfo{lfo_idx+5}_freq={m.tw_waveform_lfo_freq}\n"
                    sfz_content += f"lfo{lfo_idx+5}_wave={m.tw_waveform_lfo_wave}\n\n"

                  sfz_content += f"sample_dyn_param04={(tablewarp_switch[tablewarp_warp.index(m.tw_warp)] * 15.875) / 100}\n"
                  sfz_content += f"sample_dyn_param02={m.tw_warp_offset}\n"

                  if m.tw_warp_eg:
                    sfz_content += f"eg{eg_idx+5}_sample_dyn_param02={m.tw_warp_eg_depth}\n"
                    sfz_content += generate_eg_tw(eg_idx+5, m.tw_warp_eg_start, m.tw_warp_eg_delay, m.tw_warp_eg_attack, m.tw_warp_eg_attack_shape, m.tw_warp_eg_hold, m.tw_warp_eg_decay, m.tw_warp_eg_decay_shape, m.tw_warp_eg_sustain, m.tw_warp_eg_release, m.tw_warp_eg_release_shape)
                  if m.tw_warp_lfo:
                    sfz_content += "\n\n"
                    sfz_content += f"lfo{lfo_idx+6}_delay={m.tw_warp_lfo_delay}\n"
                    sfz_content += f"lfo{lfo_idx+6}_fade={m.tw_warp_lfo_fade}\n"
                    sfz_content += f"lfo{lfo_idx+6}_sample_dyn_param02={m.tw_warp_lfo_depth / 100}\n"
                    sfz_content += f"lfo{lfo_idx+6}_freq={m.tw_warp_lfo_freq}\n"
                    sfz_content += f"lfo{lfo_idx+6}_wave={m.tw_warp_lfo_wave}\n"
                  sfz_content += "\n"
                else:
                  if m.wave == "Sample":
                    sfz_content += f"<region> sample=$USERPATH/Wavetables/{m.pack}/{m.get_wave()}\n"
                    sfz_content += f"oscillator=on\n"
                  else:
                    sfz_content += f"<region> sample={m.get_wave()}\n"

                  sfz_content += f"oscillator_mode={wave_modes.index(m.wave_mode)} oscillator_quality={m.wave_quality} oscillator_multi={m.wave_unison} oscillator_phase={m.wave_phase / 100}\n"
                  sfz_content += f"oscillator_detune={m.wave_detune}\n"
                  if m.wave_detune_ccbool:
                    sfz_content += f"oscillator_detune_oncc{m.wave_detune_cc[0]}={m.wave_detune_cc[1]}\n"
                  if m.wave_mod_depth_ccbool:
                    sfz_content += f"oscillator_mod_depth_oncc{m.wave_mod_depth_cc[0]}={m.wave_mod_depth_cc[1]}\n"
                  sfz_content += f"oscillator_mod_depth={m.wave_mod_depth}\n\n"

          else: # sample mapping
            match m.fx_mode:
              case 0: # NO FX
                sfz_content += f"<group>\n"
                sfz_content += f"<control>\n"
                sfz_content += f"note_offset={m.note_offset}\n"
                sfz_content += f"default_path=$USERPATH/MappingPool/{m.get_default_path()}/\n#include \"$USERPATH/MappingPool/{m.get_include_path()}\"\n\n"
              case 1: # UNISON
                sfz_content += f"<control>\n"
                sfz_content += f"label_cc89=PleaseSetMe127\n"
                sfz_content += f"label_cc90=PleaseSetMe127\n"
                sfz_content += f"set_cc89=127\n"
                sfz_content += f"set_cc90=127\n"

                # OSC 1
                sfz_content += f"<group>\n"
                sfz_content += f"pitch_oncc90={int(m.fx_detune)}\n"
                if m.fx_pan >= 0:
                  sfz_content += f"pan={int(m.fx_pan)}\n"
                sfz_content += f"<control>\n"
                sfz_content += f"note_offset={m.note_offset}\n"
                sfz_content += f"default_path=$USERPATH/MappingPool/{m.get_default_path()}/\n#include \"$USERPATH/MappingPool/{m.get_include_path()}\"\n\n"

                # OSC 2
                sfz_content += f"<group>\n"
                sfz_content += f"pitch_oncc90={-abs(int(m.fx_detune))}\n"
                if m.fx_pan >= 0:
                  sfz_content += f"pan={-abs(int(m.fx_pan))}\n"
                if m.fx_delay >= 0:
                  sfz_content += f"delay_oncc{cc_sw(89, m.fx_delay)}={m.fx_delay}\n"
                sfz_content += f"<control>\n"
                sfz_content += f"note_offset={m.note_offset}\n"
                sfz_content += f"default_path=$USERPATH/MappingPool/{m.get_default_path()}/\n#include \"$USERPATH/MappingPool/{m.get_include_path()}\"\n\n"
              case 2: # MONO CHORUS
                sfz_content += f"<control>\n"
                sfz_content += f"label_cc118=PleaseSetMe127\n"
                sfz_content += f"set_cc118=127\n"
                sfz_content += f"label_cc117=PleaseSetMe127\n"
                sfz_content += f"set_cc117=127\n"
                sfz_content += f"label_cc89=PleaseSetMe127\n" # FX delay
                sfz_content += f"set_cc89=127\n"
                sfz_content += f"label_cc90=PleaseSetMe127\n"
                sfz_content += f"set_cc90=127\n"

                # OSC 1
                sfz_content += f"<group>\n"
                if m.fx_delay >= 0:
                  sfz_content += f"delay_oncc{cc_sw(89, m.fx_delay)}={m.fx_delay}\n"
                sfz_content += f"tune_oncc{cc_sw(90,m.fx_detune)}={-abs(int(m.fx_detune))} lfo{lfo_idx+4}_pitch={m.fx_depth} lfo{lfo_idx+4}_freq={m.fx_speed} lfo{lfo_idx+4}_wave={m.fx_wave} lfo{lfo_idx+4}_phase_oncc{cc_sw(117,m.fx_pan)}={int(m.fx_pan) / 100}\n"

                sfz_content += f"<control>\n"
                sfz_content += f"note_offset={m.note_offset}\n"
                sfz_content += f"default_path=$USERPATH/MappingPool/{m.get_default_path()}/\n#include \"$USERPATH/MappingPool/{m.get_include_path()}\"\n\n"

                # OSC 2
                sfz_content += f"<group>\n"
                sfz_content += f"<control>\n"
                sfz_content += f"note_offset={m.note_offset}\n"
                sfz_content += f"default_path=$USERPATH/MappingPool/{m.get_default_path()}/\n#include \"$USERPATH/MappingPool/{m.get_include_path()}\"\n\n"
              case 3: # STEREO CHORUS (WET)
                sfz_content += f"<control>\n"
                sfz_content += f"label_cc118=PleaseSetMe127\n"
                sfz_content += f"set_cc118=127\n"
                sfz_content += f"label_cc117=PleaseSetMe127\n"
                sfz_content += f"set_cc117=127\n"
                sfz_content += f"label_cc89=PleaseSetMe127\n" # FX delay
                sfz_content += f"set_cc89=127\n"
                sfz_content += f"label_cc90=PleaseSetMe127\n"
                sfz_content += f"set_cc90=127\n"

                # OSC 1
                sfz_content += f"<group>\n"
                if m.fx_delay > 0:
                  sfz_content += f"delay_oncc{cc_sw(89, m.fx_delay)}={m.fx_delay}\n"
                sfz_content += f"tune_oncc90={int(m.fx_depth) * 2} lfo{lfo_idx+4}_pitch={-abs(m.fx_depth)} lfo{lfo_idx+4}_freq={m.fx_speed} lfo{lfo_idx+4}_wave={m.fx_wave} lfo{lfo_idx+4}_phase_oncc{cc_sw(117,m.fx_pan)}={int(m.fx_pan) / 100} pan=-100\n"

                sfz_content += f"<control>\n"
                sfz_content += f"note_offset={m.note_offset}\n"
                sfz_content += f"default_path=$USERPATH/MappingPool/{m.get_default_path()}/\n#include \"$USERPATH/MappingPool/{m.get_include_path()}\"\n\n"

                # OSC 2
                sfz_content += f"<group>\n"

                if m.fx_delay > 0:
                  sfz_content += f"delay_oncc{cc_sw(89, m.fx_delay)}={m.fx_delay}\n"
                sfz_content += f"tune_oncc90={-abs(int(m.fx_depth) * 2)} lfo{lfo_idx+4}_pitch={m.fx_depth} lfo{lfo_idx+4}_freq={m.fx_speed} lfo{lfo_idx+4}_wave={m.fx_wave} lfo{lfo_idx+4}_phase_oncc{cc_sw(117,m.fx_pan)}={int(m.fx_pan) / 100} pan=100\n"

                sfz_content += f"<control>\n"
                sfz_content += f"note_offset={m.note_offset}\n"
                sfz_content += f"default_path=$USERPATH/MappingPool/{m.get_default_path()}/\n#include \"$USERPATH/MappingPool/{m.get_include_path()}\"\n\n"

              case 4: # STEREO CHORUS (WET+DRY)
                sfz_content += f"<control>\n"
                sfz_content += f"label_cc118=PleaseSetMe127\n"
                sfz_content += f"set_cc118=127\n"
                sfz_content += f"label_cc117=PleaseSetMe127\n"
                sfz_content += f"set_cc117=127\n"
                sfz_content += f"label_cc89=PleaseSetMe127\n" # FX delay
                sfz_content += f"set_cc89=127\n"
                sfz_content += f"label_cc90=PleaseSetMe127\n"
                sfz_content += f"set_cc90=127\n"

                # OSC 1
                sfz_content += f"<group>\n"
                if m.fx_delay > 0:
                  sfz_content += f"delay_oncc{cc_sw(89, m.fx_delay)}={m.fx_delay}\n"
                sfz_content += f"tune_oncc90={int(m.fx_depth) * 2} lfo{lfo_idx+4}_pitch={-abs(m.fx_depth)} lfo{lfo_idx+4}_freq={m.fx_speed} lfo{lfo_idx+4}_wave={m.fx_wave} lfo{lfo_idx+4}_phase_oncc{cc_sw(117,m.fx_pan)}={int(m.fx_pan) / 100} pan=-100\n"

                sfz_content += f"<control>\n"
                sfz_content += f"note_offset={m.note_offset}\n"
                sfz_content += f"default_path=$USERPATH/MappingPool/{m.get_default_path()}/\n#include \"$USERPATH/MappingPool/{m.get_include_path()}\"\n\n"

                # OSC 2
                sfz_content += f"<group>\n"

                if m.fx_delay > 0:
                  sfz_content += f"delay_oncc{cc_sw(89, m.fx_delay)}={m.fx_delay}\n"
                sfz_content += f"tune_oncc90={-abs(int(m.fx_depth) * 2)} lfo{lfo_idx+4}_pitch={m.fx_depth} lfo{lfo_idx+4}_freq={m.fx_speed} lfo{lfo_idx+4}_wave={m.fx_wave} lfo{lfo_idx+4}_phase_oncc{cc_sw(117,m.fx_pan)}={int(m.fx_pan) / 100} pan=100\n"

                sfz_content += f"<control>\n"
                sfz_content += f"note_offset={m.note_offset}\n"
                sfz_content += f"default_path=$USERPATH/MappingPool/{m.get_default_path()}/\n#include \"$USERPATH/MappingPool/{m.get_include_path()}\"\n\n"

                # OSC 3 (DRY)
                sfz_content += f"<group>\n"
                sfz_content += f"<control>\n"
                sfz_content += f"note_offset={m.note_offset}\n"
                sfz_content += f"default_path=$USERPATH/MappingPool/{m.get_default_path()}/\n#include \"$USERPATH/MappingPool/{m.get_include_path()}\"\n\n"

        lfo_idx += 7
        eg_idx += 6

      # write sfz
      f_sfz = open(os.path.normpath(pathstr + ".sfz"), "w", encoding="utf8")
      f_sfz.write(sfz_content)
      f_sfz.close()

      # write project
      if temp:
        proj = f"{config_path}/Projects"
        save_project(proj, f"!TEMP.sfzproj", self.global_header, self.map_objects)
        self.ui.lblLog.setText(f"""WRITTEN: TEMP""")
      else:
        proj_path = preset_path.replace(f"{common_path}/Presets/", "") # get only the folders of the preset
        proj = f"{common_path}/Projects/{proj_path}"
        #print(proj)
        #for i in range(len())
        save_project(proj, f"{name}.sfzproj", self.global_header, self.map_objects)
        self.ui.lblLog.setText(f"""WRITTEN: {os.path.normpath(str(pathstr) + ".sfz")}""")

  def onSaveProject(self):
    if len(self.map_objects) == 0:
      self.msgbox_ok.setText("Please add a mapping.")
      self.msgbox_ok.exec()
    else:
      projectpath = QFileDialog.getSaveFileName(parent=self, caption="Save SFZBuilder project", dir=f"{self.settings.value('mainfolderpath')}/Projects/{self.ui.txtPreset.text()}", filter="Project(*.sfzproj)")
      if projectpath[0] != "":
        #print(projectpath[0])
        save_project(os.path.dirname(projectpath[0]), os.path.basename(projectpath[0]), self.global_header, self.map_objects)
        self.ui.lblLog.setText(f"""WRITTEN: {str(os.path.basename(projectpath[0]) + ".sfz")}""")

  def onOpenProject(self):
    projectpath = QFileDialog.getOpenFileName(parent=self, caption="Open SFZBuilder project", dir=f"{self.settings.value('mainfolderpath')}/Projects", filter="Project(*.sfzproj)")
    if projectpath[0] != "":
      self.map_objects = self.open_project(projectpath[0])
      # update
      self.ui.listMap.clear(); self.ui.listMap.addItems(get_map_names(self.map_objects))
      self.ui.listMap.setCurrentRow(0)

  def open_project(self, filepath):
    with open(filepath, "r") as f:
      proj_dict = json.load(f)
    global_dict = proj_dict["global"]
    mappings_dict = proj_dict["maps"]

    for k, v in global_dict.items():
      self.global_header.change_value(k, v)

    mappings_list = []
    for i in range(len(mappings_dict)):
      sfzmap = Mapping(mappings_dict[i]["type"])
      for k, v in mappings_dict[i].items():
        if k == "map":
          sfzmap.change_value(k, v)
        else:
          try:
            sfzmap.change_value(k, v)
          except:
            pass
      mappings_list.append(sfzmap)
    return mappings_list

