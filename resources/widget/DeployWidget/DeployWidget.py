# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/scott/Python/CompilerDeck/resources/widget/DeployWidget/DeployWidget.ui'
#
# Created: Mon Oct 27 09:01:01 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class PySideUiFileSetup(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(686, 363)
        Form.verticalLayout_2 = QtGui.QVBoxLayout(Form)
        Form.verticalLayout_2.setObjectName("verticalLayout_2")
        Form.label_2 = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(24)
        Form.label_2.setFont(font)
        Form.label_2.setObjectName("label_2")
        Form.verticalLayout_2.addWidget(Form.label_2)
        Form.widget_3 = QtGui.QWidget(Form)
        Form.widget_3.setObjectName("widget_3")
        Form.verticalLayout = QtGui.QVBoxLayout(Form.widget_3)
        Form.verticalLayout.setContentsMargins(0, 0, 0, 0)
        Form.verticalLayout.setObjectName("verticalLayout")
        Form.label = QtGui.QLabel(Form.widget_3)
        Form.label.setObjectName("label")
        Form.verticalLayout.addWidget(Form.label)
        Form.messageText = QtGui.QPlainTextEdit(Form.widget_3)
        Form.messageText.setObjectName("messageText")
        Form.verticalLayout.addWidget(Form.messageText)
        Form.verticalLayout_2.addWidget(Form.widget_3)
        Form.widget_2 = QtGui.QWidget(Form)
        Form.widget_2.setObjectName("widget_2")
        Form.horizontalLayout_2 = QtGui.QHBoxLayout(Form.widget_2)
        Form.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        Form.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtGui.QSpacerItem(536, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Form.horizontalLayout_2.addItem(spacerItem)
        Form.emailCheck = QtGui.QCheckBox(Form.widget_2)
        Form.emailCheck.setObjectName("emailCheck")
        Form.horizontalLayout_2.addWidget(Form.emailCheck)
        Form.verticalLayout_2.addWidget(Form.widget_2)
        Form.widget = QtGui.QWidget(Form)
        Form.widget.setObjectName("widget")
        Form.horizontalLayout = QtGui.QHBoxLayout(Form.widget)
        Form.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        Form.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtGui.QSpacerItem(467, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Form.horizontalLayout.addItem(spacerItem1)
        Form.deployBtn = QtGui.QPushButton(Form.widget)
        Form.deployBtn.setObjectName("deployBtn")
        Form.horizontalLayout.addWidget(Form.deployBtn)
        Form.cancelBtn = QtGui.QPushButton(Form.widget)
        Form.cancelBtn.setObjectName("cancelBtn")
        Form.horizontalLayout.addWidget(Form.cancelBtn)
        Form.verticalLayout_2.addWidget(Form.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        Form.label_2.setText(QtGui.QApplication.translate("Form", "Deploy Build", None, QtGui.QApplication.UnicodeUTF8))
        Form.label.setText(QtGui.QApplication.translate("Form", "Build Message:", None, QtGui.QApplication.UnicodeUTF8))
        Form.emailCheck.setText(QtGui.QApplication.translate("Form", "Send Emails", None, QtGui.QApplication.UnicodeUTF8))
        Form.deployBtn.setText(QtGui.QApplication.translate("Form", "Deploy", None, QtGui.QApplication.UnicodeUTF8))
        Form.cancelBtn.setText(QtGui.QApplication.translate("Form", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

