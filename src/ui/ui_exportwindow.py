# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'exportwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QGridLayout,
    QLabel, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(381, 391)
        self.gridLayout_2 = QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 2)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.listImportMap = QListWidget(Dialog)
        self.listImportMap.setObjectName(u"listImportMap")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listImportMap.sizePolicy().hasHeightForWidth())
        self.listImportMap.setSizePolicy(sizePolicy)
        self.listImportMap.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.gridLayout.addWidget(self.listImportMap, 1, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 2)

        self.pbnImportCancel = QPushButton(Dialog)
        self.pbnImportCancel.setObjectName(u"pbnImportCancel")

        self.gridLayout_2.addWidget(self.pbnImportCancel, 2, 0, 1, 1)

        self.pbnImportAccept = QPushButton(Dialog)
        self.pbnImportAccept.setObjectName(u"pbnImportAccept")

        self.gridLayout_2.addWidget(self.pbnImportAccept, 2, 1, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Export presets", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Select the preset folder to export", None))
        self.pbnImportCancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.pbnImportAccept.setText(QCoreApplication.translate("Dialog", u"Export", None))
    # retranslateUi

