# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\Python\CompilerDeck\resources\widget\DeckHomeWidget\DeckHomeWidget.ui'
#
# Created: Sun Oct 27 19:13:24 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class PySideUiFileSetup(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(538, 449)
        Form.horizontalLayout_3 = QtGui.QHBoxLayout(Form)
        Form.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtGui.QSpacerItem(141, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Form.horizontalLayout_3.addItem(spacerItem)
        Form.widget_2 = QtGui.QWidget(Form)
        Form.widget_2.setObjectName("widget_2")
        Form.verticalLayout = QtGui.QVBoxLayout(Form.widget_2)
        Form.verticalLayout.setContentsMargins(0, 0, 0, 0)
        Form.verticalLayout.setObjectName("verticalLayout")
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        Form.verticalLayout.addItem(spacerItem1)
        Form.widget = QtGui.QWidget(Form.widget_2)
        Form.widget.setObjectName("widget")
        Form.horizontalLayout = QtGui.QHBoxLayout(Form.widget)
        Form.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        Form.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        Form.horizontalLayout.setObjectName("horizontalLayout")
        Form.pathLine = QtGui.QLineEdit(Form.widget)
        Form.pathLine.setObjectName("pathLine")
        Form.horizontalLayout.addWidget(Form.pathLine)
        Form.browseBtn = QtGui.QToolButton(Form.widget)
        Form.browseBtn.setObjectName("browseBtn")
        Form.horizontalLayout.addWidget(Form.browseBtn)
        Form.verticalLayout.addWidget(Form.widget)
        Form.horizontalWidget = QtGui.QWidget(Form.widget_2)
        Form.horizontalWidget.setObjectName("horizontalWidget")
        Form.horizontalLayout_2 = QtGui.QHBoxLayout(Form.horizontalWidget)
        Form.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        Form.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        Form.horizontalLayout_2.setObjectName("horizontalLayout_2")
        Form.settingsBtn = QtGui.QPushButton(Form.horizontalWidget)
        Form.settingsBtn.setObjectName("settingsBtn")
        Form.horizontalLayout_2.addWidget(Form.settingsBtn)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Form.horizontalLayout_2.addItem(spacerItem2)
        Form.openBtn = QtGui.QPushButton(Form.horizontalWidget)
        Form.openBtn.setObjectName("openBtn")
        Form.horizontalLayout_2.addWidget(Form.openBtn)
        Form.verticalLayout.addWidget(Form.horizontalWidget)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        Form.verticalLayout.addItem(spacerItem3)
        Form.horizontalLayout_3.addWidget(Form.widget_2)
        spacerItem4 = QtGui.QSpacerItem(141, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Form.horizontalLayout_3.addItem(spacerItem4)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        Form.browseBtn.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        Form.settingsBtn.setText(QtGui.QApplication.translate("Form", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        Form.openBtn.setText(QtGui.QApplication.translate("Form", "Open", None, QtGui.QApplication.UnicodeUTF8))

