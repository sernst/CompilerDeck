# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\scott\Documents\GitHub\CompilerDeck\resources\widget\LocalSettingsWidget\LocalSettingsWidget.ui'
#
# Created: Wed May 07 12:20:54 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class PySideUiFileSetup(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(749, 212)
        Form.setMinimumSize(QtCore.QSize(749, 212))
        Form.verticalLayout_4 = QtGui.QVBoxLayout(Form)
        Form.verticalLayout_4.setObjectName("verticalLayout_4")
        Form.widget_2 = QtGui.QWidget(Form)
        Form.widget_2.setObjectName("widget_2")
        Form.horizontalLayout = QtGui.QHBoxLayout(Form.widget_2)
        Form.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        Form.horizontalLayout.setObjectName("horizontalLayout")
        Form.verticalLayout_2 = QtGui.QVBoxLayout()
        Form.verticalLayout_2.setObjectName("verticalLayout_2")
        Form.label_2 = QtGui.QLabel(Form.widget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        Form.label_2.setFont(font)
        Form.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        Form.label_2.setObjectName("label_2")
        Form.verticalLayout_2.addWidget(Form.label_2)
        Form.label = QtGui.QLabel(Form.widget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        Form.label.setFont(font)
        Form.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        Form.label.setObjectName("label")
        Form.verticalLayout_2.addWidget(Form.label)
        Form.label_3 = QtGui.QLabel(Form.widget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        Form.label_3.setFont(font)
        Form.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        Form.label_3.setObjectName("label_3")
        Form.verticalLayout_2.addWidget(Form.label_3)
        Form.label_5 = QtGui.QLabel(Form.widget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        Form.label_5.setFont(font)
        Form.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        Form.label_5.setObjectName("label_5")
        Form.verticalLayout_2.addWidget(Form.label_5)
        Form.horizontalLayout.addLayout(Form.verticalLayout_2)
        Form.verticalLayout = QtGui.QVBoxLayout()
        Form.verticalLayout.setObjectName("verticalLayout")
        Form.airLineEdit = QtGui.QLineEdit(Form.widget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        Form.airLineEdit.setFont(font)
        Form.airLineEdit.setObjectName("airLineEdit")
        Form.verticalLayout.addWidget(Form.airLineEdit)
        Form.flexLineEdit = QtGui.QLineEdit(Form.widget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        Form.flexLineEdit.setFont(font)
        Form.flexLineEdit.setObjectName("flexLineEdit")
        Form.verticalLayout.addWidget(Form.flexLineEdit)
        Form.androidLineEdit = QtGui.QLineEdit(Form.widget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        Form.androidLineEdit.setFont(font)
        Form.androidLineEdit.setObjectName("androidLineEdit")
        Form.verticalLayout.addWidget(Form.androidLineEdit)
        Form.antLineEdit = QtGui.QLineEdit(Form.widget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        Form.antLineEdit.setFont(font)
        Form.antLineEdit.setObjectName("antLineEdit")
        Form.verticalLayout.addWidget(Form.antLineEdit)
        Form.horizontalLayout.addLayout(Form.verticalLayout)
        Form.verticalLayout_3 = QtGui.QVBoxLayout()
        Form.verticalLayout_3.setObjectName("verticalLayout_3")
        Form.airToolBtn = QtGui.QToolButton(Form.widget_2)
        Form.airToolBtn.setObjectName("airToolBtn")
        Form.verticalLayout_3.addWidget(Form.airToolBtn)
        Form.flexToolBtn = QtGui.QToolButton(Form.widget_2)
        Form.flexToolBtn.setObjectName("flexToolBtn")
        Form.verticalLayout_3.addWidget(Form.flexToolBtn)
        Form.androidToolBtn = QtGui.QToolButton(Form.widget_2)
        Form.androidToolBtn.setObjectName("androidToolBtn")
        Form.verticalLayout_3.addWidget(Form.androidToolBtn)
        Form.antToolBtn = QtGui.QToolButton(Form.widget_2)
        Form.antToolBtn.setObjectName("antToolBtn")
        Form.verticalLayout_3.addWidget(Form.antToolBtn)
        Form.horizontalLayout.addLayout(Form.verticalLayout_3)
        Form.verticalLayout_4.addWidget(Form.widget_2)
        spacerItem = QtGui.QSpacerItem(20, 12, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        Form.verticalLayout_4.addItem(spacerItem)
        Form.widget = QtGui.QWidget(Form)
        Form.widget.setObjectName("widget")
        Form.horizontalLayout_2 = QtGui.QHBoxLayout(Form.widget)
        Form.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        Form.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtGui.QSpacerItem(546, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Form.horizontalLayout_2.addItem(spacerItem1)
        Form.saveBtn = QtGui.QPushButton(Form.widget)
        Form.saveBtn.setObjectName("saveBtn")
        Form.horizontalLayout_2.addWidget(Form.saveBtn)
        Form.cancelBtn = QtGui.QPushButton(Form.widget)
        Form.cancelBtn.setObjectName("cancelBtn")
        Form.horizontalLayout_2.addWidget(Form.cancelBtn)
        Form.verticalLayout_4.addWidget(Form.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        Form.label_2.setText(QtGui.QApplication.translate("Form", "AIR Root Path:", None, QtGui.QApplication.UnicodeUTF8))
        Form.label.setText(QtGui.QApplication.translate("Form", "Flex SDK Path:", None, QtGui.QApplication.UnicodeUTF8))
        Form.label_3.setText(QtGui.QApplication.translate("Form", "Android SDK Path:", None, QtGui.QApplication.UnicodeUTF8))
        Form.label_5.setText(QtGui.QApplication.translate("Form", "Java Ant Path:", None, QtGui.QApplication.UnicodeUTF8))
        Form.airToolBtn.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        Form.flexToolBtn.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        Form.androidToolBtn.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        Form.antToolBtn.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        Form.saveBtn.setText(QtGui.QApplication.translate("Form", "Save Changes", None, QtGui.QApplication.UnicodeUTF8))
        Form.cancelBtn.setText(QtGui.QApplication.translate("Form", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

