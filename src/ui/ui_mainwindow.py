# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDial,
    QDoubleSpinBox, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLayout, QLineEdit,
    QListWidget, QListWidgetItem, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QSplitter, QTabWidget, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(896, 760)
        self.actNew = QAction(MainWindow)
        self.actNew.setObjectName(u"actNew")
        icon = QIcon(QIcon.fromTheme(u"document-new"))
        self.actNew.setIcon(icon)
        self.actNew.setMenuRole(QAction.NoRole)
        self.actOpen = QAction(MainWindow)
        self.actOpen.setObjectName(u"actOpen")
        icon1 = QIcon(QIcon.fromTheme(u"document-open"))
        self.actOpen.setIcon(icon1)
        self.actOpen.setMenuRole(QAction.NoRole)
        self.actSave = QAction(MainWindow)
        self.actSave.setObjectName(u"actSave")
        icon2 = QIcon(QIcon.fromTheme(u"document-save"))
        self.actSave.setIcon(icon2)
        self.actSave.setMenuRole(QAction.NoRole)
        self.actSaveAs = QAction(MainWindow)
        self.actSaveAs.setObjectName(u"actSaveAs")
        icon3 = QIcon(QIcon.fromTheme(u"document-save-as"))
        self.actSaveAs.setIcon(icon3)
        self.actSaveAs.setMenuRole(QAction.NoRole)
        self.actQuit = QAction(MainWindow)
        self.actQuit.setObjectName(u"actQuit")
        icon4 = QIcon(QIcon.fromTheme(u"application-exit"))
        self.actQuit.setIcon(icon4)
        self.actQuit.setMenuRole(QAction.QuitRole)
        self.actRealtimeSave = QAction(MainWindow)
        self.actRealtimeSave.setObjectName(u"actRealtimeSave")
        self.actRealtimeSave.setCheckable(True)
        self.actRealtimeSave.setMenuRole(QAction.NoRole)
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.layCentralWidget = QVBoxLayout(self.centralWidget)
        self.layCentralWidget.setObjectName(u"layCentralWidget")
        self.layCentralWidget.setSizeConstraint(QLayout.SetNoConstraint)
        self.layCentralWidget.setContentsMargins(6, 6, 6, 6)
        self.layMainFolder = QHBoxLayout()
        self.layMainFolder.setObjectName(u"layMainFolder")
        self.layMainFolder.setSizeConstraint(QLayout.SetNoConstraint)
        self.pbnMainFolder = QPushButton(self.centralWidget)
        self.pbnMainFolder.setObjectName(u"pbnMainFolder")

        self.layMainFolder.addWidget(self.pbnMainFolder)

        self.txtMainFolder = QLineEdit(self.centralWidget)
        self.txtMainFolder.setObjectName(u"txtMainFolder")

        self.layMainFolder.addWidget(self.txtMainFolder)


        self.layCentralWidget.addLayout(self.layMainFolder)

        self.layPreset = QHBoxLayout()
        self.layPreset.setObjectName(u"layPreset")
        self.layPreset.setSizeConstraint(QLayout.SetNoConstraint)
        self.lblPreset = QLabel(self.centralWidget)
        self.lblPreset.setObjectName(u"lblPreset")

        self.layPreset.addWidget(self.lblPreset)

        self.lblPresetPrefix = QLabel(self.centralWidget)
        self.lblPresetPrefix.setObjectName(u"lblPresetPrefix")

        self.layPreset.addWidget(self.lblPresetPrefix)

        self.txtPreset = QLineEdit(self.centralWidget)
        self.txtPreset.setObjectName(u"txtPreset")

        self.layPreset.addWidget(self.txtPreset)

        self.lblSfzExt = QLabel(self.centralWidget)
        self.lblSfzExt.setObjectName(u"lblSfzExt")

        self.layPreset.addWidget(self.lblSfzExt)


        self.layCentralWidget.addLayout(self.layPreset)

        self.gbxGlobal = QGroupBox(self.centralWidget)
        self.gbxGlobal.setObjectName(u"gbxGlobal")
        self.layGlobalBox = QHBoxLayout(self.gbxGlobal)
        self.layGlobalBox.setObjectName(u"layGlobalBox")
        self.layGlobalBox.setSizeConstraint(QLayout.SetNoConstraint)
        self.layGlobalBox.setContentsMargins(6, 6, 6, 6)
        self.chkKeyswitch = QCheckBox(self.gbxGlobal)
        self.chkKeyswitch.setObjectName(u"chkKeyswitch")

        self.layGlobalBox.addWidget(self.chkKeyswitch)

        self.lblKeyswitchRange = QLabel(self.gbxGlobal)
        self.lblKeyswitchRange.setObjectName(u"lblKeyswitchRange")

        self.layGlobalBox.addWidget(self.lblKeyswitchRange)

        self.sbxKeyswitchLo = QSpinBox(self.gbxGlobal)
        self.sbxKeyswitchLo.setObjectName(u"sbxKeyswitchLo")

        self.layGlobalBox.addWidget(self.sbxKeyswitchLo)

        self.lblSep1 = QLabel(self.gbxGlobal)
        self.lblSep1.setObjectName(u"lblSep1")
        self.lblSep1.setText(u"-")

        self.layGlobalBox.addWidget(self.lblSep1)

        self.sbxKeyswitchHi = QSpinBox(self.gbxGlobal)
        self.sbxKeyswitchHi.setObjectName(u"sbxKeyswitchHi")

        self.layGlobalBox.addWidget(self.sbxKeyswitchHi)

        self.lblKeyswitchDefault = QLabel(self.gbxGlobal)
        self.lblKeyswitchDefault.setObjectName(u"lblKeyswitchDefault")

        self.layGlobalBox.addWidget(self.lblKeyswitchDefault)

        self.sbxKeyswitchDefault = QSpinBox(self.gbxGlobal)
        self.sbxKeyswitchDefault.setObjectName(u"sbxKeyswitchDefault")

        self.layGlobalBox.addWidget(self.sbxKeyswitchDefault)

        self.hspKeyswitch = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layGlobalBox.addItem(self.hspKeyswitch)


        self.layCentralWidget.addWidget(self.gbxGlobal)

        self.layKey = QHBoxLayout()
        self.layKey.setObjectName(u"layKey")
        self.layKey.setSizeConstraint(QLayout.SetNoConstraint)
        self.lblKey = QLabel(self.centralWidget)
        self.lblKey.setObjectName(u"lblKey")

        self.layKey.addWidget(self.lblKey)

        self.sbxKeyLo = QSpinBox(self.centralWidget)
        self.sbxKeyLo.setObjectName(u"sbxKeyLo")

        self.layKey.addWidget(self.sbxKeyLo)

        self.lblSep2 = QLabel(self.centralWidget)
        self.lblSep2.setObjectName(u"lblSep2")
        self.lblSep2.setText(u"-")

        self.layKey.addWidget(self.lblSep2)

        self.sbxKeyHi = QSpinBox(self.centralWidget)
        self.sbxKeyHi.setObjectName(u"sbxKeyHi")

        self.layKey.addWidget(self.sbxKeyHi)

        self.lblVel = QLabel(self.centralWidget)
        self.lblVel.setObjectName(u"lblVel")

        self.layKey.addWidget(self.lblVel)

        self.sbxVelLo = QSpinBox(self.centralWidget)
        self.sbxVelLo.setObjectName(u"sbxVelLo")

        self.layKey.addWidget(self.sbxVelLo)

        self.lblSep3 = QLabel(self.centralWidget)
        self.lblSep3.setObjectName(u"lblSep3")
        self.lblSep3.setText(u"-")

        self.layKey.addWidget(self.lblSep3)

        self.sbxVelHi = QSpinBox(self.centralWidget)
        self.sbxVelHi.setObjectName(u"sbxVelHi")

        self.layKey.addWidget(self.sbxVelHi)

        self.chkNoteOn = QCheckBox(self.centralWidget)
        self.chkNoteOn.setObjectName(u"chkNoteOn")

        self.layKey.addWidget(self.chkNoteOn)

        self.lblCc = QLabel(self.centralWidget)
        self.lblCc.setObjectName(u"lblCc")

        self.layKey.addWidget(self.lblCc)

        self.sbxCc = QSpinBox(self.centralWidget)
        self.sbxCc.setObjectName(u"sbxCc")

        self.layKey.addWidget(self.sbxCc)

        self.lblEqual = QLabel(self.centralWidget)
        self.lblEqual.setObjectName(u"lblEqual")
        self.lblEqual.setText(u"=")

        self.layKey.addWidget(self.lblEqual)

        self.sbxCcLo = QSpinBox(self.centralWidget)
        self.sbxCcLo.setObjectName(u"sbxCcLo")

        self.layKey.addWidget(self.sbxCcLo)

        self.lblSep = QLabel(self.centralWidget)
        self.lblSep.setObjectName(u"lblSep")
        self.lblSep.setText(u"-")

        self.layKey.addWidget(self.lblSep)

        self.sbxCcHi = QSpinBox(self.centralWidget)
        self.sbxCcHi.setObjectName(u"sbxCcHi")

        self.layKey.addWidget(self.sbxCcHi)

        self.hspKey = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layKey.addItem(self.hspKey)


        self.layCentralWidget.addLayout(self.layKey)

        self.layPackMap = QHBoxLayout()
        self.layPackMap.setObjectName(u"layPackMap")
        self.layPackMap.setSizeConstraint(QLayout.SetNoConstraint)
        self.lblPack = QLabel(self.centralWidget)
        self.lblPack.setObjectName(u"lblPack")

        self.layPackMap.addWidget(self.lblPack)

        self.cbxPack = QComboBox(self.centralWidget)
        self.cbxPack.setObjectName(u"cbxPack")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbxPack.sizePolicy().hasHeightForWidth())
        self.cbxPack.setSizePolicy(sizePolicy)

        self.layPackMap.addWidget(self.cbxPack)

        self.lblMap = QLabel(self.centralWidget)
        self.lblMap.setObjectName(u"lblMap")

        self.layPackMap.addWidget(self.lblMap)

        self.cbxMap = QComboBox(self.centralWidget)
        self.cbxMap.setObjectName(u"cbxMap")
        sizePolicy.setHeightForWidth(self.cbxMap.sizePolicy().hasHeightForWidth())
        self.cbxMap.setSizePolicy(sizePolicy)

        self.layPackMap.addWidget(self.cbxMap)

        self.chkPercussion = QCheckBox(self.centralWidget)
        self.chkPercussion.setObjectName(u"chkPercussion")

        self.layPackMap.addWidget(self.chkPercussion)


        self.layCentralWidget.addLayout(self.layPackMap)

        self.layRandom = QHBoxLayout()
        self.layRandom.setObjectName(u"layRandom")
        self.layRandom.setSizeConstraint(QLayout.SetNoConstraint)
        self.chkRandom = QCheckBox(self.centralWidget)
        self.chkRandom.setObjectName(u"chkRandom")

        self.layRandom.addWidget(self.chkRandom)

        self.lblRandomLo = QLabel(self.centralWidget)
        self.lblRandomLo.setObjectName(u"lblRandomLo")

        self.layRandom.addWidget(self.lblRandomLo)

        self.dsbRandomLo = QDoubleSpinBox(self.centralWidget)
        self.dsbRandomLo.setObjectName(u"dsbRandomLo")
        self.dsbRandomLo.setDecimals(3)
        self.dsbRandomLo.setMaximum(1.000000000000000)

        self.layRandom.addWidget(self.dsbRandomLo)

        self.lblRandomHi = QLabel(self.centralWidget)
        self.lblRandomHi.setObjectName(u"lblRandomHi")

        self.layRandom.addWidget(self.lblRandomHi)

        self.dsbRandomHi = QDoubleSpinBox(self.centralWidget)
        self.dsbRandomHi.setObjectName(u"dsbRandomHi")

        self.layRandom.addWidget(self.dsbRandomHi)

        self.lblVolume = QLabel(self.centralWidget)
        self.lblVolume.setObjectName(u"lblVolume")

        self.layRandom.addWidget(self.lblVolume)

        self.dsbVolume = QDoubleSpinBox(self.centralWidget)
        self.dsbVolume.setObjectName(u"dsbVolume")

        self.layRandom.addWidget(self.dsbVolume)

        self.hspRandom = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layRandom.addItem(self.hspRandom)


        self.layCentralWidget.addLayout(self.layRandom)

        self.splitter = QSplitter(self.centralWidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.listWidget = QListWidget(self.splitter)
        self.listWidget.setObjectName(u"listWidget")
        self.splitter.addWidget(self.listWidget)
        self.tabWidget = QTabWidget(self.splitter)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabMap = QWidget()
        self.tabMap.setObjectName(u"tabMap")
        self.gridLayout_6 = QGridLayout(self.tabMap)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.layOutput = QHBoxLayout()
        self.layOutput.setObjectName(u"layOutput")
        self.layOutput.setSizeConstraint(QLayout.SetNoConstraint)
        self.lblOutput = QLabel(self.tabMap)
        self.lblOutput.setObjectName(u"lblOutput")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lblOutput.sizePolicy().hasHeightForWidth())
        self.lblOutput.setSizePolicy(sizePolicy1)

        self.layOutput.addWidget(self.lblOutput)

        self.sbxOutput = QSpinBox(self.tabMap)
        self.sbxOutput.setObjectName(u"sbxOutput")

        self.layOutput.addWidget(self.sbxOutput)

        self.hspOutput = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layOutput.addItem(self.hspOutput)


        self.gridLayout_6.addLayout(self.layOutput, 0, 0, 1, 2)

        self.gbxPolyphony = QGroupBox(self.tabMap)
        self.gbxPolyphony.setObjectName(u"gbxPolyphony")
        self.LayGbxPolyphony = QGridLayout(self.gbxPolyphony)
        self.LayGbxPolyphony.setObjectName(u"LayGbxPolyphony")
        self.LayGbxPolyphony.setSizeConstraint(QLayout.SetNoConstraint)
        self.LayGbxPolyphony.setContentsMargins(6, 6, 6, 6)
        self.chkPolyphony = QCheckBox(self.gbxPolyphony)
        self.chkPolyphony.setObjectName(u"chkPolyphony")

        self.LayGbxPolyphony.addWidget(self.chkPolyphony, 0, 0, 1, 1)

        self.chkNoteSelfmask = QCheckBox(self.gbxPolyphony)
        self.chkNoteSelfmask.setObjectName(u"chkNoteSelfmask")

        self.LayGbxPolyphony.addWidget(self.chkNoteSelfmask, 2, 0, 1, 1)

        self.sbxNotePolyphony = QSpinBox(self.gbxPolyphony)
        self.sbxNotePolyphony.setObjectName(u"sbxNotePolyphony")

        self.LayGbxPolyphony.addWidget(self.sbxNotePolyphony, 1, 1, 1, 1)

        self.chkNotePolyphony = QCheckBox(self.gbxPolyphony)
        self.chkNotePolyphony.setObjectName(u"chkNotePolyphony")

        self.LayGbxPolyphony.addWidget(self.chkNotePolyphony, 1, 0, 1, 1)

        self.hspMapPolyphony = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.LayGbxPolyphony.addItem(self.hspMapPolyphony, 0, 2, 1, 1)

        self.sbxPolyphony = QSpinBox(self.gbxPolyphony)
        self.sbxPolyphony.setObjectName(u"sbxPolyphony")

        self.LayGbxPolyphony.addWidget(self.sbxPolyphony, 0, 1, 1, 1)


        self.gridLayout_6.addWidget(self.gbxPolyphony, 1, 0, 1, 1)

        self.gbxTrigger = QGroupBox(self.tabMap)
        self.gbxTrigger.setObjectName(u"gbxTrigger")
        self.layTrigger = QGridLayout(self.gbxTrigger)
        self.layTrigger.setObjectName(u"layTrigger")
        self.layTrigger.setSizeConstraint(QLayout.SetNoConstraint)
        self.layTrigger.setContentsMargins(6, 6, 6, 6)
        self.dsbRtDecay = QDoubleSpinBox(self.gbxTrigger)
        self.dsbRtDecay.setObjectName(u"dsbRtDecay")

        self.layTrigger.addWidget(self.dsbRtDecay, 3, 1, 1, 1)

        self.chkRtDecay = QCheckBox(self.gbxTrigger)
        self.chkRtDecay.setObjectName(u"chkRtDecay")

        self.layTrigger.addWidget(self.chkRtDecay, 3, 0, 1, 1)

        self.chkRtDead = QCheckBox(self.gbxTrigger)
        self.chkRtDead.setObjectName(u"chkRtDead")

        self.layTrigger.addWidget(self.chkRtDead, 2, 0, 1, 1)

        self.cbxRtDeadMode = QComboBox(self.gbxTrigger)
        self.cbxRtDeadMode.addItem("")
        self.cbxRtDeadMode.addItem("")
        self.cbxRtDeadMode.addItem("")
        self.cbxRtDeadMode.addItem("")
        self.cbxRtDeadMode.addItem("")
        self.cbxRtDeadMode.setObjectName(u"cbxRtDeadMode")

        self.layTrigger.addWidget(self.cbxRtDeadMode, 1, 1, 1, 1)

        self.lblTriggerMode = QLabel(self.gbxTrigger)
        self.lblTriggerMode.setObjectName(u"lblTriggerMode")

        self.layTrigger.addWidget(self.lblTriggerMode, 1, 0, 1, 1)


        self.gridLayout_6.addWidget(self.gbxTrigger, 1, 1, 1, 1)

        self.gbxKeyswitch = QGroupBox(self.tabMap)
        self.gbxKeyswitch.setObjectName(u"gbxKeyswitch")
        self.layGbxKeyswitch = QGridLayout(self.gbxKeyswitch)
        self.layGbxKeyswitch.setObjectName(u"layGbxKeyswitch")
        self.layGbxKeyswitch.setSizeConstraint(QLayout.SetNoConstraint)
        self.layGbxKeyswitch.setContentsMargins(6, 6, 6, 6)
        self.sbxKeyswitchCount = QSpinBox(self.gbxKeyswitch)
        self.sbxKeyswitchCount.setObjectName(u"sbxKeyswitchCount")

        self.layGbxKeyswitch.addWidget(self.sbxKeyswitchCount, 0, 1, 1, 1)

        self.lblKeyswitchLabel = QLabel(self.gbxKeyswitch)
        self.lblKeyswitchLabel.setObjectName(u"lblKeyswitchLabel")

        self.layGbxKeyswitch.addWidget(self.lblKeyswitchLabel, 1, 0, 1, 1)

        self.chkKeySwitchCount = QCheckBox(self.gbxKeyswitch)
        self.chkKeySwitchCount.setObjectName(u"chkKeySwitchCount")

        self.layGbxKeyswitch.addWidget(self.chkKeySwitchCount, 0, 0, 1, 1)

        self.hspKeyswitchCount = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layGbxKeyswitch.addItem(self.hspKeyswitchCount, 0, 2, 1, 1)

        self.txtKeyswitchLabel = QLineEdit(self.gbxKeyswitch)
        self.txtKeyswitchLabel.setObjectName(u"txtKeyswitchLabel")

        self.layGbxKeyswitch.addWidget(self.txtKeyswitchLabel, 1, 1, 1, 2)


        self.gridLayout_6.addWidget(self.gbxKeyswitch, 2, 0, 1, 1)

        self.gbxMapKey = QGroupBox(self.tabMap)
        self.gbxMapKey.setObjectName(u"gbxMapKey")
        self.layMapKey = QGridLayout(self.gbxMapKey)
        self.layMapKey.setObjectName(u"layMapKey")
        self.layMapKey.setSizeConstraint(QLayout.SetNoConstraint)
        self.layMapKey.setContentsMargins(6, 6, 6, 6)
        self.layUsePitchKeycenter4All = QHBoxLayout()
        self.layUsePitchKeycenter4All.setObjectName(u"layUsePitchKeycenter4All")
        self.layUsePitchKeycenter4All.setSizeConstraint(QLayout.SetNoConstraint)
        self.chkUseGlobalPitchKeycenter = QCheckBox(self.gbxMapKey)
        self.chkUseGlobalPitchKeycenter.setObjectName(u"chkUseGlobalPitchKeycenter")

        self.layUsePitchKeycenter4All.addWidget(self.chkUseGlobalPitchKeycenter)

        self.sbxUsePitchKeycenter4All = QSpinBox(self.gbxMapKey)
        self.sbxUsePitchKeycenter4All.setObjectName(u"sbxUsePitchKeycenter4All")

        self.layUsePitchKeycenter4All.addWidget(self.sbxUsePitchKeycenter4All)


        self.layMapKey.addLayout(self.layUsePitchKeycenter4All, 0, 0, 1, 1)

        self.chkUseKey = QCheckBox(self.gbxMapKey)
        self.chkUseKey.setObjectName(u"chkUseKey")

        self.layMapKey.addWidget(self.chkUseKey, 1, 0, 1, 1)


        self.gridLayout_6.addWidget(self.gbxMapKey, 2, 1, 1, 1)

        self.vspMap = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_6.addItem(self.vspMap, 3, 0, 1, 1)

        self.tabWidget.addTab(self.tabMap, "")
        self.tabSample = QWidget()
        self.tabSample.setObjectName(u"tabSample")
        self.laySample = QGridLayout(self.tabSample)
        self.laySample.setObjectName(u"laySample")
        self.laySample.setSizeConstraint(QLayout.SetNoConstraint)
        self.laySample.setContentsMargins(6, 6, 6, 6)
        self.gbxSampleOffset = QGroupBox(self.tabSample)
        self.gbxSampleOffset.setObjectName(u"gbxSampleOffset")
        self.gbxSampleOffset.setCheckable(True)
        self.laySampleOffset = QGridLayout(self.gbxSampleOffset)
        self.laySampleOffset.setObjectName(u"laySampleOffset")
        self.laySampleOffset.setSizeConstraint(QLayout.SetNoConstraint)
        self.laySampleOffset.setContentsMargins(6, 6, 6, 6)
        self.lblSampleOffsetRandom = QLabel(self.gbxSampleOffset)
        self.lblSampleOffsetRandom.setObjectName(u"lblSampleOffsetRandom")

        self.laySampleOffset.addWidget(self.lblSampleOffsetRandom, 3, 0, 1, 1)

        self.dsbSampleOffsetRandom = QDoubleSpinBox(self.gbxSampleOffset)
        self.dsbSampleOffsetRandom.setObjectName(u"dsbSampleOffsetRandom")

        self.laySampleOffset.addWidget(self.dsbSampleOffsetRandom, 3, 1, 1, 1)

        self.dsbSampleOffsetVelocity = QDoubleSpinBox(self.gbxSampleOffset)
        self.dsbSampleOffsetVelocity.setObjectName(u"dsbSampleOffsetVelocity")

        self.laySampleOffset.addWidget(self.dsbSampleOffsetVelocity, 4, 1, 1, 1)

        self.lblSampleOffsetVelocity = QLabel(self.gbxSampleOffset)
        self.lblSampleOffsetVelocity.setObjectName(u"lblSampleOffsetVelocity")

        self.laySampleOffset.addWidget(self.lblSampleOffsetVelocity, 4, 0, 1, 1)


        self.laySample.addWidget(self.gbxSampleOffset, 1, 0, 1, 1)

        self.gbxSampleGeneral = QGroupBox(self.tabSample)
        self.gbxSampleGeneral.setObjectName(u"gbxSampleGeneral")
        self.laySampleGeneral = QGridLayout(self.gbxSampleGeneral)
        self.laySampleGeneral.setObjectName(u"laySampleGeneral")
        self.laySampleGeneral.setSizeConstraint(QLayout.SetNoConstraint)
        self.laySampleGeneral.setContentsMargins(6, 6, 6, 6)
        self.cbxDirection = QComboBox(self.gbxSampleGeneral)
        self.cbxDirection.addItem("")
        self.cbxDirection.addItem("")
        self.cbxDirection.addItem("")
        self.cbxDirection.setObjectName(u"cbxDirection")

        self.laySampleGeneral.addWidget(self.cbxDirection, 3, 1, 1, 1)

        self.dsbSampleMapDelay = QDoubleSpinBox(self.gbxSampleGeneral)
        self.dsbSampleMapDelay.setObjectName(u"dsbSampleMapDelay")

        self.laySampleGeneral.addWidget(self.dsbSampleMapDelay, 0, 1, 1, 1)

        self.lblSampleQuality = QLabel(self.gbxSampleGeneral)
        self.lblSampleQuality.setObjectName(u"lblSampleQuality")

        self.laySampleGeneral.addWidget(self.lblSampleQuality, 1, 0, 1, 1)

        self.lblLoopMode = QLabel(self.gbxSampleGeneral)
        self.lblLoopMode.setObjectName(u"lblLoopMode")

        self.laySampleGeneral.addWidget(self.lblLoopMode, 2, 0, 1, 1)

        self.lblSampleMapDelay = QLabel(self.gbxSampleGeneral)
        self.lblSampleMapDelay.setObjectName(u"lblSampleMapDelay")

        self.laySampleGeneral.addWidget(self.lblSampleMapDelay, 0, 0, 1, 1)

        self.sbxSampleQuality = QSpinBox(self.gbxSampleGeneral)
        self.sbxSampleQuality.setObjectName(u"sbxSampleQuality")

        self.laySampleGeneral.addWidget(self.sbxSampleQuality, 1, 1, 1, 1)

        self.lblDirection = QLabel(self.gbxSampleGeneral)
        self.lblDirection.setObjectName(u"lblDirection")

        self.laySampleGeneral.addWidget(self.lblDirection, 3, 0, 1, 1)

        self.cbxLoopMode = QComboBox(self.gbxSampleGeneral)
        self.cbxLoopMode.addItem("")
        self.cbxLoopMode.addItem("")
        self.cbxLoopMode.addItem("")
        self.cbxLoopMode.addItem("")
        self.cbxLoopMode.addItem("")
        self.cbxLoopMode.setObjectName(u"cbxLoopMode")

        self.laySampleGeneral.addWidget(self.cbxLoopMode, 2, 1, 1, 1)


        self.laySample.addWidget(self.gbxSampleGeneral, 0, 0, 1, 1)

        self.gbxSampleRegion = QGroupBox(self.tabSample)
        self.gbxSampleRegion.setObjectName(u"gbxSampleRegion")
        self.laySampleRegion = QGridLayout(self.gbxSampleRegion)
        self.laySampleRegion.setObjectName(u"laySampleRegion")
        self.laySampleRegion.setSizeConstraint(QLayout.SetNoConstraint)
        self.laySampleRegion.setContentsMargins(6, 6, 6, 6)
        self.cbxOffTime = QComboBox(self.gbxSampleRegion)
        self.cbxOffTime.addItem("")
        self.cbxOffTime.addItem("")
        self.cbxOffTime.setObjectName(u"cbxOffTime")

        self.laySampleRegion.addWidget(self.cbxOffTime, 5, 1, 1, 1)

        self.sbxOffBy = QSpinBox(self.gbxSampleRegion)
        self.sbxOffBy.setObjectName(u"sbxOffBy")

        self.laySampleRegion.addWidget(self.sbxOffBy, 2, 1, 1, 1)

        self.lblGroup = QLabel(self.gbxSampleRegion)
        self.lblGroup.setObjectName(u"lblGroup")

        self.laySampleRegion.addWidget(self.lblGroup, 1, 0, 1, 1)

        self.cbxOffMode = QLabel(self.gbxSampleRegion)
        self.cbxOffMode.setObjectName(u"cbxOffMode")

        self.laySampleRegion.addWidget(self.cbxOffMode, 4, 1, 1, 1)

        self.lblOffTime = QLabel(self.gbxSampleRegion)
        self.lblOffTime.setObjectName(u"lblOffTime")

        self.laySampleRegion.addWidget(self.lblOffTime, 5, 0, 1, 1)

        self.dsbOffMode = QDoubleSpinBox(self.gbxSampleRegion)
        self.dsbOffMode.setObjectName(u"dsbOffMode")

        self.laySampleRegion.addWidget(self.dsbOffMode, 4, 1, 1, 1)

        self.lblOffBy = QLabel(self.gbxSampleRegion)
        self.lblOffBy.setObjectName(u"lblOffBy")

        self.laySampleRegion.addWidget(self.lblOffBy, 2, 0, 1, 1)

        self.lblOffMode = QLabel(self.gbxSampleRegion)
        self.lblOffMode.setObjectName(u"lblOffMode")

        self.laySampleRegion.addWidget(self.lblOffMode, 4, 0, 1, 1)

        self.sbxGroup = QSpinBox(self.gbxSampleRegion)
        self.sbxGroup.setObjectName(u"sbxGroup")

        self.laySampleRegion.addWidget(self.sbxGroup, 1, 1, 1, 1)

        self.chkRegionExclusiveClass = QCheckBox(self.gbxSampleRegion)
        self.chkRegionExclusiveClass.setObjectName(u"chkRegionExclusiveClass")

        self.laySampleRegion.addWidget(self.chkRegionExclusiveClass, 0, 0, 1, 3)


        self.laySample.addWidget(self.gbxSampleRegion, 0, 1, 1, 1)

        self.gbxSampleTranspose = QGroupBox(self.tabSample)
        self.gbxSampleTranspose.setObjectName(u"gbxSampleTranspose")
        self.laySampleTranspose = QGridLayout(self.gbxSampleTranspose)
        self.laySampleTranspose.setObjectName(u"laySampleTranspose")
        self.laySampleTranspose.setSizeConstraint(QLayout.SetNoConstraint)
        self.laySampleTranspose.setContentsMargins(6, 6, 6, 6)
        self.lblSampleTransposePitch = QLabel(self.gbxSampleTranspose)
        self.lblSampleTransposePitch.setObjectName(u"lblSampleTransposePitch")

        self.laySampleTranspose.addWidget(self.lblSampleTransposePitch, 0, 0, 1, 1)

        self.sbxSampleTransposePitch = QSpinBox(self.gbxSampleTranspose)
        self.sbxSampleTransposePitch.setObjectName(u"sbxSampleTransposePitch")

        self.laySampleTranspose.addWidget(self.sbxSampleTransposePitch, 0, 1, 1, 1)

        self.lblSampleTransposeNote = QLabel(self.gbxSampleTranspose)
        self.lblSampleTransposeNote.setObjectName(u"lblSampleTransposeNote")

        self.laySampleTranspose.addWidget(self.lblSampleTransposeNote, 1, 0, 1, 1)

        self.sbxSampleTransposeNote = QSpinBox(self.gbxSampleTranspose)
        self.sbxSampleTransposeNote.setObjectName(u"sbxSampleTransposeNote")

        self.laySampleTranspose.addWidget(self.sbxSampleTransposeNote, 1, 1, 1, 1)


        self.laySample.addWidget(self.gbxSampleTranspose, 1, 1, 1, 1)

        self.vspOffset = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.laySample.addItem(self.vspOffset, 2, 0, 1, 1)

        self.tabWidget.addTab(self.tabSample, "")
        self.tabPan = QWidget()
        self.tabPan.setObjectName(u"tabPan")
        self.layPan = QGridLayout(self.tabPan)
        self.layPan.setObjectName(u"layPan")
        self.layPan.setSizeConstraint(QLayout.SetNoConstraint)
        self.layPan.setContentsMargins(6, 6, 6, 6)
        self.vspPan = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layPan.addItem(self.vspPan, 2, 0, 1, 2)

        self.gbxPan = QGroupBox(self.tabPan)
        self.gbxPan.setObjectName(u"gbxPan")
        self.gbxPan.setCheckable(True)
        self.layGbxPan = QGridLayout(self.gbxPan)
        self.layGbxPan.setObjectName(u"layGbxPan")
        self.layGbxPan.setSizeConstraint(QLayout.SetNoConstraint)
        self.layGbxPan.setContentsMargins(6, 6, 6, 6)
        self.layPanKeycenter = QHBoxLayout()
        self.layPanKeycenter.setObjectName(u"layPanKeycenter")
        self.layPanKeycenter.setSizeConstraint(QLayout.SetNoConstraint)
        self.lblPanKeycenter = QLabel(self.gbxPan)
        self.lblPanKeycenter.setObjectName(u"lblPanKeycenter")

        self.layPanKeycenter.addWidget(self.lblPanKeycenter)

        self.sbxPanKeycenter = QSpinBox(self.gbxPan)
        self.sbxPanKeycenter.setObjectName(u"sbxPanKeycenter")

        self.layPanKeycenter.addWidget(self.sbxPanKeycenter)

        self.hspPanKeycenter = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layPanKeycenter.addItem(self.hspPanKeycenter)


        self.layGbxPan.addLayout(self.layPanKeycenter, 0, 0, 1, 1)

        self.layPanKnobs = QGridLayout()
        self.layPanKnobs.setObjectName(u"layPanKnobs")
        self.layPanKnobs.setSizeConstraint(QLayout.SetNoConstraint)
        self.lblPanRandom = QLabel(self.gbxPan)
        self.lblPanRandom.setObjectName(u"lblPanRandom")
        self.lblPanRandom.setAlignment(Qt.AlignCenter)

        self.layPanKnobs.addWidget(self.lblPanRandom, 0, 4, 1, 1)

        self.lblPanKeytrackVal = QLabel(self.gbxPan)
        self.lblPanKeytrackVal.setObjectName(u"lblPanKeytrackVal")
        self.lblPanKeytrackVal.setMinimumSize(QSize(64, 0))
        self.lblPanKeytrackVal.setAlignment(Qt.AlignCenter)

        self.layPanKnobs.addWidget(self.lblPanKeytrackVal, 2, 2, 1, 1)

        self.lblPanVal = QLabel(self.gbxPan)
        self.lblPanVal.setObjectName(u"lblPanVal")
        self.lblPanVal.setMinimumSize(QSize(64, 0))
        self.lblPanVal.setAlignment(Qt.AlignCenter)

        self.layPanKnobs.addWidget(self.lblPanVal, 2, 1, 1, 1)

        self.knbPanVeltrack = QDial(self.gbxPan)
        self.knbPanVeltrack.setObjectName(u"knbPanVeltrack")
        self.knbPanVeltrack.setMinimumSize(QSize(0, 48))
        self.knbPanVeltrack.setMaximumSize(QSize(16777215, 48))

        self.layPanKnobs.addWidget(self.knbPanVeltrack, 1, 3, 1, 1)

        self.knbPan = QDial(self.gbxPan)
        self.knbPan.setObjectName(u"knbPan")
        self.knbPan.setMinimumSize(QSize(0, 48))
        self.knbPan.setMaximumSize(QSize(16777215, 48))

        self.layPanKnobs.addWidget(self.knbPan, 1, 1, 1, 1)

        self.lblPan = QLabel(self.gbxPan)
        self.lblPan.setObjectName(u"lblPan")
        self.lblPan.setAlignment(Qt.AlignCenter)

        self.layPanKnobs.addWidget(self.lblPan, 0, 1, 1, 1)

        self.knbPanRandom = QDial(self.gbxPan)
        self.knbPanRandom.setObjectName(u"knbPanRandom")
        self.knbPanRandom.setMinimumSize(QSize(0, 48))
        self.knbPanRandom.setMaximumSize(QSize(16777215, 48))

        self.layPanKnobs.addWidget(self.knbPanRandom, 1, 4, 1, 1)

        self.lblPanVeltrackVal = QLabel(self.gbxPan)
        self.lblPanVeltrackVal.setObjectName(u"lblPanVeltrackVal")
        self.lblPanVeltrackVal.setMinimumSize(QSize(64, 0))
        self.lblPanVeltrackVal.setAlignment(Qt.AlignCenter)

        self.layPanKnobs.addWidget(self.lblPanVeltrackVal, 2, 3, 1, 1)

        self.lblPanRandomVal = QLabel(self.gbxPan)
        self.lblPanRandomVal.setObjectName(u"lblPanRandomVal")
        self.lblPanRandomVal.setMinimumSize(QSize(64, 0))
        self.lblPanRandomVal.setAlignment(Qt.AlignCenter)

        self.layPanKnobs.addWidget(self.lblPanRandomVal, 2, 4, 1, 1)

        self.lblPanKeytrack = QLabel(self.gbxPan)
        self.lblPanKeytrack.setObjectName(u"lblPanKeytrack")
        self.lblPanKeytrack.setAlignment(Qt.AlignCenter)

        self.layPanKnobs.addWidget(self.lblPanKeytrack, 0, 2, 1, 1)

        self.lblPanVeltrack = QLabel(self.gbxPan)
        self.lblPanVeltrack.setObjectName(u"lblPanVeltrack")
        self.lblPanVeltrack.setAlignment(Qt.AlignCenter)

        self.layPanKnobs.addWidget(self.lblPanVeltrack, 0, 3, 1, 1)

        self.knbPanKeytrack = QDial(self.gbxPan)
        self.knbPanKeytrack.setObjectName(u"knbPanKeytrack")
        self.knbPanKeytrack.setMinimumSize(QSize(0, 48))
        self.knbPanKeytrack.setMaximumSize(QSize(16777215, 48))

        self.layPanKnobs.addWidget(self.knbPanKeytrack, 1, 2, 1, 1)

        self.hspPanL = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layPanKnobs.addItem(self.hspPanL, 1, 0, 1, 1)

        self.hspPanR = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layPanKnobs.addItem(self.hspPanR, 1, 5, 1, 1)


        self.layGbxPan.addLayout(self.layPanKnobs, 1, 0, 1, 1)


        self.layPan.addWidget(self.gbxPan, 0, 0, 1, 2)

        self.tabWidget.addTab(self.tabPan, "")
        self.tabAmp = QWidget()
        self.tabAmp.setObjectName(u"tabAmp")
        self.gridLayout_4 = QGridLayout(self.tabAmp)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gbxAmpGeneral = QGroupBox(self.tabAmp)
        self.gbxAmpGeneral.setObjectName(u"gbxAmpGeneral")
        self.gbxAmpGeneral.setCheckable(True)
        self.gbxAmpGeneral.setChecked(True)
        self.layAmpGeneral = QGridLayout(self.gbxAmpGeneral)
        self.layAmpGeneral.setObjectName(u"layAmpGeneral")
        self.layAmpGeneral.setSizeConstraint(QLayout.SetNoConstraint)
        self.layAmpGeneral.setContentsMargins(6, 6, 6, 6)
        self.layAmpVelFloor = QHBoxLayout()
        self.layAmpVelFloor.setObjectName(u"layAmpVelFloor")
        self.layAmpVelFloor.setSizeConstraint(QLayout.SetNoConstraint)
        self.chkAmpVelFloor = QCheckBox(self.gbxAmpGeneral)
        self.chkAmpVelFloor.setObjectName(u"chkAmpVelFloor")

        self.layAmpVelFloor.addWidget(self.chkAmpVelFloor)

        self.sbxAmpVelFloor = QSpinBox(self.gbxAmpGeneral)
        self.sbxAmpVelFloor.setObjectName(u"sbxAmpVelFloor")

        self.layAmpVelFloor.addWidget(self.sbxAmpVelFloor)

        self.lblAmpKeycenter = QLabel(self.gbxAmpGeneral)
        self.lblAmpKeycenter.setObjectName(u"lblAmpKeycenter")

        self.layAmpVelFloor.addWidget(self.lblAmpKeycenter)

        self.sbxAmpKeycenter = QSpinBox(self.gbxAmpGeneral)
        self.sbxAmpKeycenter.setObjectName(u"sbxAmpKeycenter")

        self.layAmpVelFloor.addWidget(self.sbxAmpKeycenter)

        self.hspAmpVelFloor = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layAmpVelFloor.addItem(self.hspAmpVelFloor)


        self.layAmpGeneral.addLayout(self.layAmpVelFloor, 1, 0, 1, 2)

        self.layAmpKeyVeltrackRandom = QGridLayout()
        self.layAmpKeyVeltrackRandom.setObjectName(u"layAmpKeyVeltrackRandom")
        self.layAmpKeyVeltrackRandom.setSizeConstraint(QLayout.SetNoConstraint)
        self.lblAmpVeltrack = QLabel(self.gbxAmpGeneral)
        self.lblAmpVeltrack.setObjectName(u"lblAmpVeltrack")
        self.lblAmpVeltrack.setAlignment(Qt.AlignCenter)

        self.layAmpKeyVeltrackRandom.addWidget(self.lblAmpVeltrack, 0, 2, 1, 1)

        self.lblAmpKeytrack = QLabel(self.gbxAmpGeneral)
        self.lblAmpKeytrack.setObjectName(u"lblAmpKeytrack")
        self.lblAmpKeytrack.setAlignment(Qt.AlignCenter)

        self.layAmpKeyVeltrackRandom.addWidget(self.lblAmpKeytrack, 0, 1, 1, 1)

        self.lblAmpRandomVal = QLabel(self.gbxAmpGeneral)
        self.lblAmpRandomVal.setObjectName(u"lblAmpRandomVal")
        self.lblAmpRandomVal.setAlignment(Qt.AlignCenter)

        self.layAmpKeyVeltrackRandom.addWidget(self.lblAmpRandomVal, 2, 3, 1, 1)

        self.knbAmpVeltrack = QDial(self.gbxAmpGeneral)
        self.knbAmpVeltrack.setObjectName(u"knbAmpVeltrack")
        self.knbAmpVeltrack.setMaximumSize(QSize(16777215, 48))

        self.layAmpKeyVeltrackRandom.addWidget(self.knbAmpVeltrack, 1, 2, 1, 1)

        self.knbAmpRandom = QDial(self.gbxAmpGeneral)
        self.knbAmpRandom.setObjectName(u"knbAmpRandom")
        self.knbAmpRandom.setMaximumSize(QSize(16777215, 48))

        self.layAmpKeyVeltrackRandom.addWidget(self.knbAmpRandom, 1, 3, 1, 1)

        self.knbAmpKeytrack = QDial(self.gbxAmpGeneral)
        self.knbAmpKeytrack.setObjectName(u"knbAmpKeytrack")
        self.knbAmpKeytrack.setMaximumSize(QSize(16777215, 48))

        self.layAmpKeyVeltrackRandom.addWidget(self.knbAmpKeytrack, 1, 1, 1, 1)

        self.lblAmpVeltrackVal = QLabel(self.gbxAmpGeneral)
        self.lblAmpVeltrackVal.setObjectName(u"lblAmpVeltrackVal")
        self.lblAmpVeltrackVal.setAlignment(Qt.AlignCenter)

        self.layAmpKeyVeltrackRandom.addWidget(self.lblAmpVeltrackVal, 2, 2, 1, 1)

        self.hspAmpL = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layAmpKeyVeltrackRandom.addItem(self.hspAmpL, 1, 0, 1, 1)

        self.lblAmpRandom = QLabel(self.gbxAmpGeneral)
        self.lblAmpRandom.setObjectName(u"lblAmpRandom")
        self.lblAmpRandom.setAlignment(Qt.AlignCenter)

        self.layAmpKeyVeltrackRandom.addWidget(self.lblAmpRandom, 0, 3, 1, 1)

        self.lblAmpKeytrackVal = QLabel(self.gbxAmpGeneral)
        self.lblAmpKeytrackVal.setObjectName(u"lblAmpKeytrackVal")
        self.lblAmpKeytrackVal.setAlignment(Qt.AlignCenter)

        self.layAmpKeyVeltrackRandom.addWidget(self.lblAmpKeytrackVal, 2, 1, 1, 1)

        self.hspAmpR = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layAmpKeyVeltrackRandom.addItem(self.hspAmpR, 1, 4, 1, 1)


        self.layAmpGeneral.addLayout(self.layAmpKeyVeltrackRandom, 6, 0, 2, 2)

        self.layAmpVelAttack = QHBoxLayout()
        self.layAmpVelAttack.setObjectName(u"layAmpVelAttack")
        self.layAmpVelAttack.setSizeConstraint(QLayout.SetNoConstraint)
        self.chkAmpVelAttack = QCheckBox(self.gbxAmpGeneral)
        self.chkAmpVelAttack.setObjectName(u"chkAmpVelAttack")

        self.layAmpVelAttack.addWidget(self.chkAmpVelAttack)

        self.sbxAmpVelAttack = QSpinBox(self.gbxAmpGeneral)
        self.sbxAmpVelAttack.setObjectName(u"sbxAmpVelAttack")

        self.layAmpVelAttack.addWidget(self.sbxAmpVelAttack)

        self.hspAmpVelAttack = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layAmpVelAttack.addItem(self.hspAmpVelAttack)


        self.layAmpGeneral.addLayout(self.layAmpVelAttack, 2, 0, 1, 2)


        self.gridLayout_4.addWidget(self.gbxAmpGeneral, 0, 0, 1, 1)

        self.vspAmp = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.vspAmp, 2, 0, 1, 1)

        self.gbxAmpLfo = QGroupBox(self.tabAmp)
        self.gbxAmpLfo.setObjectName(u"gbxAmpLfo")
        self.gbxAmpLfo.setCheckable(True)
        self.layAmpLfo = QGridLayout(self.gbxAmpLfo)
        self.layAmpLfo.setObjectName(u"layAmpLfo")
        self.layAmpLfo.setSizeConstraint(QLayout.SetNoConstraint)
        self.layAmpLfo.setContentsMargins(6, 6, 6, 6)
        self.knbAmpLfoDepth = QDial(self.gbxAmpLfo)
        self.knbAmpLfoDepth.setObjectName(u"knbAmpLfoDepth")
        self.knbAmpLfoDepth.setMaximumSize(QSize(16777215, 48))
        self.knbAmpLfoDepth.setNotchesVisible(True)

        self.layAmpLfo.addWidget(self.knbAmpLfoDepth, 1, 3, 1, 1)

        self.lblAmpLfoFadeVal = QLabel(self.gbxAmpLfo)
        self.lblAmpLfoFadeVal.setObjectName(u"lblAmpLfoFadeVal")
        self.lblAmpLfoFadeVal.setAlignment(Qt.AlignCenter)

        self.layAmpLfo.addWidget(self.lblAmpLfoFadeVal, 2, 2, 1, 1)

        self.knbAmpLfoFade = QDial(self.gbxAmpLfo)
        self.knbAmpLfoFade.setObjectName(u"knbAmpLfoFade")
        self.knbAmpLfoFade.setMaximumSize(QSize(16777215, 48))
        self.knbAmpLfoFade.setNotchesVisible(True)

        self.layAmpLfo.addWidget(self.knbAmpLfoFade, 1, 2, 1, 1)

        self.knbAmpLfoFreq = QDial(self.gbxAmpLfo)
        self.knbAmpLfoFreq.setObjectName(u"knbAmpLfoFreq")
        self.knbAmpLfoFreq.setMaximumSize(QSize(16777215, 48))
        self.knbAmpLfoFreq.setNotchesVisible(True)

        self.layAmpLfo.addWidget(self.knbAmpLfoFreq, 1, 4, 1, 1)

        self.lblAmpLfoDepthVal = QLabel(self.gbxAmpLfo)
        self.lblAmpLfoDepthVal.setObjectName(u"lblAmpLfoDepthVal")
        self.lblAmpLfoDepthVal.setAlignment(Qt.AlignCenter)

        self.layAmpLfo.addWidget(self.lblAmpLfoDepthVal, 2, 3, 1, 1)

        self.lblAmpLfoDelayVal = QLabel(self.gbxAmpLfo)
        self.lblAmpLfoDelayVal.setObjectName(u"lblAmpLfoDelayVal")
        self.lblAmpLfoDelayVal.setAlignment(Qt.AlignCenter)

        self.layAmpLfo.addWidget(self.lblAmpLfoDelayVal, 2, 1, 1, 1)

        self.hspAmpLfoL = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layAmpLfo.addItem(self.hspAmpLfoL, 0, 0, 1, 1)

        self.lblAmpLfoDepth = QLabel(self.gbxAmpLfo)
        self.lblAmpLfoDepth.setObjectName(u"lblAmpLfoDepth")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lblAmpLfoDepth.sizePolicy().hasHeightForWidth())
        self.lblAmpLfoDepth.setSizePolicy(sizePolicy2)
        self.lblAmpLfoDepth.setAlignment(Qt.AlignCenter)

        self.layAmpLfo.addWidget(self.lblAmpLfoDepth, 0, 3, 1, 1)

        self.lblAmpLfoFreq = QLabel(self.gbxAmpLfo)
        self.lblAmpLfoFreq.setObjectName(u"lblAmpLfoFreq")
        sizePolicy2.setHeightForWidth(self.lblAmpLfoFreq.sizePolicy().hasHeightForWidth())
        self.lblAmpLfoFreq.setSizePolicy(sizePolicy2)
        self.lblAmpLfoFreq.setAlignment(Qt.AlignCenter)

        self.layAmpLfo.addWidget(self.lblAmpLfoFreq, 0, 4, 1, 1)

        self.lblAmpLfoFade = QLabel(self.gbxAmpLfo)
        self.lblAmpLfoFade.setObjectName(u"lblAmpLfoFade")
        sizePolicy2.setHeightForWidth(self.lblAmpLfoFade.sizePolicy().hasHeightForWidth())
        self.lblAmpLfoFade.setSizePolicy(sizePolicy2)
        self.lblAmpLfoFade.setAlignment(Qt.AlignCenter)

        self.layAmpLfo.addWidget(self.lblAmpLfoFade, 0, 2, 1, 1)

        self.lblAmpLfoFreqVal = QLabel(self.gbxAmpLfo)
        self.lblAmpLfoFreqVal.setObjectName(u"lblAmpLfoFreqVal")
        self.lblAmpLfoFreqVal.setAlignment(Qt.AlignCenter)

        self.layAmpLfo.addWidget(self.lblAmpLfoFreqVal, 2, 4, 1, 1)

        self.knbAmpLfoDelay = QDial(self.gbxAmpLfo)
        self.knbAmpLfoDelay.setObjectName(u"knbAmpLfoDelay")
        self.knbAmpLfoDelay.setMaximumSize(QSize(16777215, 48))
        self.knbAmpLfoDelay.setNotchesVisible(True)

        self.layAmpLfo.addWidget(self.knbAmpLfoDelay, 1, 1, 1, 1)

        self.hspAmpLfoR = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layAmpLfo.addItem(self.hspAmpLfoR, 0, 5, 1, 1)

        self.lblAmpLfoDelay = QLabel(self.gbxAmpLfo)
        self.lblAmpLfoDelay.setObjectName(u"lblAmpLfoDelay")
        sizePolicy2.setHeightForWidth(self.lblAmpLfoDelay.sizePolicy().hasHeightForWidth())
        self.lblAmpLfoDelay.setSizePolicy(sizePolicy2)
        self.lblAmpLfoDelay.setAlignment(Qt.AlignCenter)

        self.layAmpLfo.addWidget(self.lblAmpLfoDelay, 0, 1, 1, 1)


        self.gridLayout_4.addWidget(self.gbxAmpLfo, 1, 0, 1, 1)

        self.tabWidget.addTab(self.tabAmp, "")
        self.tabAmpEnv = QWidget()
        self.tabAmpEnv.setObjectName(u"tabAmpEnv")
        self.gridLayout_12 = QGridLayout(self.tabAmpEnv)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gbxAmpEnv = QGroupBox(self.tabAmpEnv)
        self.gbxAmpEnv.setObjectName(u"gbxAmpEnv")
        self.gbxAmpEnv.setCheckable(True)
        self.layAmpEnv = QGridLayout(self.gbxAmpEnv)
        self.layAmpEnv.setObjectName(u"layAmpEnv")
        self.layAmpEnv.setSizeConstraint(QLayout.SetNoConstraint)
        self.layAmpEnv.setContentsMargins(6, 6, 6, 6)
        self.gbxAmpEnvHold = QGroupBox(self.gbxAmpEnv)
        self.gbxAmpEnvHold.setObjectName(u"gbxAmpEnvHold")
        self.gbxAmpEnvHold.setAlignment(Qt.AlignCenter)
        self.layAmpEnvHold = QVBoxLayout(self.gbxAmpEnvHold)
        self.layAmpEnvHold.setObjectName(u"layAmpEnvHold")
        self.layAmpEnvHold.setSizeConstraint(QLayout.SetNoConstraint)
        self.layAmpEnvHold.setContentsMargins(6, 6, 6, 6)
        self.knbAmpEnvHold = QDial(self.gbxAmpEnvHold)
        self.knbAmpEnvHold.setObjectName(u"knbAmpEnvHold")
        self.knbAmpEnvHold.setMinimumSize(QSize(0, 48))
        self.knbAmpEnvHold.setMaximumSize(QSize(16777215, 48))

        self.layAmpEnvHold.addWidget(self.knbAmpEnvHold)

        self.lblAmpEnvHoldVal = QLabel(self.gbxAmpEnvHold)
        self.lblAmpEnvHoldVal.setObjectName(u"lblAmpEnvHoldVal")
        self.lblAmpEnvHoldVal.setAlignment(Qt.AlignCenter)

        self.layAmpEnvHold.addWidget(self.lblAmpEnvHoldVal)

        self.vspEnvAmpHold = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layAmpEnvHold.addItem(self.vspEnvAmpHold)

        self.layAmpEnvHold.setStretch(2, 1)

        self.layAmpEnv.addWidget(self.gbxAmpEnvHold, 0, 2, 1, 1)

        self.gbxAmpEnvDecay = QGroupBox(self.gbxAmpEnv)
        self.gbxAmpEnvDecay.setObjectName(u"gbxAmpEnvDecay")
        self.gbxAmpEnvDecay.setAlignment(Qt.AlignCenter)
        self.layAmpEnvDecay = QVBoxLayout(self.gbxAmpEnvDecay)
        self.layAmpEnvDecay.setObjectName(u"layAmpEnvDecay")
        self.layAmpEnvDecay.setSizeConstraint(QLayout.SetNoConstraint)
        self.layAmpEnvDecay.setContentsMargins(6, 6, 6, 6)
        self.knbAmpEnvDecay = QDial(self.gbxAmpEnvDecay)
        self.knbAmpEnvDecay.setObjectName(u"knbAmpEnvDecay")
        self.knbAmpEnvDecay.setMinimumSize(QSize(0, 48))
        self.knbAmpEnvDecay.setMaximumSize(QSize(16777215, 48))

        self.layAmpEnvDecay.addWidget(self.knbAmpEnvDecay)

        self.lblAmpEnvDecayVal = QLabel(self.gbxAmpEnvDecay)
        self.lblAmpEnvDecayVal.setObjectName(u"lblAmpEnvDecayVal")
        self.lblAmpEnvDecayVal.setAlignment(Qt.AlignCenter)

        self.layAmpEnvDecay.addWidget(self.lblAmpEnvDecayVal)

        self.line_2 = QFrame(self.gbxAmpEnvDecay)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.layAmpEnvDecay.addWidget(self.line_2)

        self.pbnAmpEnvDecayShapeEnable = QPushButton(self.gbxAmpEnvDecay)
        self.pbnAmpEnvDecayShapeEnable.setObjectName(u"pbnAmpEnvDecayShapeEnable")

        self.layAmpEnvDecay.addWidget(self.pbnAmpEnvDecayShapeEnable)

        self.pnlAmpEnvDecayShape = QWidget(self.gbxAmpEnvDecay)
        self.pnlAmpEnvDecayShape.setObjectName(u"pnlAmpEnvDecayShape")
        self.pnlAmpEnvDecayShape.setEnabled(False)
        self.layAmpEnvDecayShape = QVBoxLayout(self.pnlAmpEnvDecayShape)
        self.layAmpEnvDecayShape.setObjectName(u"layAmpEnvDecayShape")
        self.layAmpEnvDecayShape.setSizeConstraint(QLayout.SetNoConstraint)
        self.layAmpEnvDecayShape.setContentsMargins(6, 6, 6, 6)
        self.lblAmpEnvDecayShape = QLabel(self.pnlAmpEnvDecayShape)
        self.lblAmpEnvDecayShape.setObjectName(u"lblAmpEnvDecayShape")
        self.lblAmpEnvDecayShape.setAlignment(Qt.AlignCenter)

        self.layAmpEnvDecayShape.addWidget(self.lblAmpEnvDecayShape)

        self.knbAmpEnvDecayShape = QDial(self.pnlAmpEnvDecayShape)
        self.knbAmpEnvDecayShape.setObjectName(u"knbAmpEnvDecayShape")
        self.knbAmpEnvDecayShape.setMinimumSize(QSize(0, 48))
        self.knbAmpEnvDecayShape.setMaximumSize(QSize(16777215, 48))

        self.layAmpEnvDecayShape.addWidget(self.knbAmpEnvDecayShape)

        self.lblAmpEnvDecayShapeVal = QLabel(self.pnlAmpEnvDecayShape)
        self.lblAmpEnvDecayShapeVal.setObjectName(u"lblAmpEnvDecayShapeVal")
        self.lblAmpEnvDecayShapeVal.setAlignment(Qt.AlignCenter)

        self.layAmpEnvDecayShape.addWidget(self.lblAmpEnvDecayShapeVal)


        self.layAmpEnvDecay.addWidget(self.pnlAmpEnvDecayShape)

        self.pbnAmpEnvDecayShapeReset = QPushButton(self.gbxAmpEnvDecay)
        self.pbnAmpEnvDecayShapeReset.setObjectName(u"pbnAmpEnvDecayShapeReset")

        self.layAmpEnvDecay.addWidget(self.pbnAmpEnvDecayShapeReset)


        self.layAmpEnv.addWidget(self.gbxAmpEnvDecay, 0, 3, 1, 1)

        self.gbxAmpEnvDelay = QGroupBox(self.gbxAmpEnv)
        self.gbxAmpEnvDelay.setObjectName(u"gbxAmpEnvDelay")
        self.gbxAmpEnvDelay.setAlignment(Qt.AlignCenter)
        self.layAmpEnvDelay = QVBoxLayout(self.gbxAmpEnvDelay)
        self.layAmpEnvDelay.setObjectName(u"layAmpEnvDelay")
        self.layAmpEnvDelay.setSizeConstraint(QLayout.SetNoConstraint)
        self.layAmpEnvDelay.setContentsMargins(6, 6, 6, 6)
        self.knbAmpEnvDelay = QDial(self.gbxAmpEnvDelay)
        self.knbAmpEnvDelay.setObjectName(u"knbAmpEnvDelay")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.knbAmpEnvDelay.sizePolicy().hasHeightForWidth())
        self.knbAmpEnvDelay.setSizePolicy(sizePolicy3)
        self.knbAmpEnvDelay.setMinimumSize(QSize(0, 48))
        self.knbAmpEnvDelay.setMaximumSize(QSize(16777215, 48))

        self.layAmpEnvDelay.addWidget(self.knbAmpEnvDelay)

        self.lblAmpEnvDelayVal = QLabel(self.gbxAmpEnvDelay)
        self.lblAmpEnvDelayVal.setObjectName(u"lblAmpEnvDelayVal")
        sizePolicy3.setHeightForWidth(self.lblAmpEnvDelayVal.sizePolicy().hasHeightForWidth())
        self.lblAmpEnvDelayVal.setSizePolicy(sizePolicy3)
        self.lblAmpEnvDelayVal.setAlignment(Qt.AlignCenter)

        self.layAmpEnvDelay.addWidget(self.lblAmpEnvDelayVal)

        self.vspEnvAmpDelay = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layAmpEnvDelay.addItem(self.vspEnvAmpDelay)

        self.layAmpEnvDelay.setStretch(2, 1)

        self.layAmpEnv.addWidget(self.gbxAmpEnvDelay, 0, 0, 1, 1)

        self.gbxAmpEnvAttack = QGroupBox(self.gbxAmpEnv)
        self.gbxAmpEnvAttack.setObjectName(u"gbxAmpEnvAttack")
        self.gbxAmpEnvAttack.setAlignment(Qt.AlignCenter)
        self.layAmpEnvAttack = QVBoxLayout(self.gbxAmpEnvAttack)
        self.layAmpEnvAttack.setObjectName(u"layAmpEnvAttack")
        self.layAmpEnvAttack.setSizeConstraint(QLayout.SetNoConstraint)
        self.layAmpEnvAttack.setContentsMargins(6, 6, 6, 6)
        self.knbAmpEnvAttack = QDial(self.gbxAmpEnvAttack)
        self.knbAmpEnvAttack.setObjectName(u"knbAmpEnvAttack")
        self.knbAmpEnvAttack.setMinimumSize(QSize(0, 48))
        self.knbAmpEnvAttack.setMaximumSize(QSize(16777215, 48))

        self.layAmpEnvAttack.addWidget(self.knbAmpEnvAttack)

        self.lblAmpEnvAttackVal = QLabel(self.gbxAmpEnvAttack)
        self.lblAmpEnvAttackVal.setObjectName(u"lblAmpEnvAttackVal")
        self.lblAmpEnvAttackVal.setAlignment(Qt.AlignCenter)

        self.layAmpEnvAttack.addWidget(self.lblAmpEnvAttackVal)

        self.line = QFrame(self.gbxAmpEnvAttack)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.layAmpEnvAttack.addWidget(self.line)

        self.pbnAmpEnvAttackShapeEnable = QPushButton(self.gbxAmpEnvAttack)
        self.pbnAmpEnvAttackShapeEnable.setObjectName(u"pbnAmpEnvAttackShapeEnable")

        self.layAmpEnvAttack.addWidget(self.pbnAmpEnvAttackShapeEnable)

        self.pnlAmpEnvAttackShape = QWidget(self.gbxAmpEnvAttack)
        self.pnlAmpEnvAttackShape.setObjectName(u"pnlAmpEnvAttackShape")
        self.pnlAmpEnvAttackShape.setEnabled(False)
        self.layAmpEnvAttackShape = QVBoxLayout(self.pnlAmpEnvAttackShape)
        self.layAmpEnvAttackShape.setObjectName(u"layAmpEnvAttackShape")
        self.layAmpEnvAttackShape.setSizeConstraint(QLayout.SetNoConstraint)
        self.lblAmpEnvAttackShape = QLabel(self.pnlAmpEnvAttackShape)
        self.lblAmpEnvAttackShape.setObjectName(u"lblAmpEnvAttackShape")
        self.lblAmpEnvAttackShape.setAlignment(Qt.AlignCenter)

        self.layAmpEnvAttackShape.addWidget(self.lblAmpEnvAttackShape)

        self.knbAmpEnvAttackShape = QDial(self.pnlAmpEnvAttackShape)
        self.knbAmpEnvAttackShape.setObjectName(u"knbAmpEnvAttackShape")
        self.knbAmpEnvAttackShape.setMinimumSize(QSize(0, 48))
        self.knbAmpEnvAttackShape.setMaximumSize(QSize(16777215, 48))

        self.layAmpEnvAttackShape.addWidget(self.knbAmpEnvAttackShape)

        self.lblAmpEnvAttackShapeVal = QLabel(self.pnlAmpEnvAttackShape)
        self.lblAmpEnvAttackShapeVal.setObjectName(u"lblAmpEnvAttackShapeVal")
        self.lblAmpEnvAttackShapeVal.setAlignment(Qt.AlignCenter)

        self.layAmpEnvAttackShape.addWidget(self.lblAmpEnvAttackShapeVal)


        self.layAmpEnvAttack.addWidget(self.pnlAmpEnvAttackShape)

        self.pbnAmpEnvAttackShapeReset = QPushButton(self.gbxAmpEnvAttack)
        self.pbnAmpEnvAttackShapeReset.setObjectName(u"pbnAmpEnvAttackShapeReset")

        self.layAmpEnvAttack.addWidget(self.pbnAmpEnvAttackShapeReset)


        self.layAmpEnv.addWidget(self.gbxAmpEnvAttack, 0, 1, 1, 1)

        self.gbxAmpEnvSustain = QGroupBox(self.gbxAmpEnv)
        self.gbxAmpEnvSustain.setObjectName(u"gbxAmpEnvSustain")
        self.gbxAmpEnvSustain.setAlignment(Qt.AlignCenter)
        self.layAmpEnvSustain = QVBoxLayout(self.gbxAmpEnvSustain)
        self.layAmpEnvSustain.setObjectName(u"layAmpEnvSustain")
        self.layAmpEnvSustain.setSizeConstraint(QLayout.SetNoConstraint)
        self.layAmpEnvSustain.setContentsMargins(6, 6, 6, 6)
        self.knbAmpEnvSustain = QDial(self.gbxAmpEnvSustain)
        self.knbAmpEnvSustain.setObjectName(u"knbAmpEnvSustain")
        self.knbAmpEnvSustain.setMinimumSize(QSize(0, 48))
        self.knbAmpEnvSustain.setMaximumSize(QSize(16777215, 48))

        self.layAmpEnvSustain.addWidget(self.knbAmpEnvSustain)

        self.lblAmpEnvSustainVal = QLabel(self.gbxAmpEnvSustain)
        self.lblAmpEnvSustainVal.setObjectName(u"lblAmpEnvSustainVal")
        self.lblAmpEnvSustainVal.setAlignment(Qt.AlignCenter)

        self.layAmpEnvSustain.addWidget(self.lblAmpEnvSustainVal)

        self.vspEnvAmpSustain = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layAmpEnvSustain.addItem(self.vspEnvAmpSustain)

        self.layAmpEnvSustain.setStretch(2, 1)

        self.layAmpEnv.addWidget(self.gbxAmpEnvSustain, 0, 4, 1, 1)

        self.gbxAmpEnvRelease = QGroupBox(self.gbxAmpEnv)
        self.gbxAmpEnvRelease.setObjectName(u"gbxAmpEnvRelease")
        self.gbxAmpEnvRelease.setAlignment(Qt.AlignCenter)
        self.layAmpEnvRelease = QVBoxLayout(self.gbxAmpEnvRelease)
        self.layAmpEnvRelease.setObjectName(u"layAmpEnvRelease")
        self.layAmpEnvRelease.setSizeConstraint(QLayout.SetNoConstraint)
        self.layAmpEnvRelease.setContentsMargins(6, 6, 6, 6)
        self.knbAmpEnvRelease = QDial(self.gbxAmpEnvRelease)
        self.knbAmpEnvRelease.setObjectName(u"knbAmpEnvRelease")
        self.knbAmpEnvRelease.setMinimumSize(QSize(0, 48))
        self.knbAmpEnvRelease.setMaximumSize(QSize(16777215, 48))

        self.layAmpEnvRelease.addWidget(self.knbAmpEnvRelease)

        self.lblAmpEnvReleaseVal = QLabel(self.gbxAmpEnvRelease)
        self.lblAmpEnvReleaseVal.setObjectName(u"lblAmpEnvReleaseVal")
        self.lblAmpEnvReleaseVal.setAlignment(Qt.AlignCenter)

        self.layAmpEnvRelease.addWidget(self.lblAmpEnvReleaseVal)

        self.vspEnvAmpRelease = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layAmpEnvRelease.addItem(self.vspEnvAmpRelease)

        self.layAmpEnvRelease.setStretch(2, 1)

        self.layAmpEnv.addWidget(self.gbxAmpEnvRelease, 0, 5, 1, 1)

        self.vspAmpEnv = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layAmpEnv.addItem(self.vspAmpEnv, 1, 2, 1, 1)


        self.gridLayout_12.addWidget(self.gbxAmpEnv, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tabAmpEnv, "")
        self.tabFilter = QWidget()
        self.tabFilter.setObjectName(u"tabFilter")
        self.layFilter = QGridLayout(self.tabFilter)
        self.layFilter.setObjectName(u"layFilter")
        self.layFilter.setSizeConstraint(QLayout.SetNoConstraint)
        self.layFilter.setContentsMargins(6, 6, 6, 6)
        self.gbxFilterGeneral = QGroupBox(self.tabFilter)
        self.gbxFilterGeneral.setObjectName(u"gbxFilterGeneral")
        self.gbxFilterGeneral.setCheckable(True)
        self.layFilterGeneral = QGridLayout(self.gbxFilterGeneral)
        self.layFilterGeneral.setObjectName(u"layFilterGeneral")
        self.layFilterGeneral.setSizeConstraint(QLayout.SetNoConstraint)
        self.layFilterGeneral.setContentsMargins(6, 6, 6, 6)
        self.layFilterGeneralTop = QHBoxLayout()
        self.layFilterGeneralTop.setObjectName(u"layFilterGeneralTop")
        self.layFilterGeneralTop.setSizeConstraint(QLayout.SetNoConstraint)
        self.lblFilterType = QLabel(self.gbxFilterGeneral)
        self.lblFilterType.setObjectName(u"lblFilterType")

        self.layFilterGeneralTop.addWidget(self.lblFilterType)

        self.cbxFilterType = QComboBox(self.gbxFilterGeneral)
        self.cbxFilterType.addItem("")
        self.cbxFilterType.addItem("")
        self.cbxFilterType.addItem("")
        self.cbxFilterType.addItem("")
        self.cbxFilterType.addItem("")
        self.cbxFilterType.addItem("")
        self.cbxFilterType.setObjectName(u"cbxFilterType")

        self.layFilterGeneralTop.addWidget(self.cbxFilterType)

        self.lblFilterKeycenter = QLabel(self.gbxFilterGeneral)
        self.lblFilterKeycenter.setObjectName(u"lblFilterKeycenter")

        self.layFilterGeneralTop.addWidget(self.lblFilterKeycenter)

        self.sbxFilterKeycenter = QSpinBox(self.gbxFilterGeneral)
        self.sbxFilterKeycenter.setObjectName(u"sbxFilterKeycenter")

        self.layFilterGeneralTop.addWidget(self.sbxFilterKeycenter)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layFilterGeneralTop.addItem(self.horizontalSpacer)


        self.layFilterGeneral.addLayout(self.layFilterGeneralTop, 0, 0, 1, 7)

        self.layFilterGeneralKnobs = QGridLayout()
        self.layFilterGeneralKnobs.setObjectName(u"layFilterGeneralKnobs")
        self.layFilterGeneralKnobs.setSizeConstraint(QLayout.SetNoConstraint)
        self.lblFilterRandomVal = QLabel(self.gbxFilterGeneral)
        self.lblFilterRandomVal.setObjectName(u"lblFilterRandomVal")
        self.lblFilterRandomVal.setAlignment(Qt.AlignCenter)

        self.layFilterGeneralKnobs.addWidget(self.lblFilterRandomVal, 2, 5, 1, 1)

        self.hspFilterL = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layFilterGeneralKnobs.addItem(self.hspFilterL, 1, 0, 1, 1)

        self.lblFilterVeltrackVal = QLabel(self.gbxFilterGeneral)
        self.lblFilterVeltrackVal.setObjectName(u"lblFilterVeltrackVal")
        self.lblFilterVeltrackVal.setAlignment(Qt.AlignCenter)

        self.layFilterGeneralKnobs.addWidget(self.lblFilterVeltrackVal, 2, 4, 1, 1)

        self.lblFilterCutoff = QLabel(self.gbxFilterGeneral)
        self.lblFilterCutoff.setObjectName(u"lblFilterCutoff")
        sizePolicy2.setHeightForWidth(self.lblFilterCutoff.sizePolicy().hasHeightForWidth())
        self.lblFilterCutoff.setSizePolicy(sizePolicy2)
        self.lblFilterCutoff.setAlignment(Qt.AlignCenter)

        self.layFilterGeneralKnobs.addWidget(self.lblFilterCutoff, 0, 1, 1, 1)

        self.knbFilterCutoff = QDial(self.gbxFilterGeneral)
        self.knbFilterCutoff.setObjectName(u"knbFilterCutoff")
        sizePolicy2.setHeightForWidth(self.knbFilterCutoff.sizePolicy().hasHeightForWidth())
        self.knbFilterCutoff.setSizePolicy(sizePolicy2)
        self.knbFilterCutoff.setMaximumSize(QSize(16777215, 48))
        self.knbFilterCutoff.setNotchesVisible(True)

        self.layFilterGeneralKnobs.addWidget(self.knbFilterCutoff, 1, 1, 1, 1)

        self.knbFilterKeytrack = QDial(self.gbxFilterGeneral)
        self.knbFilterKeytrack.setObjectName(u"knbFilterKeytrack")
        self.knbFilterKeytrack.setMaximumSize(QSize(16777215, 48))
        self.knbFilterKeytrack.setNotchesVisible(True)

        self.layFilterGeneralKnobs.addWidget(self.knbFilterKeytrack, 1, 3, 1, 1)

        self.lblFilterResonanceVal = QLabel(self.gbxFilterGeneral)
        self.lblFilterResonanceVal.setObjectName(u"lblFilterResonanceVal")
        self.lblFilterResonanceVal.setAlignment(Qt.AlignCenter)

        self.layFilterGeneralKnobs.addWidget(self.lblFilterResonanceVal, 2, 2, 1, 1)

        self.knbFilterRandom = QDial(self.gbxFilterGeneral)
        self.knbFilterRandom.setObjectName(u"knbFilterRandom")
        self.knbFilterRandom.setMaximumSize(QSize(16777215, 48))
        self.knbFilterRandom.setNotchesVisible(True)

        self.layFilterGeneralKnobs.addWidget(self.knbFilterRandom, 1, 5, 1, 1)

        self.knbFilterResonance = QDial(self.gbxFilterGeneral)
        self.knbFilterResonance.setObjectName(u"knbFilterResonance")
        self.knbFilterResonance.setMaximumSize(QSize(16777215, 48))
        self.knbFilterResonance.setNotchesVisible(True)

        self.layFilterGeneralKnobs.addWidget(self.knbFilterResonance, 1, 2, 1, 1)

        self.lblFilterCutoffVal = QLabel(self.gbxFilterGeneral)
        self.lblFilterCutoffVal.setObjectName(u"lblFilterCutoffVal")
        self.lblFilterCutoffVal.setAlignment(Qt.AlignCenter)

        self.layFilterGeneralKnobs.addWidget(self.lblFilterCutoffVal, 2, 1, 1, 1)

        self.lblFilterVeltrack = QLabel(self.gbxFilterGeneral)
        self.lblFilterVeltrack.setObjectName(u"lblFilterVeltrack")
        sizePolicy2.setHeightForWidth(self.lblFilterVeltrack.sizePolicy().hasHeightForWidth())
        self.lblFilterVeltrack.setSizePolicy(sizePolicy2)
        self.lblFilterVeltrack.setAlignment(Qt.AlignCenter)

        self.layFilterGeneralKnobs.addWidget(self.lblFilterVeltrack, 0, 4, 1, 1)

        self.knbFilterVeltrack = QDial(self.gbxFilterGeneral)
        self.knbFilterVeltrack.setObjectName(u"knbFilterVeltrack")
        self.knbFilterVeltrack.setMaximumSize(QSize(16777215, 48))
        self.knbFilterVeltrack.setNotchesVisible(True)

        self.layFilterGeneralKnobs.addWidget(self.knbFilterVeltrack, 1, 4, 1, 1)

        self.lblFilterRandom = QLabel(self.gbxFilterGeneral)
        self.lblFilterRandom.setObjectName(u"lblFilterRandom")
        sizePolicy2.setHeightForWidth(self.lblFilterRandom.sizePolicy().hasHeightForWidth())
        self.lblFilterRandom.setSizePolicy(sizePolicy2)
        self.lblFilterRandom.setAlignment(Qt.AlignCenter)

        self.layFilterGeneralKnobs.addWidget(self.lblFilterRandom, 0, 5, 1, 1)

        self.lblFilterKeytrack = QLabel(self.gbxFilterGeneral)
        self.lblFilterKeytrack.setObjectName(u"lblFilterKeytrack")
        sizePolicy2.setHeightForWidth(self.lblFilterKeytrack.sizePolicy().hasHeightForWidth())
        self.lblFilterKeytrack.setSizePolicy(sizePolicy2)
        self.lblFilterKeytrack.setAlignment(Qt.AlignCenter)

        self.layFilterGeneralKnobs.addWidget(self.lblFilterKeytrack, 0, 3, 1, 1)

        self.lblFilterKeytrackVal = QLabel(self.gbxFilterGeneral)
        self.lblFilterKeytrackVal.setObjectName(u"lblFilterKeytrackVal")
        self.lblFilterKeytrackVal.setAlignment(Qt.AlignCenter)

        self.layFilterGeneralKnobs.addWidget(self.lblFilterKeytrackVal, 2, 3, 1, 1)

        self.lblFilterResonance = QLabel(self.gbxFilterGeneral)
        self.lblFilterResonance.setObjectName(u"lblFilterResonance")
        sizePolicy2.setHeightForWidth(self.lblFilterResonance.sizePolicy().hasHeightForWidth())
        self.lblFilterResonance.setSizePolicy(sizePolicy2)
        self.lblFilterResonance.setAlignment(Qt.AlignCenter)

        self.layFilterGeneralKnobs.addWidget(self.lblFilterResonance, 0, 2, 1, 1)

        self.hspFilterR = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layFilterGeneralKnobs.addItem(self.hspFilterR, 1, 6, 1, 1)


        self.layFilterGeneral.addLayout(self.layFilterGeneralKnobs, 2, 0, 1, 7)


        self.layFilter.addWidget(self.gbxFilterGeneral, 0, 0, 1, 1)

        self.gbxFilterLfo = QGroupBox(self.tabFilter)
        self.gbxFilterLfo.setObjectName(u"gbxFilterLfo")
        self.gbxFilterLfo.setCheckable(True)
        self.layFilterLfo = QGridLayout(self.gbxFilterLfo)
        self.layFilterLfo.setObjectName(u"layFilterLfo")
        self.layFilterLfo.setSizeConstraint(QLayout.SetNoConstraint)
        self.layFilterLfo.setContentsMargins(6, 6, 6, 6)
        self.knbFilterLfoDepth = QDial(self.gbxFilterLfo)
        self.knbFilterLfoDepth.setObjectName(u"knbFilterLfoDepth")
        self.knbFilterLfoDepth.setMaximumSize(QSize(16777215, 48))
        self.knbFilterLfoDepth.setNotchesVisible(True)

        self.layFilterLfo.addWidget(self.knbFilterLfoDepth, 1, 3, 1, 1)

        self.lblFilterLfoFadeVal = QLabel(self.gbxFilterLfo)
        self.lblFilterLfoFadeVal.setObjectName(u"lblFilterLfoFadeVal")
        self.lblFilterLfoFadeVal.setAlignment(Qt.AlignCenter)

        self.layFilterLfo.addWidget(self.lblFilterLfoFadeVal, 2, 2, 1, 1)

        self.knbFilterLfoFade = QDial(self.gbxFilterLfo)
        self.knbFilterLfoFade.setObjectName(u"knbFilterLfoFade")
        self.knbFilterLfoFade.setMaximumSize(QSize(16777215, 48))
        self.knbFilterLfoFade.setNotchesVisible(True)

        self.layFilterLfo.addWidget(self.knbFilterLfoFade, 1, 2, 1, 1)

        self.knbFilterLfoFreq = QDial(self.gbxFilterLfo)
        self.knbFilterLfoFreq.setObjectName(u"knbFilterLfoFreq")
        self.knbFilterLfoFreq.setMaximumSize(QSize(16777215, 48))
        self.knbFilterLfoFreq.setNotchesVisible(True)

        self.layFilterLfo.addWidget(self.knbFilterLfoFreq, 1, 4, 1, 1)

        self.lblFilterLfoDepthVal = QLabel(self.gbxFilterLfo)
        self.lblFilterLfoDepthVal.setObjectName(u"lblFilterLfoDepthVal")
        self.lblFilterLfoDepthVal.setAlignment(Qt.AlignCenter)

        self.layFilterLfo.addWidget(self.lblFilterLfoDepthVal, 2, 3, 1, 1)

        self.lblFilterLfoDelayVal = QLabel(self.gbxFilterLfo)
        self.lblFilterLfoDelayVal.setObjectName(u"lblFilterLfoDelayVal")
        self.lblFilterLfoDelayVal.setAlignment(Qt.AlignCenter)

        self.layFilterLfo.addWidget(self.lblFilterLfoDelayVal, 2, 1, 1, 1)

        self.lblFilterLfoDepth = QLabel(self.gbxFilterLfo)
        self.lblFilterLfoDepth.setObjectName(u"lblFilterLfoDepth")
        sizePolicy2.setHeightForWidth(self.lblFilterLfoDepth.sizePolicy().hasHeightForWidth())
        self.lblFilterLfoDepth.setSizePolicy(sizePolicy2)
        self.lblFilterLfoDepth.setAlignment(Qt.AlignCenter)

        self.layFilterLfo.addWidget(self.lblFilterLfoDepth, 0, 3, 1, 1)

        self.lblFilterLfoFreq = QLabel(self.gbxFilterLfo)
        self.lblFilterLfoFreq.setObjectName(u"lblFilterLfoFreq")
        sizePolicy2.setHeightForWidth(self.lblFilterLfoFreq.sizePolicy().hasHeightForWidth())
        self.lblFilterLfoFreq.setSizePolicy(sizePolicy2)
        self.lblFilterLfoFreq.setAlignment(Qt.AlignCenter)

        self.layFilterLfo.addWidget(self.lblFilterLfoFreq, 0, 4, 1, 1)

        self.lblFilterLfoFade = QLabel(self.gbxFilterLfo)
        self.lblFilterLfoFade.setObjectName(u"lblFilterLfoFade")
        sizePolicy2.setHeightForWidth(self.lblFilterLfoFade.sizePolicy().hasHeightForWidth())
        self.lblFilterLfoFade.setSizePolicy(sizePolicy2)
        self.lblFilterLfoFade.setAlignment(Qt.AlignCenter)

        self.layFilterLfo.addWidget(self.lblFilterLfoFade, 0, 2, 1, 1)

        self.lblFilterLfoFreqVal = QLabel(self.gbxFilterLfo)
        self.lblFilterLfoFreqVal.setObjectName(u"lblFilterLfoFreqVal")
        self.lblFilterLfoFreqVal.setAlignment(Qt.AlignCenter)

        self.layFilterLfo.addWidget(self.lblFilterLfoFreqVal, 2, 4, 1, 1)

        self.knbFilterLfoDelay = QDial(self.gbxFilterLfo)
        self.knbFilterLfoDelay.setObjectName(u"knbFilterLfoDelay")
        self.knbFilterLfoDelay.setMaximumSize(QSize(16777215, 48))
        self.knbFilterLfoDelay.setNotchesVisible(True)

        self.layFilterLfo.addWidget(self.knbFilterLfoDelay, 1, 1, 1, 1)

        self.lblFilterLfoDelay = QLabel(self.gbxFilterLfo)
        self.lblFilterLfoDelay.setObjectName(u"lblFilterLfoDelay")
        sizePolicy2.setHeightForWidth(self.lblFilterLfoDelay.sizePolicy().hasHeightForWidth())
        self.lblFilterLfoDelay.setSizePolicy(sizePolicy2)
        self.lblFilterLfoDelay.setAlignment(Qt.AlignCenter)

        self.layFilterLfo.addWidget(self.lblFilterLfoDelay, 0, 1, 1, 1)

        self.hspFilterLfoL = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layFilterLfo.addItem(self.hspFilterLfoL, 1, 0, 1, 1)

        self.hspFilterLfoR = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layFilterLfo.addItem(self.hspFilterLfoR, 1, 5, 1, 1)


        self.layFilter.addWidget(self.gbxFilterLfo, 1, 0, 1, 1)

        self.vspFilter = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layFilter.addItem(self.vspFilter, 2, 0, 1, 1)

        self.tabWidget.addTab(self.tabFilter, "")
        self.tabEnvFilter = QWidget()
        self.tabEnvFilter.setObjectName(u"tabEnvFilter")
        self.verticalLayout_22 = QVBoxLayout(self.tabEnvFilter)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.gbxFilEnv = QGroupBox(self.tabEnvFilter)
        self.gbxFilEnv.setObjectName(u"gbxFilEnv")
        self.gbxFilEnv.setCheckable(True)
        self.gridLayout_16 = QGridLayout(self.gbxFilEnv)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.vspFilEnv = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_16.addItem(self.vspFilEnv, 1, 4, 1, 1)

        self.gbxFilEnvDecay = QGroupBox(self.gbxFilEnv)
        self.gbxFilEnvDecay.setObjectName(u"gbxFilEnvDecay")
        self.gbxFilEnvDecay.setAlignment(Qt.AlignCenter)
        self.layFilEnvDecay = QVBoxLayout(self.gbxFilEnvDecay)
        self.layFilEnvDecay.setObjectName(u"layFilEnvDecay")
        self.layFilEnvDecay.setSizeConstraint(QLayout.SetNoConstraint)
        self.layFilEnvDecay.setContentsMargins(6, 6, 6, 6)
        self.knbFilEnvDecay = QDial(self.gbxFilEnvDecay)
        self.knbFilEnvDecay.setObjectName(u"knbFilEnvDecay")
        self.knbFilEnvDecay.setMinimumSize(QSize(0, 48))
        self.knbFilEnvDecay.setMaximumSize(QSize(16777215, 48))

        self.layFilEnvDecay.addWidget(self.knbFilEnvDecay)

        self.lblFilEnvDecayVal = QLabel(self.gbxFilEnvDecay)
        self.lblFilEnvDecayVal.setObjectName(u"lblFilEnvDecayVal")
        self.lblFilEnvDecayVal.setAlignment(Qt.AlignCenter)

        self.layFilEnvDecay.addWidget(self.lblFilEnvDecayVal)

        self.vspFilEnvDecay = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layFilEnvDecay.addItem(self.vspFilEnvDecay)

        self.layFilEnvDecay.setStretch(2, 1)

        self.gridLayout_16.addWidget(self.gbxFilEnvDecay, 0, 4, 1, 1)

        self.gbxFilEnvDepth = QGroupBox(self.gbxFilEnv)
        self.gbxFilEnvDepth.setObjectName(u"gbxFilEnvDepth")
        self.gbxFilEnvDepth.setAlignment(Qt.AlignCenter)
        self.layFilEnvDepth = QVBoxLayout(self.gbxFilEnvDepth)
        self.layFilEnvDepth.setObjectName(u"layFilEnvDepth")
        self.layFilEnvDepth.setSizeConstraint(QLayout.SetNoConstraint)
        self.layFilEnvDepth.setContentsMargins(6, 6, 6, 6)
        self.knbFilEnvDepth = QDial(self.gbxFilEnvDepth)
        self.knbFilEnvDepth.setObjectName(u"knbFilEnvDepth")
        self.knbFilEnvDepth.setMinimumSize(QSize(0, 48))
        self.knbFilEnvDepth.setMaximumSize(QSize(16777215, 48))

        self.layFilEnvDepth.addWidget(self.knbFilEnvDepth)

        self.lblFilEnvDepthVal = QLabel(self.gbxFilEnvDepth)
        self.lblFilEnvDepthVal.setObjectName(u"lblFilEnvDepthVal")
        self.lblFilEnvDepthVal.setAlignment(Qt.AlignCenter)

        self.layFilEnvDepth.addWidget(self.lblFilEnvDepthVal)

        self.vspFilEnvDepth = QSpacerItem(20, 65, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layFilEnvDepth.addItem(self.vspFilEnvDepth)


        self.gridLayout_16.addWidget(self.gbxFilEnvDepth, 0, 7, 1, 1)

        self.gbxFilEnvDelay = QGroupBox(self.gbxFilEnv)
        self.gbxFilEnvDelay.setObjectName(u"gbxFilEnvDelay")
        self.gbxFilEnvDelay.setAlignment(Qt.AlignCenter)
        self.layFilEnvDelay = QVBoxLayout(self.gbxFilEnvDelay)
        self.layFilEnvDelay.setObjectName(u"layFilEnvDelay")
        self.layFilEnvDelay.setSizeConstraint(QLayout.SetNoConstraint)
        self.layFilEnvDelay.setContentsMargins(6, 6, 6, 6)
        self.knbFilEnvDelay = QDial(self.gbxFilEnvDelay)
        self.knbFilEnvDelay.setObjectName(u"knbFilEnvDelay")
        self.knbFilEnvDelay.setMinimumSize(QSize(0, 48))
        self.knbFilEnvDelay.setMaximumSize(QSize(16777215, 48))

        self.layFilEnvDelay.addWidget(self.knbFilEnvDelay)

        self.lblFilEnvDelayVal = QLabel(self.gbxFilEnvDelay)
        self.lblFilEnvDelayVal.setObjectName(u"lblFilEnvDelayVal")
        sizePolicy3.setHeightForWidth(self.lblFilEnvDelayVal.sizePolicy().hasHeightForWidth())
        self.lblFilEnvDelayVal.setSizePolicy(sizePolicy3)
        self.lblFilEnvDelayVal.setAlignment(Qt.AlignCenter)

        self.layFilEnvDelay.addWidget(self.lblFilEnvDelayVal)

        self.vspFilEnvDelay = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layFilEnvDelay.addItem(self.vspFilEnvDelay)

        self.layFilEnvDelay.setStretch(2, 1)

        self.gridLayout_16.addWidget(self.gbxFilEnvDelay, 0, 1, 1, 1)

        self.gbxFilEnvHold = QGroupBox(self.gbxFilEnv)
        self.gbxFilEnvHold.setObjectName(u"gbxFilEnvHold")
        self.gbxFilEnvHold.setAlignment(Qt.AlignCenter)
        self.layFilEnvHold = QVBoxLayout(self.gbxFilEnvHold)
        self.layFilEnvHold.setObjectName(u"layFilEnvHold")
        self.layFilEnvHold.setSizeConstraint(QLayout.SetNoConstraint)
        self.layFilEnvHold.setContentsMargins(6, 6, 6, 6)
        self.knbFilEnvHold = QDial(self.gbxFilEnvHold)
        self.knbFilEnvHold.setObjectName(u"knbFilEnvHold")
        self.knbFilEnvHold.setMinimumSize(QSize(0, 48))
        self.knbFilEnvHold.setMaximumSize(QSize(16777215, 48))

        self.layFilEnvHold.addWidget(self.knbFilEnvHold)

        self.lblFilEnvHoldVal = QLabel(self.gbxFilEnvHold)
        self.lblFilEnvHoldVal.setObjectName(u"lblFilEnvHoldVal")
        self.lblFilEnvHoldVal.setAlignment(Qt.AlignCenter)

        self.layFilEnvHold.addWidget(self.lblFilEnvHoldVal)

        self.vspFilEnvHold = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layFilEnvHold.addItem(self.vspFilEnvHold)

        self.layFilEnvHold.setStretch(2, 1)

        self.gridLayout_16.addWidget(self.gbxFilEnvHold, 0, 3, 1, 1)

        self.hspFilEnvL = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_16.addItem(self.hspFilEnvL, 0, 0, 1, 1)

        self.gbxFilEnvRelease = QGroupBox(self.gbxFilEnv)
        self.gbxFilEnvRelease.setObjectName(u"gbxFilEnvRelease")
        self.gbxFilEnvRelease.setAlignment(Qt.AlignCenter)
        self.layFilEnvRelease = QVBoxLayout(self.gbxFilEnvRelease)
        self.layFilEnvRelease.setObjectName(u"layFilEnvRelease")
        self.layFilEnvRelease.setSizeConstraint(QLayout.SetNoConstraint)
        self.layFilEnvRelease.setContentsMargins(6, 6, 6, 6)
        self.knbFilEnvRelease = QDial(self.gbxFilEnvRelease)
        self.knbFilEnvRelease.setObjectName(u"knbFilEnvRelease")
        self.knbFilEnvRelease.setMinimumSize(QSize(0, 48))
        self.knbFilEnvRelease.setMaximumSize(QSize(16777215, 48))

        self.layFilEnvRelease.addWidget(self.knbFilEnvRelease)

        self.lblFilEnvReleaseVal = QLabel(self.gbxFilEnvRelease)
        self.lblFilEnvReleaseVal.setObjectName(u"lblFilEnvReleaseVal")
        self.lblFilEnvReleaseVal.setAlignment(Qt.AlignCenter)

        self.layFilEnvRelease.addWidget(self.lblFilEnvReleaseVal)

        self.vspFilEnvRelease = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layFilEnvRelease.addItem(self.vspFilEnvRelease)

        self.layFilEnvRelease.setStretch(2, 1)

        self.gridLayout_16.addWidget(self.gbxFilEnvRelease, 0, 6, 1, 1)

        self.gbxFilEnvAttack = QGroupBox(self.gbxFilEnv)
        self.gbxFilEnvAttack.setObjectName(u"gbxFilEnvAttack")
        self.gbxFilEnvAttack.setAlignment(Qt.AlignCenter)
        self.layFilEnvAttack = QVBoxLayout(self.gbxFilEnvAttack)
        self.layFilEnvAttack.setObjectName(u"layFilEnvAttack")
        self.layFilEnvAttack.setSizeConstraint(QLayout.SetNoConstraint)
        self.layFilEnvAttack.setContentsMargins(6, 6, 6, 6)
        self.knbFilEnvAttack = QDial(self.gbxFilEnvAttack)
        self.knbFilEnvAttack.setObjectName(u"knbFilEnvAttack")
        self.knbFilEnvAttack.setMinimumSize(QSize(0, 48))
        self.knbFilEnvAttack.setMaximumSize(QSize(16777215, 48))

        self.layFilEnvAttack.addWidget(self.knbFilEnvAttack)

        self.lblFilEnvAttack = QLabel(self.gbxFilEnvAttack)
        self.lblFilEnvAttack.setObjectName(u"lblFilEnvAttack")
        self.lblFilEnvAttack.setAlignment(Qt.AlignCenter)

        self.layFilEnvAttack.addWidget(self.lblFilEnvAttack)

        self.vspFilEnvAttack = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layFilEnvAttack.addItem(self.vspFilEnvAttack)

        self.layFilEnvAttack.setStretch(2, 1)

        self.gridLayout_16.addWidget(self.gbxFilEnvAttack, 0, 2, 1, 1)

        self.gbxFilEnvSustain = QGroupBox(self.gbxFilEnv)
        self.gbxFilEnvSustain.setObjectName(u"gbxFilEnvSustain")
        self.gbxFilEnvSustain.setAlignment(Qt.AlignCenter)
        self.layFilEnvSustain = QVBoxLayout(self.gbxFilEnvSustain)
        self.layFilEnvSustain.setObjectName(u"layFilEnvSustain")
        self.layFilEnvSustain.setSizeConstraint(QLayout.SetNoConstraint)
        self.layFilEnvSustain.setContentsMargins(6, 6, 6, 6)
        self.knbFilEnvSustain = QDial(self.gbxFilEnvSustain)
        self.knbFilEnvSustain.setObjectName(u"knbFilEnvSustain")
        self.knbFilEnvSustain.setMinimumSize(QSize(0, 48))
        self.knbFilEnvSustain.setMaximumSize(QSize(16777215, 48))

        self.layFilEnvSustain.addWidget(self.knbFilEnvSustain)

        self.lblFilEnvSustainVal = QLabel(self.gbxFilEnvSustain)
        self.lblFilEnvSustainVal.setObjectName(u"lblFilEnvSustainVal")
        self.lblFilEnvSustainVal.setAlignment(Qt.AlignCenter)

        self.layFilEnvSustain.addWidget(self.lblFilEnvSustainVal)

        self.vspFilEnvSustain = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layFilEnvSustain.addItem(self.vspFilEnvSustain)

        self.layFilEnvSustain.setStretch(2, 1)

        self.gridLayout_16.addWidget(self.gbxFilEnvSustain, 0, 5, 1, 1)

        self.hspFilEnvR = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_16.addItem(self.hspFilEnvR, 0, 8, 1, 1)


        self.verticalLayout_22.addWidget(self.gbxFilEnv)

        self.tabWidget.addTab(self.tabEnvFilter, "")
        self.tabPitch = QWidget()
        self.tabPitch.setObjectName(u"tabPitch")
        self.layPitch = QGridLayout(self.tabPitch)
        self.layPitch.setObjectName(u"layPitch")
        self.layPitch.setSizeConstraint(QLayout.SetNoConstraint)
        self.layPitch.setContentsMargins(6, 6, 6, 6)
        self.gbxPitch = QGroupBox(self.tabPitch)
        self.gbxPitch.setObjectName(u"gbxPitch")
        self.gbxPitch.setCheckable(True)
        self.layGbxPitch = QGridLayout(self.gbxPitch)
        self.layGbxPitch.setObjectName(u"layGbxPitch")
        self.layGbxPitch.setSizeConstraint(QLayout.SetNoConstraint)
        self.layGbxPitch.setContentsMargins(6, 6, 6, 6)
        self.layPitchKnobs = QGridLayout()
        self.layPitchKnobs.setObjectName(u"layPitchKnobs")
        self.layPitchKnobs.setSizeConstraint(QLayout.SetNoConstraint)
        self.lblPitchRandom = QLabel(self.gbxPitch)
        self.lblPitchRandom.setObjectName(u"lblPitchRandom")
        sizePolicy2.setHeightForWidth(self.lblPitchRandom.sizePolicy().hasHeightForWidth())
        self.lblPitchRandom.setSizePolicy(sizePolicy2)
        self.lblPitchRandom.setAlignment(Qt.AlignCenter)

        self.layPitchKnobs.addWidget(self.lblPitchRandom, 0, 3, 1, 1)

        self.knbPitchRandom = QDial(self.gbxPitch)
        self.knbPitchRandom.setObjectName(u"knbPitchRandom")
        self.knbPitchRandom.setMaximumSize(QSize(16777215, 48))
        self.knbPitchRandom.setNotchesVisible(True)

        self.layPitchKnobs.addWidget(self.knbPitchRandom, 1, 3, 1, 1)

        self.lblPitchKeytrack = QLabel(self.gbxPitch)
        self.lblPitchKeytrack.setObjectName(u"lblPitchKeytrack")
        sizePolicy2.setHeightForWidth(self.lblPitchKeytrack.sizePolicy().hasHeightForWidth())
        self.lblPitchKeytrack.setSizePolicy(sizePolicy2)
        self.lblPitchKeytrack.setAlignment(Qt.AlignCenter)

        self.layPitchKnobs.addWidget(self.lblPitchKeytrack, 0, 1, 1, 1)

        self.lblPitchVeltrackVal = QLabel(self.gbxPitch)
        self.lblPitchVeltrackVal.setObjectName(u"lblPitchVeltrackVal")
        self.lblPitchVeltrackVal.setAlignment(Qt.AlignCenter)

        self.layPitchKnobs.addWidget(self.lblPitchVeltrackVal, 2, 2, 1, 1)

        self.knbPitchVeltrack = QDial(self.gbxPitch)
        self.knbPitchVeltrack.setObjectName(u"knbPitchVeltrack")
        self.knbPitchVeltrack.setMaximumSize(QSize(16777215, 48))
        self.knbPitchVeltrack.setNotchesVisible(True)

        self.layPitchKnobs.addWidget(self.knbPitchVeltrack, 1, 2, 1, 1)

        self.hspPitchL = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layPitchKnobs.addItem(self.hspPitchL, 1, 0, 1, 1)

        self.knbPitchKeytrack = QDial(self.gbxPitch)
        self.knbPitchKeytrack.setObjectName(u"knbPitchKeytrack")
        self.knbPitchKeytrack.setMaximumSize(QSize(16777215, 48))
        self.knbPitchKeytrack.setNotchesVisible(True)

        self.layPitchKnobs.addWidget(self.knbPitchKeytrack, 1, 1, 1, 1)

        self.lblPitchRandomVal = QLabel(self.gbxPitch)
        self.lblPitchRandomVal.setObjectName(u"lblPitchRandomVal")
        self.lblPitchRandomVal.setAlignment(Qt.AlignCenter)

        self.layPitchKnobs.addWidget(self.lblPitchRandomVal, 2, 3, 1, 1)

        self.lblPitchKeytrackVal = QLabel(self.gbxPitch)
        self.lblPitchKeytrackVal.setObjectName(u"lblPitchKeytrackVal")
        self.lblPitchKeytrackVal.setAlignment(Qt.AlignCenter)

        self.layPitchKnobs.addWidget(self.lblPitchKeytrackVal, 2, 1, 1, 1)

        self.lblPitchVeltrack = QLabel(self.gbxPitch)
        self.lblPitchVeltrack.setObjectName(u"lblPitchVeltrack")
        sizePolicy2.setHeightForWidth(self.lblPitchVeltrack.sizePolicy().hasHeightForWidth())
        self.lblPitchVeltrack.setSizePolicy(sizePolicy2)
        self.lblPitchVeltrack.setAlignment(Qt.AlignCenter)

        self.layPitchKnobs.addWidget(self.lblPitchVeltrack, 0, 2, 1, 1)

        self.hspPitchR = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layPitchKnobs.addItem(self.hspPitchR, 1, 4, 1, 1)


        self.layGbxPitch.addLayout(self.layPitchKnobs, 1, 0, 1, 2)


        self.layPitch.addWidget(self.gbxPitch, 0, 0, 1, 1)

        self.gbxPitchLfo = QGroupBox(self.tabPitch)
        self.gbxPitchLfo.setObjectName(u"gbxPitchLfo")
        self.gbxPitchLfo.setCheckable(True)
        self.layGbxPitchLfo = QGridLayout(self.gbxPitchLfo)
        self.layGbxPitchLfo.setObjectName(u"layGbxPitchLfo")
        self.layGbxPitchLfo.setSizeConstraint(QLayout.SetNoConstraint)
        self.layGbxPitchLfo.setContentsMargins(6, 6, 6, 6)
        self.knbPitchDepth = QDial(self.gbxPitchLfo)
        self.knbPitchDepth.setObjectName(u"knbPitchDepth")
        self.knbPitchDepth.setMaximumSize(QSize(16777215, 48))
        self.knbPitchDepth.setNotchesVisible(True)

        self.layGbxPitchLfo.addWidget(self.knbPitchDepth, 1, 3, 1, 1)

        self.lblPitchLfoFadeVal = QLabel(self.gbxPitchLfo)
        self.lblPitchLfoFadeVal.setObjectName(u"lblPitchLfoFadeVal")
        self.lblPitchLfoFadeVal.setAlignment(Qt.AlignCenter)

        self.layGbxPitchLfo.addWidget(self.lblPitchLfoFadeVal, 2, 2, 1, 1)

        self.knbPitchFade = QDial(self.gbxPitchLfo)
        self.knbPitchFade.setObjectName(u"knbPitchFade")
        self.knbPitchFade.setMaximumSize(QSize(16777215, 48))
        self.knbPitchFade.setNotchesVisible(True)

        self.layGbxPitchLfo.addWidget(self.knbPitchFade, 1, 2, 1, 1)

        self.knbPitchFreq = QDial(self.gbxPitchLfo)
        self.knbPitchFreq.setObjectName(u"knbPitchFreq")
        self.knbPitchFreq.setMaximumSize(QSize(16777215, 48))
        self.knbPitchFreq.setNotchesVisible(True)

        self.layGbxPitchLfo.addWidget(self.knbPitchFreq, 1, 4, 1, 1)

        self.lblPitchLfoDepthVal = QLabel(self.gbxPitchLfo)
        self.lblPitchLfoDepthVal.setObjectName(u"lblPitchLfoDepthVal")
        self.lblPitchLfoDepthVal.setAlignment(Qt.AlignCenter)

        self.layGbxPitchLfo.addWidget(self.lblPitchLfoDepthVal, 2, 3, 1, 1)

        self.lblPitchLfoDelayVal = QLabel(self.gbxPitchLfo)
        self.lblPitchLfoDelayVal.setObjectName(u"lblPitchLfoDelayVal")
        self.lblPitchLfoDelayVal.setAlignment(Qt.AlignCenter)

        self.layGbxPitchLfo.addWidget(self.lblPitchLfoDelayVal, 2, 1, 1, 1)

        self.lblPitchLfoDepth = QLabel(self.gbxPitchLfo)
        self.lblPitchLfoDepth.setObjectName(u"lblPitchLfoDepth")
        sizePolicy2.setHeightForWidth(self.lblPitchLfoDepth.sizePolicy().hasHeightForWidth())
        self.lblPitchLfoDepth.setSizePolicy(sizePolicy2)
        self.lblPitchLfoDepth.setAlignment(Qt.AlignCenter)

        self.layGbxPitchLfo.addWidget(self.lblPitchLfoDepth, 0, 3, 1, 1)

        self.lblPitchLfoFreq = QLabel(self.gbxPitchLfo)
        self.lblPitchLfoFreq.setObjectName(u"lblPitchLfoFreq")
        sizePolicy2.setHeightForWidth(self.lblPitchLfoFreq.sizePolicy().hasHeightForWidth())
        self.lblPitchLfoFreq.setSizePolicy(sizePolicy2)
        self.lblPitchLfoFreq.setAlignment(Qt.AlignCenter)

        self.layGbxPitchLfo.addWidget(self.lblPitchLfoFreq, 0, 4, 1, 1)

        self.lblPitchLfoFade = QLabel(self.gbxPitchLfo)
        self.lblPitchLfoFade.setObjectName(u"lblPitchLfoFade")
        sizePolicy2.setHeightForWidth(self.lblPitchLfoFade.sizePolicy().hasHeightForWidth())
        self.lblPitchLfoFade.setSizePolicy(sizePolicy2)
        self.lblPitchLfoFade.setAlignment(Qt.AlignCenter)

        self.layGbxPitchLfo.addWidget(self.lblPitchLfoFade, 0, 2, 1, 1)

        self.lblPitchLfoFreqVal = QLabel(self.gbxPitchLfo)
        self.lblPitchLfoFreqVal.setObjectName(u"lblPitchLfoFreqVal")
        self.lblPitchLfoFreqVal.setAlignment(Qt.AlignCenter)

        self.layGbxPitchLfo.addWidget(self.lblPitchLfoFreqVal, 2, 4, 1, 1)

        self.knbPitchDelay = QDial(self.gbxPitchLfo)
        self.knbPitchDelay.setObjectName(u"knbPitchDelay")
        self.knbPitchDelay.setMaximumSize(QSize(16777215, 48))
        self.knbPitchDelay.setNotchesVisible(True)

        self.layGbxPitchLfo.addWidget(self.knbPitchDelay, 1, 1, 1, 1)

        self.lblPitchLfoDelay = QLabel(self.gbxPitchLfo)
        self.lblPitchLfoDelay.setObjectName(u"lblPitchLfoDelay")
        sizePolicy2.setHeightForWidth(self.lblPitchLfoDelay.sizePolicy().hasHeightForWidth())
        self.lblPitchLfoDelay.setSizePolicy(sizePolicy2)
        self.lblPitchLfoDelay.setAlignment(Qt.AlignCenter)

        self.layGbxPitchLfo.addWidget(self.lblPitchLfoDelay, 0, 1, 1, 1)

        self.hspPitchLfoL = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layGbxPitchLfo.addItem(self.hspPitchLfoL, 1, 0, 1, 1)

        self.hspPitchLfoR = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layGbxPitchLfo.addItem(self.hspPitchLfoR, 1, 5, 1, 1)


        self.layPitch.addWidget(self.gbxPitchLfo, 1, 0, 1, 1)

        self.VspPitch = QSpacerItem(20, 77, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layPitch.addItem(self.VspPitch, 2, 0, 1, 1)

        self.tabWidget.addTab(self.tabPitch, "")
        self.tabPitchEnv = QWidget()
        self.tabPitchEnv.setObjectName(u"tabPitchEnv")
        self.layPitchEnv = QVBoxLayout(self.tabPitchEnv)
        self.layPitchEnv.setObjectName(u"layPitchEnv")
        self.layPitchEnv.setSizeConstraint(QLayout.SetNoConstraint)
        self.layPitchEnv.setContentsMargins(6, 6, 6, 6)
        self.gbxPitchEnv = QGroupBox(self.tabPitchEnv)
        self.gbxPitchEnv.setObjectName(u"gbxPitchEnv")
        self.gbxPitchEnv.setCheckable(True)
        self.layGbxPitchEnv = QGridLayout(self.gbxPitchEnv)
        self.layGbxPitchEnv.setObjectName(u"layGbxPitchEnv")
        self.layGbxPitchEnv.setSizeConstraint(QLayout.SetNoConstraint)
        self.layGbxPitchEnv.setContentsMargins(6, 6, 6, 6)
        self.gbxPitchEnvAttack = QGroupBox(self.gbxPitchEnv)
        self.gbxPitchEnvAttack.setObjectName(u"gbxPitchEnvAttack")
        self.gbxPitchEnvAttack.setAlignment(Qt.AlignCenter)
        self.layPitchEnvAttack = QVBoxLayout(self.gbxPitchEnvAttack)
        self.layPitchEnvAttack.setObjectName(u"layPitchEnvAttack")
        self.layPitchEnvAttack.setSizeConstraint(QLayout.SetNoConstraint)
        self.layPitchEnvAttack.setContentsMargins(6, 6, 6, 6)
        self.knbPitchEnvAttack = QDial(self.gbxPitchEnvAttack)
        self.knbPitchEnvAttack.setObjectName(u"knbPitchEnvAttack")
        self.knbPitchEnvAttack.setMinimumSize(QSize(0, 48))
        self.knbPitchEnvAttack.setMaximumSize(QSize(16777215, 48))

        self.layPitchEnvAttack.addWidget(self.knbPitchEnvAttack)

        self.lblPitchEnvAttackVal = QLabel(self.gbxPitchEnvAttack)
        self.lblPitchEnvAttackVal.setObjectName(u"lblPitchEnvAttackVal")
        self.lblPitchEnvAttackVal.setAlignment(Qt.AlignCenter)

        self.layPitchEnvAttack.addWidget(self.lblPitchEnvAttackVal)

        self.vspPitchEnvAttack = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layPitchEnvAttack.addItem(self.vspPitchEnvAttack)

        self.layPitchEnvAttack.setStretch(2, 1)

        self.layGbxPitchEnv.addWidget(self.gbxPitchEnvAttack, 0, 2, 1, 1)

        self.gbxPitchEnvHold = QGroupBox(self.gbxPitchEnv)
        self.gbxPitchEnvHold.setObjectName(u"gbxPitchEnvHold")
        self.gbxPitchEnvHold.setAlignment(Qt.AlignCenter)
        self.layPitchEnvHold = QVBoxLayout(self.gbxPitchEnvHold)
        self.layPitchEnvHold.setObjectName(u"layPitchEnvHold")
        self.layPitchEnvHold.setSizeConstraint(QLayout.SetNoConstraint)
        self.layPitchEnvHold.setContentsMargins(6, 6, 6, 6)
        self.knbPitchEnvHold = QDial(self.gbxPitchEnvHold)
        self.knbPitchEnvHold.setObjectName(u"knbPitchEnvHold")
        self.knbPitchEnvHold.setMinimumSize(QSize(0, 48))
        self.knbPitchEnvHold.setMaximumSize(QSize(16777215, 48))

        self.layPitchEnvHold.addWidget(self.knbPitchEnvHold)

        self.lblPitchEnvHoldVal = QLabel(self.gbxPitchEnvHold)
        self.lblPitchEnvHoldVal.setObjectName(u"lblPitchEnvHoldVal")
        self.lblPitchEnvHoldVal.setAlignment(Qt.AlignCenter)

        self.layPitchEnvHold.addWidget(self.lblPitchEnvHoldVal)

        self.vspPitchEnvHold = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layPitchEnvHold.addItem(self.vspPitchEnvHold)

        self.layPitchEnvHold.setStretch(2, 1)

        self.layGbxPitchEnv.addWidget(self.gbxPitchEnvHold, 0, 3, 1, 1)

        self.gbxPitchEnvDecay = QGroupBox(self.gbxPitchEnv)
        self.gbxPitchEnvDecay.setObjectName(u"gbxPitchEnvDecay")
        self.gbxPitchEnvDecay.setAlignment(Qt.AlignCenter)
        self.layPitchEnvDecay = QVBoxLayout(self.gbxPitchEnvDecay)
        self.layPitchEnvDecay.setObjectName(u"layPitchEnvDecay")
        self.layPitchEnvDecay.setSizeConstraint(QLayout.SetNoConstraint)
        self.layPitchEnvDecay.setContentsMargins(6, 6, 6, 6)
        self.knbPitchEnvDecay = QDial(self.gbxPitchEnvDecay)
        self.knbPitchEnvDecay.setObjectName(u"knbPitchEnvDecay")
        self.knbPitchEnvDecay.setMinimumSize(QSize(0, 48))
        self.knbPitchEnvDecay.setMaximumSize(QSize(16777215, 48))

        self.layPitchEnvDecay.addWidget(self.knbPitchEnvDecay)

        self.lblPitchEnvDecayVal = QLabel(self.gbxPitchEnvDecay)
        self.lblPitchEnvDecayVal.setObjectName(u"lblPitchEnvDecayVal")
        self.lblPitchEnvDecayVal.setAlignment(Qt.AlignCenter)

        self.layPitchEnvDecay.addWidget(self.lblPitchEnvDecayVal)

        self.vspPitchEnvDecay = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layPitchEnvDecay.addItem(self.vspPitchEnvDecay)

        self.layPitchEnvDecay.setStretch(2, 1)

        self.layGbxPitchEnv.addWidget(self.gbxPitchEnvDecay, 0, 4, 1, 1)

        self.hspPitchEnvL = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layGbxPitchEnv.addItem(self.hspPitchEnvL, 0, 0, 1, 1)

        self.gbxPitchEnvSustain = QGroupBox(self.gbxPitchEnv)
        self.gbxPitchEnvSustain.setObjectName(u"gbxPitchEnvSustain")
        self.gbxPitchEnvSustain.setAlignment(Qt.AlignCenter)
        self.layPitchEnvSustain = QVBoxLayout(self.gbxPitchEnvSustain)
        self.layPitchEnvSustain.setObjectName(u"layPitchEnvSustain")
        self.layPitchEnvSustain.setSizeConstraint(QLayout.SetNoConstraint)
        self.layPitchEnvSustain.setContentsMargins(6, 6, 6, 6)
        self.knbPitchEnvSustain = QDial(self.gbxPitchEnvSustain)
        self.knbPitchEnvSustain.setObjectName(u"knbPitchEnvSustain")
        self.knbPitchEnvSustain.setMinimumSize(QSize(0, 48))
        self.knbPitchEnvSustain.setMaximumSize(QSize(16777215, 48))

        self.layPitchEnvSustain.addWidget(self.knbPitchEnvSustain)

        self.lblPitchEnvSustain = QLabel(self.gbxPitchEnvSustain)
        self.lblPitchEnvSustain.setObjectName(u"lblPitchEnvSustain")
        self.lblPitchEnvSustain.setAlignment(Qt.AlignCenter)

        self.layPitchEnvSustain.addWidget(self.lblPitchEnvSustain)

        self.vspPitchEnvSustain = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layPitchEnvSustain.addItem(self.vspPitchEnvSustain)

        self.layPitchEnvSustain.setStretch(2, 1)

        self.layGbxPitchEnv.addWidget(self.gbxPitchEnvSustain, 0, 5, 1, 1)

        self.gbxPitchEnvDepth = QGroupBox(self.gbxPitchEnv)
        self.gbxPitchEnvDepth.setObjectName(u"gbxPitchEnvDepth")
        self.gbxPitchEnvDepth.setAlignment(Qt.AlignCenter)
        self.layPitchEnvDepth = QVBoxLayout(self.gbxPitchEnvDepth)
        self.layPitchEnvDepth.setObjectName(u"layPitchEnvDepth")
        self.layPitchEnvDepth.setSizeConstraint(QLayout.SetNoConstraint)
        self.layPitchEnvDepth.setContentsMargins(6, 6, 6, 6)
        self.knbPitchEnvDepth = QDial(self.gbxPitchEnvDepth)
        self.knbPitchEnvDepth.setObjectName(u"knbPitchEnvDepth")
        self.knbPitchEnvDepth.setMinimumSize(QSize(0, 48))
        self.knbPitchEnvDepth.setMaximumSize(QSize(16777215, 48))

        self.layPitchEnvDepth.addWidget(self.knbPitchEnvDepth)

        self.lblPitchEnvDepthVal = QLabel(self.gbxPitchEnvDepth)
        self.lblPitchEnvDepthVal.setObjectName(u"lblPitchEnvDepthVal")
        self.lblPitchEnvDepthVal.setAlignment(Qt.AlignCenter)

        self.layPitchEnvDepth.addWidget(self.lblPitchEnvDepthVal)

        self.lblPitchEnvDepthVel = QLabel(self.gbxPitchEnvDepth)
        self.lblPitchEnvDepthVel.setObjectName(u"lblPitchEnvDepthVel")
        self.lblPitchEnvDepthVel.setAlignment(Qt.AlignCenter)

        self.layPitchEnvDepth.addWidget(self.lblPitchEnvDepthVel)

        self.knbPitchEnvDepthVel = QDial(self.gbxPitchEnvDepth)
        self.knbPitchEnvDepthVel.setObjectName(u"knbPitchEnvDepthVel")
        self.knbPitchEnvDepthVel.setMinimumSize(QSize(0, 48))
        self.knbPitchEnvDepthVel.setMaximumSize(QSize(16777215, 48))

        self.layPitchEnvDepth.addWidget(self.knbPitchEnvDepthVel)

        self.lblPitchEnvDepthVelVal = QLabel(self.gbxPitchEnvDepth)
        self.lblPitchEnvDepthVelVal.setObjectName(u"lblPitchEnvDepthVelVal")
        self.lblPitchEnvDepthVelVal.setAlignment(Qt.AlignCenter)

        self.layPitchEnvDepth.addWidget(self.lblPitchEnvDepthVelVal)

        self.vspPitchEnvDepth = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layPitchEnvDepth.addItem(self.vspPitchEnvDepth)


        self.layGbxPitchEnv.addWidget(self.gbxPitchEnvDepth, 0, 7, 1, 1)

        self.gbxPitchEnvRelease = QGroupBox(self.gbxPitchEnv)
        self.gbxPitchEnvRelease.setObjectName(u"gbxPitchEnvRelease")
        self.gbxPitchEnvRelease.setAlignment(Qt.AlignCenter)
        self.layPitchEnvRelease = QVBoxLayout(self.gbxPitchEnvRelease)
        self.layPitchEnvRelease.setObjectName(u"layPitchEnvRelease")
        self.layPitchEnvRelease.setSizeConstraint(QLayout.SetNoConstraint)
        self.layPitchEnvRelease.setContentsMargins(6, 6, 6, 6)
        self.knbPitchEnvRelease = QDial(self.gbxPitchEnvRelease)
        self.knbPitchEnvRelease.setObjectName(u"knbPitchEnvRelease")
        self.knbPitchEnvRelease.setMinimumSize(QSize(0, 48))
        self.knbPitchEnvRelease.setMaximumSize(QSize(16777215, 48))

        self.layPitchEnvRelease.addWidget(self.knbPitchEnvRelease)

        self.lblPitchEnvReleaseVal = QLabel(self.gbxPitchEnvRelease)
        self.lblPitchEnvReleaseVal.setObjectName(u"lblPitchEnvReleaseVal")
        self.lblPitchEnvReleaseVal.setAlignment(Qt.AlignCenter)

        self.layPitchEnvRelease.addWidget(self.lblPitchEnvReleaseVal)

        self.vspPitchEnvRelease = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layPitchEnvRelease.addItem(self.vspPitchEnvRelease)

        self.layPitchEnvRelease.setStretch(2, 1)

        self.layGbxPitchEnv.addWidget(self.gbxPitchEnvRelease, 0, 6, 1, 1)

        self.gbxPitchEnvDelay = QGroupBox(self.gbxPitchEnv)
        self.gbxPitchEnvDelay.setObjectName(u"gbxPitchEnvDelay")
        self.gbxPitchEnvDelay.setAlignment(Qt.AlignCenter)
        self.layPitchEnvDelay = QVBoxLayout(self.gbxPitchEnvDelay)
        self.layPitchEnvDelay.setObjectName(u"layPitchEnvDelay")
        self.layPitchEnvDelay.setSizeConstraint(QLayout.SetNoConstraint)
        self.layPitchEnvDelay.setContentsMargins(6, 6, 6, 6)
        self.knbPitchEnvDelay = QDial(self.gbxPitchEnvDelay)
        self.knbPitchEnvDelay.setObjectName(u"knbPitchEnvDelay")
        sizePolicy3.setHeightForWidth(self.knbPitchEnvDelay.sizePolicy().hasHeightForWidth())
        self.knbPitchEnvDelay.setSizePolicy(sizePolicy3)
        self.knbPitchEnvDelay.setMinimumSize(QSize(0, 48))
        self.knbPitchEnvDelay.setMaximumSize(QSize(16777215, 48))

        self.layPitchEnvDelay.addWidget(self.knbPitchEnvDelay)

        self.lblPitchEnvDelayVal = QLabel(self.gbxPitchEnvDelay)
        self.lblPitchEnvDelayVal.setObjectName(u"lblPitchEnvDelayVal")
        sizePolicy3.setHeightForWidth(self.lblPitchEnvDelayVal.sizePolicy().hasHeightForWidth())
        self.lblPitchEnvDelayVal.setSizePolicy(sizePolicy3)
        self.lblPitchEnvDelayVal.setAlignment(Qt.AlignCenter)

        self.layPitchEnvDelay.addWidget(self.lblPitchEnvDelayVal)

        self.vspPitchEnvDelay = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layPitchEnvDelay.addItem(self.vspPitchEnvDelay)

        self.layPitchEnvDelay.setStretch(2, 1)

        self.layGbxPitchEnv.addWidget(self.gbxPitchEnvDelay, 0, 1, 1, 1)

        self.hspPitchEnvR = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layGbxPitchEnv.addItem(self.hspPitchEnvR, 0, 8, 1, 1)


        self.layPitchEnv.addWidget(self.gbxPitchEnv)

        self.vspPitchEnv = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layPitchEnv.addItem(self.vspPitchEnv)

        self.tabWidget.addTab(self.tabPitchEnv, "")
        self.tabOpcodes = QWidget()
        self.tabOpcodes.setObjectName(u"tabOpcodes")
        self.layOpcodes = QGridLayout(self.tabOpcodes)
        self.layOpcodes.setObjectName(u"layOpcodes")
        self.layOpcodes.setSizeConstraint(QLayout.SetNoConstraint)
        self.layOpcodes.setContentsMargins(6, 6, 6, 6)
        self.lblOpcodes = QLabel(self.tabOpcodes)
        self.lblOpcodes.setObjectName(u"lblOpcodes")

        self.layOpcodes.addWidget(self.lblOpcodes, 0, 0, 1, 1)

        self.lstOpcodes = QListWidget(self.tabOpcodes)
        self.lstOpcodes.setObjectName(u"lstOpcodes")

        self.layOpcodes.addWidget(self.lstOpcodes, 1, 0, 1, 1)

        self.tabWidget.addTab(self.tabOpcodes, "")
        self.splitter.addWidget(self.tabWidget)

        self.layCentralWidget.addWidget(self.splitter)

        self.layCentralWidget.setStretch(6, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 896, 28))
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actNew)
        self.menuFile.addAction(self.actOpen)
        self.menuFile.addAction(self.actSave)
        self.menuFile.addAction(self.actSaveAs)
        self.menuFile.addAction(self.actRealtimeSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actQuit)

        self.retranslateUi(MainWindow)
        self.actQuit.triggered.connect(MainWindow.close)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        self.actNew.setText(QCoreApplication.translate("MainWindow", u"&New project...", None))
#if QT_CONFIG(shortcut)
        self.actNew.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.actOpen.setText(QCoreApplication.translate("MainWindow", u"&Open...", None))
#if QT_CONFIG(shortcut)
        self.actOpen.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actSave.setText(QCoreApplication.translate("MainWindow", u"&Save", None))
#if QT_CONFIG(shortcut)
        self.actSave.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actSaveAs.setText(QCoreApplication.translate("MainWindow", u"&Save as...", None))
#if QT_CONFIG(shortcut)
        self.actSaveAs.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+A", None))
#endif // QT_CONFIG(shortcut)
        self.actQuit.setText(QCoreApplication.translate("MainWindow", u"&Quit", None))
#if QT_CONFIG(shortcut)
        self.actQuit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.actRealtimeSave.setText(QCoreApplication.translate("MainWindow", u"Realtime Save", None))
        self.pbnMainFolder.setText(QCoreApplication.translate("MainWindow", u"Main Folder", None))
        self.lblPreset.setText(QCoreApplication.translate("MainWindow", u"PRESET:", None))
        self.lblPresetPrefix.setText(QCoreApplication.translate("MainWindow", u"NONE/", None))
        self.lblSfzExt.setText(QCoreApplication.translate("MainWindow", u".sfz", None))
        self.gbxGlobal.setTitle(QCoreApplication.translate("MainWindow", u"Global", None))
        self.chkKeyswitch.setText(QCoreApplication.translate("MainWindow", u"Keyswitch", None))
        self.lblKeyswitchRange.setText(QCoreApplication.translate("MainWindow", u"Range:", None))
        self.lblKeyswitchDefault.setText(QCoreApplication.translate("MainWindow", u"Default:", None))
        self.lblKey.setText(QCoreApplication.translate("MainWindow", u"Key:", None))
        self.lblVel.setText(QCoreApplication.translate("MainWindow", u"Vel:", None))
        self.chkNoteOn.setText(QCoreApplication.translate("MainWindow", u"\"note on\"", None))
        self.lblCc.setText(QCoreApplication.translate("MainWindow", u"CC:", None))
        self.lblPack.setText(QCoreApplication.translate("MainWindow", u"Pack:", None))
        self.lblMap.setText(QCoreApplication.translate("MainWindow", u"Map:", None))
        self.chkPercussion.setText(QCoreApplication.translate("MainWindow", u"Percussion", None))
        self.chkRandom.setText(QCoreApplication.translate("MainWindow", u"Random:", None))
        self.lblRandomLo.setText(QCoreApplication.translate("MainWindow", u"lo:", None))
        self.lblRandomHi.setText(QCoreApplication.translate("MainWindow", u"hi:", None))
        self.lblVolume.setText(QCoreApplication.translate("MainWindow", u"Vol (dB):", None))
        self.lblOutput.setText(QCoreApplication.translate("MainWindow", u"Output:", None))
        self.gbxPolyphony.setTitle(QCoreApplication.translate("MainWindow", u"Polyphony", None))
        self.chkPolyphony.setText(QCoreApplication.translate("MainWindow", u"Polyphony:", None))
        self.chkNoteSelfmask.setText(QCoreApplication.translate("MainWindow", u"Note Selfmask", None))
        self.chkNotePolyphony.setText(QCoreApplication.translate("MainWindow", u"Note Polyphony:", None))
        self.gbxTrigger.setTitle(QCoreApplication.translate("MainWindow", u"Trigger", None))
        self.chkRtDecay.setText(QCoreApplication.translate("MainWindow", u"rt_decay (dB):", None))
        self.chkRtDead.setText(QCoreApplication.translate("MainWindow", u"rt_dead", None))
        self.cbxRtDeadMode.setItemText(0, QCoreApplication.translate("MainWindow", u"attack", None))
        self.cbxRtDeadMode.setItemText(1, QCoreApplication.translate("MainWindow", u"release", None))
        self.cbxRtDeadMode.setItemText(2, QCoreApplication.translate("MainWindow", u"first", None))
        self.cbxRtDeadMode.setItemText(3, QCoreApplication.translate("MainWindow", u"legato", None))
        self.cbxRtDeadMode.setItemText(4, QCoreApplication.translate("MainWindow", u"release_key", None))

        self.lblTriggerMode.setText(QCoreApplication.translate("MainWindow", u"Mode:", None))
        self.gbxKeyswitch.setTitle(QCoreApplication.translate("MainWindow", u"Keyswitch", None))
        self.lblKeyswitchLabel.setText(QCoreApplication.translate("MainWindow", u"Label:", None))
        self.chkKeySwitchCount.setText(QCoreApplication.translate("MainWindow", u"Number:", None))
        self.gbxMapKey.setTitle(QCoreApplication.translate("MainWindow", u"Key", None))
        self.chkUseGlobalPitchKeycenter.setText(QCoreApplication.translate("MainWindow", u"Global `pitch_keycenter`", None))
        self.chkUseKey.setText(QCoreApplication.translate("MainWindow", u"Use `key` opcode instead", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMap), QCoreApplication.translate("MainWindow", u"Map", None))
        self.gbxSampleOffset.setTitle(QCoreApplication.translate("MainWindow", u"Offset", None))
        self.lblSampleOffsetRandom.setText(QCoreApplication.translate("MainWindow", u"Random:", None))
        self.lblSampleOffsetVelocity.setText(QCoreApplication.translate("MainWindow", u"Velocity:", None))
        self.gbxSampleGeneral.setTitle(QCoreApplication.translate("MainWindow", u"General", None))
        self.cbxDirection.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))
        self.cbxDirection.setItemText(1, QCoreApplication.translate("MainWindow", u"forward", None))
        self.cbxDirection.setItemText(2, QCoreApplication.translate("MainWindow", u"reverse", None))

        self.lblSampleQuality.setText(QCoreApplication.translate("MainWindow", u"Quality (interpolation):", None))
        self.lblLoopMode.setText(QCoreApplication.translate("MainWindow", u"Loop Mode:", None))
        self.lblSampleMapDelay.setText(QCoreApplication.translate("MainWindow", u"Map Delay (sec):", None))
        self.lblDirection.setText(QCoreApplication.translate("MainWindow", u"Direction:", None))
        self.cbxLoopMode.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))
        self.cbxLoopMode.setItemText(1, QCoreApplication.translate("MainWindow", u"no_loop", None))
        self.cbxLoopMode.setItemText(2, QCoreApplication.translate("MainWindow", u"one_shot", None))
        self.cbxLoopMode.setItemText(3, QCoreApplication.translate("MainWindow", u"loop_continuous", None))
        self.cbxLoopMode.setItemText(4, QCoreApplication.translate("MainWindow", u"loop_sustain", None))

        self.gbxSampleRegion.setTitle(QCoreApplication.translate("MainWindow", u"Region", None))
        self.cbxOffTime.setItemText(0, QCoreApplication.translate("MainWindow", u"fast", None))
        self.cbxOffTime.setItemText(1, QCoreApplication.translate("MainWindow", u"normal", None))

        self.lblGroup.setText(QCoreApplication.translate("MainWindow", u"Group:", None))
        self.cbxOffMode.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.lblOffTime.setText(QCoreApplication.translate("MainWindow", u"Off time:", None))
        self.lblOffBy.setText(QCoreApplication.translate("MainWindow", u"Off by:", None))
        self.lblOffMode.setText(QCoreApplication.translate("MainWindow", u"Off mode:", None))
        self.chkRegionExclusiveClass.setText(QCoreApplication.translate("MainWindow", u"Exclusive Class", None))
        self.gbxSampleTranspose.setTitle(QCoreApplication.translate("MainWindow", u"Transpose", None))
        self.lblSampleTransposePitch.setText(QCoreApplication.translate("MainWindow", u"Pitch", None))
        self.lblSampleTransposeNote.setText(QCoreApplication.translate("MainWindow", u"Note", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSample), QCoreApplication.translate("MainWindow", u"Sample", None))
        self.gbxPan.setTitle(QCoreApplication.translate("MainWindow", u"Enable", None))
        self.lblPanKeycenter.setText(QCoreApplication.translate("MainWindow", u"Keycenter", None))
        self.lblPanRandom.setText(QCoreApplication.translate("MainWindow", u"Random", None))
        self.lblPanKeytrackVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lblPanVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lblPan.setText(QCoreApplication.translate("MainWindow", u"Pan", None))
        self.lblPanVeltrackVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lblPanRandomVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lblPanKeytrack.setText(QCoreApplication.translate("MainWindow", u"Keytrack", None))
        self.lblPanVeltrack.setText(QCoreApplication.translate("MainWindow", u"Veltrack", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabPan), QCoreApplication.translate("MainWindow", u"Pan", None))
        self.gbxAmpGeneral.setTitle(QCoreApplication.translate("MainWindow", u"General", None))
        self.chkAmpVelFloor.setText(QCoreApplication.translate("MainWindow", u"Velocity floor:", None))
        self.lblAmpKeycenter.setText(QCoreApplication.translate("MainWindow", u"Keycenter:", None))
        self.lblAmpVeltrack.setText(QCoreApplication.translate("MainWindow", u"Veltrack", None))
        self.lblAmpKeytrack.setText(QCoreApplication.translate("MainWindow", u"Keytrack", None))
        self.lblAmpRandomVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lblAmpVeltrackVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lblAmpRandom.setText(QCoreApplication.translate("MainWindow", u"Random", None))
        self.lblAmpKeytrackVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.chkAmpVelAttack.setText(QCoreApplication.translate("MainWindow", u"Velocity -> Env Amp Attack:", None))
        self.gbxAmpLfo.setTitle(QCoreApplication.translate("MainWindow", u"LFO", None))
        self.lblAmpLfoFadeVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lblAmpLfoDepthVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lblAmpLfoDelayVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lblAmpLfoDepth.setText(QCoreApplication.translate("MainWindow", u"Depth", None))
        self.lblAmpLfoFreq.setText(QCoreApplication.translate("MainWindow", u"Freq", None))
        self.lblAmpLfoFade.setText(QCoreApplication.translate("MainWindow", u"Fade", None))
        self.lblAmpLfoFreqVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lblAmpLfoDelay.setText(QCoreApplication.translate("MainWindow", u"Delay", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabAmp), QCoreApplication.translate("MainWindow", u"Amp", None))
        self.gbxAmpEnv.setTitle(QCoreApplication.translate("MainWindow", u"Enable Envelope", None))
        self.gbxAmpEnvHold.setTitle(QCoreApplication.translate("MainWindow", u"Hold", None))
        self.lblAmpEnvHoldVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.gbxAmpEnvDecay.setTitle(QCoreApplication.translate("MainWindow", u"Decay", None))
        self.lblAmpEnvDecayVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.pbnAmpEnvDecayShapeEnable.setText(QCoreApplication.translate("MainWindow", u"Enable", None))
        self.lblAmpEnvDecayShape.setText(QCoreApplication.translate("MainWindow", u"Shape", None))
        self.lblAmpEnvDecayShapeVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.pbnAmpEnvDecayShapeReset.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.gbxAmpEnvDelay.setTitle(QCoreApplication.translate("MainWindow", u"Delay", None))
        self.lblAmpEnvDelayVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.gbxAmpEnvAttack.setTitle(QCoreApplication.translate("MainWindow", u"Attack", None))
        self.lblAmpEnvAttackVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.pbnAmpEnvAttackShapeEnable.setText(QCoreApplication.translate("MainWindow", u"Enable", None))
        self.lblAmpEnvAttackShape.setText(QCoreApplication.translate("MainWindow", u"Shape", None))
        self.lblAmpEnvAttackShapeVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.pbnAmpEnvAttackShapeReset.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.gbxAmpEnvSustain.setTitle(QCoreApplication.translate("MainWindow", u"Sustain", None))
        self.lblAmpEnvSustainVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.gbxAmpEnvRelease.setTitle(QCoreApplication.translate("MainWindow", u"Release", None))
        self.lblAmpEnvReleaseVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabAmpEnv), QCoreApplication.translate("MainWindow", u"Amp Env", None))
        self.gbxFilterGeneral.setTitle(QCoreApplication.translate("MainWindow", u"General", None))
        self.lblFilterType.setText(QCoreApplication.translate("MainWindow", u"Type:", None))
        self.cbxFilterType.setItemText(0, QCoreApplication.translate("MainWindow", u"lpf_1p", None))
        self.cbxFilterType.setItemText(1, QCoreApplication.translate("MainWindow", u"hpf_1p", None))
        self.cbxFilterType.setItemText(2, QCoreApplication.translate("MainWindow", u"lpf_2p", None))
        self.cbxFilterType.setItemText(3, QCoreApplication.translate("MainWindow", u"hpf_2p", None))
        self.cbxFilterType.setItemText(4, QCoreApplication.translate("MainWindow", u"bpf_2p", None))
        self.cbxFilterType.setItemText(5, QCoreApplication.translate("MainWindow", u"brf_2p", None))

        self.lblFilterKeycenter.setText(QCoreApplication.translate("MainWindow", u"Keycenter:", None))
        self.lblFilterRandomVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lblFilterVeltrackVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lblFilterCutoff.setText(QCoreApplication.translate("MainWindow", u"Cutoff", None))
        self.lblFilterResonanceVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lblFilterCutoffVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lblFilterVeltrack.setText(QCoreApplication.translate("MainWindow", u"Veltrack", None))
        self.lblFilterRandom.setText(QCoreApplication.translate("MainWindow", u"Random", None))
        self.lblFilterKeytrack.setText(QCoreApplication.translate("MainWindow", u"Keytrack", None))
        self.lblFilterKeytrackVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lblFilterResonance.setText(QCoreApplication.translate("MainWindow", u"Resonance", None))
        self.gbxFilterLfo.setTitle(QCoreApplication.translate("MainWindow", u"LFO", None))
        self.lblFilterLfoFadeVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lblFilterLfoDepthVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lblFilterLfoDelayVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lblFilterLfoDepth.setText(QCoreApplication.translate("MainWindow", u"Depth", None))
        self.lblFilterLfoFreq.setText(QCoreApplication.translate("MainWindow", u"Freq", None))
        self.lblFilterLfoFade.setText(QCoreApplication.translate("MainWindow", u"Fade", None))
        self.lblFilterLfoFreqVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lblFilterLfoDelay.setText(QCoreApplication.translate("MainWindow", u"Delay", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabFilter), QCoreApplication.translate("MainWindow", u"Filter", None))
        self.gbxFilEnv.setTitle(QCoreApplication.translate("MainWindow", u"Enable Envelope", None))
        self.gbxFilEnvDecay.setTitle(QCoreApplication.translate("MainWindow", u"Decay", None))
        self.lblFilEnvDecayVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.gbxFilEnvDepth.setTitle(QCoreApplication.translate("MainWindow", u"Depth (cents)", None))
        self.lblFilEnvDepthVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.gbxFilEnvDelay.setTitle(QCoreApplication.translate("MainWindow", u"Delay", None))
        self.lblFilEnvDelayVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.gbxFilEnvHold.setTitle(QCoreApplication.translate("MainWindow", u"Hold", None))
        self.lblFilEnvHoldVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.gbxFilEnvRelease.setTitle(QCoreApplication.translate("MainWindow", u"Release", None))
        self.lblFilEnvReleaseVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.gbxFilEnvAttack.setTitle(QCoreApplication.translate("MainWindow", u"Attack", None))
        self.lblFilEnvAttack.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.gbxFilEnvSustain.setTitle(QCoreApplication.translate("MainWindow", u"Sustain", None))
        self.lblFilEnvSustainVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabEnvFilter), QCoreApplication.translate("MainWindow", u"Filter Env", None))
        self.gbxPitch.setTitle(QCoreApplication.translate("MainWindow", u"Pitch", None))
        self.lblPitchRandom.setText(QCoreApplication.translate("MainWindow", u"Random", None))
        self.lblPitchKeytrack.setText(QCoreApplication.translate("MainWindow", u"Keytrack", None))
        self.lblPitchVeltrackVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lblPitchRandomVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lblPitchKeytrackVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lblPitchVeltrack.setText(QCoreApplication.translate("MainWindow", u"Veltrack", None))
        self.gbxPitchLfo.setTitle(QCoreApplication.translate("MainWindow", u"LFO", None))
        self.lblPitchLfoFadeVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lblPitchLfoDepthVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lblPitchLfoDelayVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lblPitchLfoDepth.setText(QCoreApplication.translate("MainWindow", u"Depth", None))
        self.lblPitchLfoFreq.setText(QCoreApplication.translate("MainWindow", u"Freq", None))
        self.lblPitchLfoFade.setText(QCoreApplication.translate("MainWindow", u"Fade", None))
        self.lblPitchLfoFreqVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lblPitchLfoDelay.setText(QCoreApplication.translate("MainWindow", u"Delay", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabPitch), QCoreApplication.translate("MainWindow", u"Pitch", None))
        self.gbxPitchEnv.setTitle(QCoreApplication.translate("MainWindow", u"Enable Envelope", None))
        self.gbxPitchEnvAttack.setTitle(QCoreApplication.translate("MainWindow", u"Attack", None))
        self.lblPitchEnvAttackVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.gbxPitchEnvHold.setTitle(QCoreApplication.translate("MainWindow", u"Hold", None))
        self.lblPitchEnvHoldVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.gbxPitchEnvDecay.setTitle(QCoreApplication.translate("MainWindow", u"Decay", None))
        self.lblPitchEnvDecayVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.gbxPitchEnvSustain.setTitle(QCoreApplication.translate("MainWindow", u"Sustain", None))
        self.lblPitchEnvSustain.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.gbxPitchEnvDepth.setTitle(QCoreApplication.translate("MainWindow", u"Depth (cents)", None))
        self.lblPitchEnvDepthVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lblPitchEnvDepthVel.setText(QCoreApplication.translate("MainWindow", u"Velocity", None))
        self.lblPitchEnvDepthVelVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.gbxPitchEnvRelease.setTitle(QCoreApplication.translate("MainWindow", u"Release", None))
        self.lblPitchEnvReleaseVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.gbxPitchEnvDelay.setTitle(QCoreApplication.translate("MainWindow", u"Delay", None))
        self.lblPitchEnvDelayVal.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabPitchEnv), QCoreApplication.translate("MainWindow", u"Pitch Env", None))
        self.lblOpcodes.setText(QCoreApplication.translate("MainWindow", u"Additional Opcodes", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabOpcodes), QCoreApplication.translate("MainWindow", u"Opcodes", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
        pass
    # retranslateUi

