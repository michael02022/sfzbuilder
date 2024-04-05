# Copyright (c) 2024 Andrea Zanellato
# SPDX-License-Identifier: BSD-3-Clause

# This Python file uses the following encoding: utf-8
from PySide6.QtCore    import Qt
from PySide6.QtGui     import QPixmap
from PySide6.QtWidgets import QLabel
from .AyrePy           import KnobPy

def setupKnobs(ui):
  knbPixmap = QPixmap(r":/pan")
  knbPixmap.scaledToWidth(48, Qt.SmoothTransformation)
  ui.knbPan.setPixmap(knbPixmap)
  ui.knbPan.valueChanged.connect(lambda v: ui.dspPan.setValue(float("{:.3f}".format(v))))

  names = [ "Keytrack", "Veltrack", "Random" ]
  for name in names:
    knbPixmap = QPixmap(r":/volume")
    knbPixmap.scaledToWidth(48, Qt.SmoothTransformation)

    knobName   = "knbPan{}".format(name)
    lblValName = "lblPan{}Val".format(name)
    lblVal     = ui.gbxPan.findChild(QLabel, lblValName)
    knob       = ui.gbxPan.findChild(KnobPy, knobName)
    knob.resize(48, 48)
    knob.setPixmap(knbPixmap, 100)
    knob.setValue(0.000);
    knob.valueChanged.connect(lambda v: lblVal.setText("{:.3f}".format(v)))

  names = [ "Keytrack", "Veltrack", "Random" ]
  for name in names:
    knbPixmap = QPixmap(r":/volume")
    knbPixmap.scaledToWidth(48, Qt.SmoothTransformation)

    knobName   = "knbAmp{}".format(name)
    lblValName = "lblAmp{}Val".format(name)
    lblVal     = ui.gbxAmpGeneral.findChild(QLabel, lblValName)
    knob       = ui.gbxAmpGeneral.findChild(KnobPy, knobName)
    knob.resize(48, 48)
    knob.setPixmap(knbPixmap, 100)
    knob.setValue(0.000);
    knob.valueChanged.connect(lambda v: lblVal.setText("{:.3f}".format(v)))

  names = [ "Delay", "Fade", "Depth", "Freq" ]
  for name in names:
    knbPixmap = QPixmap(r":/volume")
    knbPixmap.scaledToWidth(48, Qt.SmoothTransformation)

    knobName   = "knbAmpLfo{}".format(name)
    lblValName = "lblAmpLfo{}Val".format(name)
    lblVal     = ui.gbxAmpLfo.findChild(QLabel, lblValName)
    knob       = ui.gbxAmpLfo.findChild(KnobPy, knobName)
    knob.resize(48, 48)
    knob.setPixmap(knbPixmap, 100)
    knob.setValue(0.000);
    knob.valueChanged.connect(lambda v: lblVal.setText("{:.3f}".format(v)))
