# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\Python\CompilerDeck\resources\widget\DeckCompileWidget\DeckCompileWidget.ui'
#
# Created: Sat Jul 06 14:02:55 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class PySideUiFileSetup(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(640, 480)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(640, 480))
        Form.horizontalLayout_5 = QtGui.QHBoxLayout(Form)
        Form.horizontalLayout_5.setObjectName("horizontalLayout_5")
        Form.mainTab = QtGui.QTabWidget(Form)
        Form.mainTab.setObjectName("mainTab")
        Form.settingsTabPage = QtGui.QWidget()
        Form.settingsTabPage.setObjectName("settingsTabPage")
        Form.verticalLayout_7 = QtGui.QVBoxLayout(Form.settingsTabPage)
        Form.verticalLayout_7.setObjectName("verticalLayout_7")
        Form.widget_4 = QtGui.QWidget(Form.settingsTabPage)
        Form.widget_4.setObjectName("widget_4")
        Form.horizontalLayout_2 = QtGui.QHBoxLayout(Form.widget_4)
        Form.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        Form.horizontalLayout_2.setObjectName("horizontalLayout_2")
        Form.groupBox_3 = QtGui.QGroupBox(Form.widget_4)
        Form.groupBox_3.setObjectName("groupBox_3")
        Form.verticalLayout_6 = QtGui.QVBoxLayout(Form.groupBox_3)
        Form.verticalLayout_6.setObjectName("verticalLayout_6")
        Form.debugCheck = QtGui.QCheckBox(Form.groupBox_3)
        Form.debugCheck.setObjectName("debugCheck")
        Form.verticalLayout_6.addWidget(Form.debugCheck)
        Form.liveCheck = QtGui.QCheckBox(Form.groupBox_3)
        Form.liveCheck.setObjectName("liveCheck")
        Form.verticalLayout_6.addWidget(Form.liveCheck)
        Form.packageAirCheck = QtGui.QCheckBox(Form.groupBox_3)
        Form.packageAirCheck.setObjectName("packageAirCheck")
        Form.verticalLayout_6.addWidget(Form.packageAirCheck)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        Form.verticalLayout_6.addItem(spacerItem)
        Form.horizontalLayout_2.addWidget(Form.groupBox_3)
        Form.platformBox = QtGui.QGroupBox(Form.widget_4)
        Form.platformBox.setObjectName("platformBox")
        Form.verticalLayout_4 = QtGui.QVBoxLayout(Form.platformBox)
        Form.verticalLayout_4.setObjectName("verticalLayout_4")
        Form.webPlatformCheck = QtGui.QCheckBox(Form.platformBox)
        Form.webPlatformCheck.setObjectName("webPlatformCheck")
        Form.verticalLayout_4.addWidget(Form.webPlatformCheck)
        Form.desktopPlatformCheck = QtGui.QCheckBox(Form.platformBox)
        Form.desktopPlatformCheck.setObjectName("desktopPlatformCheck")
        Form.verticalLayout_4.addWidget(Form.desktopPlatformCheck)
        Form.androidPlatformCheck = QtGui.QCheckBox(Form.platformBox)
        Form.androidPlatformCheck.setObjectName("androidPlatformCheck")
        Form.verticalLayout_4.addWidget(Form.androidPlatformCheck)
        Form.iosPlatformCheck = QtGui.QCheckBox(Form.platformBox)
        Form.iosPlatformCheck.setObjectName("iosPlatformCheck")
        Form.verticalLayout_4.addWidget(Form.iosPlatformCheck)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        Form.verticalLayout_4.addItem(spacerItem1)
        Form.horizontalLayout_2.addWidget(Form.platformBox)
        spacerItem2 = QtGui.QSpacerItem(666, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Form.horizontalLayout_2.addItem(spacerItem2)
        Form.verticalLayout_7.addWidget(Form.widget_4)
        Form.widget_2 = QtGui.QWidget(Form.settingsTabPage)
        Form.widget_2.setObjectName("widget_2")
        Form.horizontalLayout = QtGui.QHBoxLayout(Form.widget_2)
        Form.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        Form.horizontalLayout.setObjectName("horizontalLayout")
        Form.widget_5 = QtGui.QWidget(Form.widget_2)
        Form.widget_5.setObjectName("widget_5")
        Form.formLayout = QtGui.QFormLayout(Form.widget_5)
        Form.formLayout.setContentsMargins(0, 0, 0, 0)
        Form.formLayout.setObjectName("formLayout")
        Form.label_3 = QtGui.QLabel(Form.widget_5)
        Form.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        Form.label_3.setObjectName("label_3")
        Form.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, Form.label_3)
        Form.flashPlayerComboBox = QtGui.QComboBox(Form.widget_5)
        Form.flashPlayerComboBox.setObjectName("flashPlayerComboBox")
        Form.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, Form.flashPlayerComboBox)
        Form.label_4 = QtGui.QLabel(Form.widget_5)
        Form.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        Form.label_4.setObjectName("label_4")
        Form.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, Form.label_4)
        Form.airSDKComboBox = QtGui.QComboBox(Form.widget_5)
        Form.airSDKComboBox.setObjectName("airSDKComboBox")
        Form.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, Form.airSDKComboBox)
        Form.horizontalLayout.addWidget(Form.widget_5)
        spacerItem3 = QtGui.QSpacerItem(469, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Form.horizontalLayout.addItem(spacerItem3)
        Form.verticalLayout_7.addWidget(Form.widget_2)
        Form.widget_7 = QtGui.QWidget(Form.settingsTabPage)
        Form.widget_7.setObjectName("widget_7")
        Form.horizontalLayout_4 = QtGui.QHBoxLayout(Form.widget_7)
        Form.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        Form.horizontalLayout_4.setObjectName("horizontalLayout_4")
        Form.widget = QtGui.QWidget(Form.widget_7)
        Form.widget.setObjectName("widget")
        Form.verticalLayout_5 = QtGui.QVBoxLayout(Form.widget)
        Form.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        Form.verticalLayout_5.setObjectName("verticalLayout_5")
        Form.label_5 = QtGui.QLabel(Form.widget)
        Form.label_5.setObjectName("label_5")
        Form.verticalLayout_5.addWidget(Form.label_5)
        Form.remoteDebugComboBox = QtGui.QComboBox(Form.widget)
        Form.remoteDebugComboBox.setObjectName("remoteDebugComboBox")
        Form.verticalLayout_5.addWidget(Form.remoteDebugComboBox)
        Form.horizontalLayout_4.addWidget(Form.widget)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Form.horizontalLayout_4.addItem(spacerItem4)
        Form.verticalLayout_7.addWidget(Form.widget_7)
        spacerItem5 = QtGui.QSpacerItem(20, 140, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        Form.verticalLayout_7.addItem(spacerItem5)
        Form.widget_6 = QtGui.QWidget(Form.settingsTabPage)
        Form.widget_6.setObjectName("widget_6")
        Form.horizontalLayout_3 = QtGui.QHBoxLayout(Form.widget_6)
        Form.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        Form.horizontalLayout_3.setObjectName("horizontalLayout_3")
        Form.compileBtn = QtGui.QPushButton(Form.widget_6)
        font = QtGui.QFont()
        font.setPointSize(10)
        Form.compileBtn.setFont(font)
        Form.compileBtn.setObjectName("compileBtn")
        Form.horizontalLayout_3.addWidget(Form.compileBtn)
        spacerItem6 = QtGui.QSpacerItem(852, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Form.horizontalLayout_3.addItem(spacerItem6)
        Form.verticalLayout_7.addWidget(Form.widget_6)
        Form.mainTab.addTab(Form.settingsTabPage, "")
        Form.deployTabPage = QtGui.QWidget()
        Form.deployTabPage.setObjectName("deployTabPage")
        Form.verticalLayout_12 = QtGui.QVBoxLayout(Form.deployTabPage)
        Form.verticalLayout_12.setObjectName("verticalLayout_12")
        Form.sendEmailCheck = QtGui.QCheckBox(Form.deployTabPage)
        Form.sendEmailCheck.setObjectName("sendEmailCheck")
        Form.verticalLayout_12.addWidget(Form.sendEmailCheck)
        Form.line = QtGui.QFrame(Form.deployTabPage)
        Form.line.setFrameShape(QtGui.QFrame.HLine)
        Form.line.setFrameShadow(QtGui.QFrame.Sunken)
        Form.line.setObjectName("line")
        Form.verticalLayout_12.addWidget(Form.line)
        Form.widget_18 = QtGui.QWidget(Form.deployTabPage)
        Form.widget_18.setObjectName("widget_18")
        Form.horizontalLayout_11 = QtGui.QHBoxLayout(Form.widget_18)
        Form.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        Form.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        Form.horizontalLayout_11.setObjectName("horizontalLayout_11")
        Form.widget_13 = QtGui.QWidget(Form.widget_18)
        Form.widget_13.setObjectName("widget_13")
        Form.verticalLayout_3 = QtGui.QVBoxLayout(Form.widget_13)
        Form.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        Form.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        Form.verticalLayout_3.setObjectName("verticalLayout_3")
        Form.widget_20 = QtGui.QWidget(Form.widget_13)
        Form.widget_20.setObjectName("widget_20")
        Form.horizontalLayout_12 = QtGui.QHBoxLayout(Form.widget_20)
        Form.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        Form.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        Form.horizontalLayout_12.setObjectName("horizontalLayout_12")
        Form.label_17 = QtGui.QLabel(Form.widget_20)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(50)
        font.setBold(False)
        Form.label_17.setFont(font)
        Form.label_17.setObjectName("label_17")
        Form.horizontalLayout_12.addWidget(Form.label_17)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Form.horizontalLayout_12.addItem(spacerItem7)
        Form.summaryDefaultBtn = QtGui.QPushButton(Form.widget_20)
        font = QtGui.QFont()
        font.setPointSize(8)
        Form.summaryDefaultBtn.setFont(font)
        Form.summaryDefaultBtn.setObjectName("summaryDefaultBtn")
        Form.horizontalLayout_12.addWidget(Form.summaryDefaultBtn)
        Form.verticalLayout_3.addWidget(Form.widget_20)
        Form.summaryText = QtGui.QPlainTextEdit(Form.widget_13)
        Form.summaryText.setObjectName("summaryText")
        Form.verticalLayout_3.addWidget(Form.summaryText)
        Form.horizontalLayout_11.addWidget(Form.widget_13)
        Form.widget_16 = QtGui.QWidget(Form.widget_18)
        Form.widget_16.setObjectName("widget_16")
        Form.verticalLayout_11 = QtGui.QVBoxLayout(Form.widget_16)
        Form.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        Form.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        Form.verticalLayout_11.setObjectName("verticalLayout_11")
        Form.widget_21 = QtGui.QWidget(Form.widget_16)
        Form.widget_21.setObjectName("widget_21")
        Form.horizontalLayout_13 = QtGui.QHBoxLayout(Form.widget_21)
        Form.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        Form.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        Form.horizontalLayout_13.setObjectName("horizontalLayout_13")
        Form.label_19 = QtGui.QLabel(Form.widget_21)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(50)
        font.setBold(False)
        Form.label_19.setFont(font)
        Form.label_19.setObjectName("label_19")
        Form.horizontalLayout_13.addWidget(Form.label_19)
        spacerItem8 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Form.horizontalLayout_13.addItem(spacerItem8)
        Form.additionsDefaultBtn = QtGui.QPushButton(Form.widget_21)
        font = QtGui.QFont()
        font.setPointSize(8)
        Form.additionsDefaultBtn.setFont(font)
        Form.additionsDefaultBtn.setObjectName("additionsDefaultBtn")
        Form.horizontalLayout_13.addWidget(Form.additionsDefaultBtn)
        Form.verticalLayout_11.addWidget(Form.widget_21)
        Form.additionsText = QtGui.QPlainTextEdit(Form.widget_16)
        Form.additionsText.setObjectName("additionsText")
        Form.verticalLayout_11.addWidget(Form.additionsText)
        Form.horizontalLayout_11.addWidget(Form.widget_16)
        Form.verticalLayout_12.addWidget(Form.widget_18)
        Form.widget_19 = QtGui.QWidget(Form.deployTabPage)
        Form.widget_19.setObjectName("widget_19")
        Form.horizontalLayout_10 = QtGui.QHBoxLayout(Form.widget_19)
        Form.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        Form.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        Form.horizontalLayout_10.setObjectName("horizontalLayout_10")
        Form.widget_14 = QtGui.QWidget(Form.widget_19)
        Form.widget_14.setObjectName("widget_14")
        Form.verticalLayout_9 = QtGui.QVBoxLayout(Form.widget_14)
        Form.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        Form.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        Form.verticalLayout_9.setObjectName("verticalLayout_9")
        Form.widget_22 = QtGui.QWidget(Form.widget_14)
        Form.widget_22.setObjectName("widget_22")
        Form.horizontalLayout_14 = QtGui.QHBoxLayout(Form.widget_22)
        Form.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        Form.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        Form.horizontalLayout_14.setObjectName("horizontalLayout_14")
        Form.label_18 = QtGui.QLabel(Form.widget_22)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(50)
        font.setBold(False)
        Form.label_18.setFont(font)
        Form.label_18.setObjectName("label_18")
        Form.horizontalLayout_14.addWidget(Form.label_18)
        spacerItem9 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Form.horizontalLayout_14.addItem(spacerItem9)
        Form.fixesDefaultBtn = QtGui.QPushButton(Form.widget_22)
        font = QtGui.QFont()
        font.setPointSize(8)
        Form.fixesDefaultBtn.setFont(font)
        Form.fixesDefaultBtn.setObjectName("fixesDefaultBtn")
        Form.horizontalLayout_14.addWidget(Form.fixesDefaultBtn)
        Form.verticalLayout_9.addWidget(Form.widget_22)
        Form.fixesText = QtGui.QPlainTextEdit(Form.widget_14)
        Form.fixesText.setObjectName("fixesText")
        Form.verticalLayout_9.addWidget(Form.fixesText)
        Form.horizontalLayout_10.addWidget(Form.widget_14)
        Form.widget_15 = QtGui.QWidget(Form.widget_19)
        Form.widget_15.setObjectName("widget_15")
        Form.verticalLayout_10 = QtGui.QVBoxLayout(Form.widget_15)
        Form.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        Form.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        Form.verticalLayout_10.setObjectName("verticalLayout_10")
        Form.widget_23 = QtGui.QWidget(Form.widget_15)
        Form.widget_23.setObjectName("widget_23")
        Form.horizontalLayout_15 = QtGui.QHBoxLayout(Form.widget_23)
        Form.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        Form.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        Form.horizontalLayout_15.setObjectName("horizontalLayout_15")
        Form.label_20 = QtGui.QLabel(Form.widget_23)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(50)
        font.setBold(False)
        Form.label_20.setFont(font)
        Form.label_20.setObjectName("label_20")
        Form.horizontalLayout_15.addWidget(Form.label_20)
        spacerItem10 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Form.horizontalLayout_15.addItem(spacerItem10)
        Form.removalsDefaultBtn = QtGui.QPushButton(Form.widget_23)
        font = QtGui.QFont()
        font.setPointSize(8)
        Form.removalsDefaultBtn.setFont(font)
        Form.removalsDefaultBtn.setObjectName("removalsDefaultBtn")
        Form.horizontalLayout_15.addWidget(Form.removalsDefaultBtn)
        Form.verticalLayout_10.addWidget(Form.widget_23)
        Form.removalsText = QtGui.QPlainTextEdit(Form.widget_15)
        Form.removalsText.setObjectName("removalsText")
        Form.verticalLayout_10.addWidget(Form.removalsText)
        Form.horizontalLayout_10.addWidget(Form.widget_15)
        Form.verticalLayout_12.addWidget(Form.widget_19)
        Form.widget_17 = QtGui.QWidget(Form.deployTabPage)
        Form.widget_17.setObjectName("widget_17")
        Form.verticalLayout_8 = QtGui.QVBoxLayout(Form.widget_17)
        Form.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        Form.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        Form.verticalLayout_8.setObjectName("verticalLayout_8")
        Form.widget_24 = QtGui.QWidget(Form.widget_17)
        Form.widget_24.setObjectName("widget_24")
        Form.horizontalLayout_16 = QtGui.QHBoxLayout(Form.widget_24)
        Form.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        Form.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        Form.horizontalLayout_16.setObjectName("horizontalLayout_16")
        Form.label_21 = QtGui.QLabel(Form.widget_24)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(50)
        font.setBold(False)
        Form.label_21.setFont(font)
        Form.label_21.setObjectName("label_21")
        Form.horizontalLayout_16.addWidget(Form.label_21)
        spacerItem11 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Form.horizontalLayout_16.addItem(spacerItem11)
        Form.releaseInfoDefaultBtn = QtGui.QPushButton(Form.widget_24)
        font = QtGui.QFont()
        font.setPointSize(8)
        Form.releaseInfoDefaultBtn.setFont(font)
        Form.releaseInfoDefaultBtn.setObjectName("releaseInfoDefaultBtn")
        Form.horizontalLayout_16.addWidget(Form.releaseInfoDefaultBtn)
        Form.verticalLayout_8.addWidget(Form.widget_24)
        Form.releaseInfoText = QtGui.QPlainTextEdit(Form.widget_17)
        Form.releaseInfoText.setObjectName("releaseInfoText")
        Form.verticalLayout_8.addWidget(Form.releaseInfoText)
        Form.verticalLayout_12.addWidget(Form.widget_17)
        Form.widget_12 = QtGui.QWidget(Form.deployTabPage)
        Form.widget_12.setObjectName("widget_12")
        Form.horizontalLayout_9 = QtGui.QHBoxLayout(Form.widget_12)
        Form.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        Form.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        Form.horizontalLayout_9.setObjectName("horizontalLayout_9")
        Form.deployBuildBtn = QtGui.QPushButton(Form.widget_12)
        font = QtGui.QFont()
        font.setPointSize(10)
        Form.deployBuildBtn.setFont(font)
        Form.deployBuildBtn.setObjectName("deployBuildBtn")
        Form.horizontalLayout_9.addWidget(Form.deployBuildBtn)
        spacerItem12 = QtGui.QSpacerItem(514, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Form.horizontalLayout_9.addItem(spacerItem12)
        Form.verticalLayout_12.addWidget(Form.widget_12)
        Form.mainTab.addTab(Form.deployTabPage, "")
        Form.descriptorTabPage = QtGui.QWidget()
        Form.descriptorTabPage.setObjectName("descriptorTabPage")
        Form.verticalLayout_2 = QtGui.QVBoxLayout(Form.descriptorTabPage)
        Form.verticalLayout_2.setObjectName("verticalLayout_2")
        Form.label = QtGui.QLabel(Form.descriptorTabPage)
        font = QtGui.QFont()
        font.setPointSize(12)
        Form.label.setFont(font)
        Form.label.setObjectName("label")
        Form.verticalLayout_2.addWidget(Form.label)
        Form.widget_10 = QtGui.QWidget(Form.descriptorTabPage)
        Form.widget_10.setObjectName("widget_10")
        Form.horizontalLayout_6 = QtGui.QHBoxLayout(Form.widget_10)
        Form.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        Form.horizontalLayout_6.setObjectName("horizontalLayout_6")
        Form.widget_8 = QtGui.QWidget(Form.widget_10)
        Form.widget_8.setObjectName("widget_8")
        Form.formLayout_3 = QtGui.QFormLayout(Form.widget_8)
        Form.formLayout_3.setContentsMargins(0, 0, 0, 0)
        Form.formLayout_3.setContentsMargins(0, 0, 0, 0)
        Form.formLayout_3.setObjectName("formLayout_3")
        Form.label_13 = QtGui.QLabel(Form.widget_8)
        Form.label_13.setObjectName("label_13")
        Form.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, Form.label_13)
        Form.prefixLine = QtGui.QLineEdit(Form.widget_8)
        Form.prefixLine.setObjectName("prefixLine")
        Form.formLayout_3.setWidget(0, QtGui.QFormLayout.FieldRole, Form.prefixLine)
        Form.label_14 = QtGui.QLabel(Form.widget_8)
        Form.label_14.setObjectName("label_14")
        Form.formLayout_3.setWidget(1, QtGui.QFormLayout.LabelRole, Form.label_14)
        Form.suffixSpin = QtGui.QSpinBox(Form.widget_8)
        Form.suffixSpin.setObjectName("suffixSpin")
        Form.formLayout_3.setWidget(1, QtGui.QFormLayout.FieldRole, Form.suffixSpin)
        Form.horizontalLayout_6.addWidget(Form.widget_8)
        spacerItem13 = QtGui.QSpacerItem(284, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Form.horizontalLayout_6.addItem(spacerItem13)
        Form.verticalLayout_2.addWidget(Form.widget_10)
        Form.label_2 = QtGui.QLabel(Form.descriptorTabPage)
        font = QtGui.QFont()
        font.setPointSize(12)
        Form.label_2.setFont(font)
        Form.label_2.setObjectName("label_2")
        Form.verticalLayout_2.addWidget(Form.label_2)
        Form.widget_9 = QtGui.QWidget(Form.descriptorTabPage)
        Form.widget_9.setObjectName("widget_9")
        Form.horizontalLayout_7 = QtGui.QHBoxLayout(Form.widget_9)
        Form.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        Form.horizontalLayout_7.setObjectName("horizontalLayout_7")
        Form.widget_3 = QtGui.QWidget(Form.widget_9)
        Form.widget_3.setObjectName("widget_3")
        Form.formLayout_2 = QtGui.QFormLayout(Form.widget_3)
        Form.formLayout_2.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        Form.formLayout_2.setContentsMargins(0, 0, 0, 0)
        Form.formLayout_2.setContentsMargins(0, 0, 0, 0)
        Form.formLayout_2.setObjectName("formLayout_2")
        Form.label_10 = QtGui.QLabel(Form.widget_3)
        Form.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        Form.label_10.setObjectName("label_10")
        Form.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, Form.label_10)
        Form.majorSpin = QtGui.QSpinBox(Form.widget_3)
        Form.majorSpin.setObjectName("majorSpin")
        Form.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, Form.majorSpin)
        Form.label_11 = QtGui.QLabel(Form.widget_3)
        Form.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        Form.label_11.setObjectName("label_11")
        Form.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, Form.label_11)
        Form.minorSpin = QtGui.QSpinBox(Form.widget_3)
        Form.minorSpin.setObjectName("minorSpin")
        Form.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, Form.minorSpin)
        Form.label_12 = QtGui.QLabel(Form.widget_3)
        Form.label_12.setObjectName("label_12")
        Form.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, Form.label_12)
        Form.revisionSpin = QtGui.QSpinBox(Form.widget_3)
        Form.revisionSpin.setObjectName("revisionSpin")
        Form.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, Form.revisionSpin)
        Form.horizontalLayout_7.addWidget(Form.widget_3)
        spacerItem14 = QtGui.QSpacerItem(483, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Form.horizontalLayout_7.addItem(spacerItem14)
        Form.verticalLayout_2.addWidget(Form.widget_9)
        Form.widget_11 = QtGui.QWidget(Form.descriptorTabPage)
        Form.widget_11.setObjectName("widget_11")
        Form.horizontalLayout_8 = QtGui.QHBoxLayout(Form.widget_11)
        Form.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        Form.horizontalLayout_8.setObjectName("horizontalLayout_8")
        Form.reloadSettingsBtn = QtGui.QPushButton(Form.widget_11)
        Form.reloadSettingsBtn.setObjectName("reloadSettingsBtn")
        Form.horizontalLayout_8.addWidget(Form.reloadSettingsBtn)
        Form.incrementSettingsBtn = QtGui.QPushButton(Form.widget_11)
        Form.incrementSettingsBtn.setObjectName("incrementSettingsBtn")
        Form.horizontalLayout_8.addWidget(Form.incrementSettingsBtn)
        Form.writeSettingsBtn = QtGui.QPushButton(Form.widget_11)
        Form.writeSettingsBtn.setObjectName("writeSettingsBtn")
        Form.horizontalLayout_8.addWidget(Form.writeSettingsBtn)
        spacerItem15 = QtGui.QSpacerItem(415, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Form.horizontalLayout_8.addItem(spacerItem15)
        Form.verticalLayout_2.addWidget(Form.widget_11)
        spacerItem16 = QtGui.QSpacerItem(20, 152, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        Form.verticalLayout_2.addItem(spacerItem16)
        Form.mainTab.addTab(Form.descriptorTabPage, "")
        Form.utilsTabPage = QtGui.QWidget()
        Form.utilsTabPage.setObjectName("utilsTabPage")
        Form.installApkBtn = QtGui.QPushButton(Form.utilsTabPage)
        Form.installApkBtn.setGeometry(QtCore.QRect(10, 180, 101, 23))
        Form.installApkBtn.setObjectName("installApkBtn")
        Form.runDebugBtn = QtGui.QPushButton(Form.utilsTabPage)
        Form.runDebugBtn.setGeometry(QtCore.QRect(10, 70, 101, 23))
        Form.runDebugBtn.setObjectName("runDebugBtn")
        Form.label_6 = QtGui.QLabel(Form.utilsTabPage)
        Form.label_6.setGeometry(QtCore.QRect(10, 130, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        Form.label_6.setFont(font)
        Form.label_6.setObjectName("label_6")
        Form.label_7 = QtGui.QLabel(Form.utilsTabPage)
        Form.label_7.setGeometry(QtCore.QRect(10, 160, 211, 16))
        Form.label_7.setObjectName("label_7")
        Form.label_8 = QtGui.QLabel(Form.utilsTabPage)
        Form.label_8.setGeometry(QtCore.QRect(10, 10, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        Form.label_8.setFont(font)
        Form.label_8.setObjectName("label_8")
        Form.label_9 = QtGui.QLabel(Form.utilsTabPage)
        Form.label_9.setGeometry(QtCore.QRect(10, 40, 211, 16))
        Form.label_9.setObjectName("label_9")
        Form.logcatDumpBtn = QtGui.QPushButton(Form.utilsTabPage)
        Form.logcatDumpBtn.setGeometry(QtCore.QRect(120, 180, 121, 23))
        Form.logcatDumpBtn.setObjectName("logcatDumpBtn")
        Form.clearLogcatBtn = QtGui.QPushButton(Form.utilsTabPage)
        Form.clearLogcatBtn.setGeometry(QtCore.QRect(120, 210, 121, 23))
        Form.clearLogcatBtn.setObjectName("clearLogcatBtn")
        Form.flexDebugBtn = QtGui.QPushButton(Form.utilsTabPage)
        Form.flexDebugBtn.setGeometry(QtCore.QRect(250, 180, 131, 23))
        Form.flexDebugBtn.setObjectName("flexDebugBtn")
        Form.label_15 = QtGui.QLabel(Form.utilsTabPage)
        Form.label_15.setGeometry(QtCore.QRect(10, 260, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        Form.label_15.setFont(font)
        Form.label_15.setObjectName("label_15")
        Form.label_16 = QtGui.QLabel(Form.utilsTabPage)
        Form.label_16.setGeometry(QtCore.QRect(10, 290, 211, 16))
        Form.label_16.setObjectName("label_16")
        Form.installIpaBtn = QtGui.QPushButton(Form.utilsTabPage)
        Form.installIpaBtn.setGeometry(QtCore.QRect(10, 310, 101, 23))
        Form.installIpaBtn.setObjectName("installIpaBtn")
        Form.mainTab.addTab(Form.utilsTabPage, "")
        Form.resultsTabPage = QtGui.QWidget()
        Form.resultsTabPage.setObjectName("resultsTabPage")
        Form.verticalLayout = QtGui.QVBoxLayout(Form.resultsTabPage)
        Form.verticalLayout.setObjectName("verticalLayout")
        Form.resultsTextBrowser = QtGui.QTextBrowser(Form.resultsTabPage)
        Form.resultsTextBrowser.setEnabled(True)
        Form.resultsTextBrowser.setProperty("cursor", QtCore.Qt.ArrowCursor)
        Form.resultsTextBrowser.setAcceptDrops(True)
        Form.resultsTextBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        Form.resultsTextBrowser.setObjectName("resultsTextBrowser")
        Form.verticalLayout.addWidget(Form.resultsTextBrowser)
        Form.mainTab.addTab(Form.resultsTabPage, "")
        Form.horizontalLayout_5.addWidget(Form.mainTab)

        self.retranslateUi(Form)
        Form.mainTab.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(Form.sendEmailCheck, Form.summaryText)
        Form.setTabOrder(Form.summaryText, Form.additionsText)
        Form.setTabOrder(Form.additionsText, Form.fixesText)
        Form.setTabOrder(Form.fixesText, Form.removalsText)
        Form.setTabOrder(Form.removalsText, Form.releaseInfoText)
        Form.setTabOrder(Form.releaseInfoText, Form.deployBuildBtn)
        Form.setTabOrder(Form.deployBuildBtn, Form.flashPlayerComboBox)
        Form.setTabOrder(Form.flashPlayerComboBox, Form.airSDKComboBox)
        Form.setTabOrder(Form.airSDKComboBox, Form.iosPlatformCheck)
        Form.setTabOrder(Form.iosPlatformCheck, Form.mainTab)
        Form.setTabOrder(Form.mainTab, Form.compileBtn)
        Form.setTabOrder(Form.compileBtn, Form.prefixLine)
        Form.setTabOrder(Form.prefixLine, Form.suffixSpin)
        Form.setTabOrder(Form.suffixSpin, Form.majorSpin)
        Form.setTabOrder(Form.majorSpin, Form.minorSpin)
        Form.setTabOrder(Form.minorSpin, Form.revisionSpin)
        Form.setTabOrder(Form.revisionSpin, Form.reloadSettingsBtn)
        Form.setTabOrder(Form.reloadSettingsBtn, Form.incrementSettingsBtn)
        Form.setTabOrder(Form.incrementSettingsBtn, Form.writeSettingsBtn)
        Form.setTabOrder(Form.writeSettingsBtn, Form.installApkBtn)
        Form.setTabOrder(Form.installApkBtn, Form.runDebugBtn)
        Form.setTabOrder(Form.runDebugBtn, Form.logcatDumpBtn)
        Form.setTabOrder(Form.logcatDumpBtn, Form.clearLogcatBtn)
        Form.setTabOrder(Form.clearLogcatBtn, Form.flexDebugBtn)
        Form.setTabOrder(Form.flexDebugBtn, Form.installIpaBtn)
        Form.setTabOrder(Form.installIpaBtn, Form.resultsTextBrowser)
        Form.setTabOrder(Form.resultsTextBrowser, Form.desktopPlatformCheck)
        Form.setTabOrder(Form.desktopPlatformCheck, Form.androidPlatformCheck)
        Form.setTabOrder(Form.androidPlatformCheck, Form.remoteDebugComboBox)
        Form.setTabOrder(Form.remoteDebugComboBox, Form.liveCheck)
        Form.setTabOrder(Form.liveCheck, Form.debugCheck)
        Form.setTabOrder(Form.debugCheck, Form.packageAirCheck)
        Form.setTabOrder(Form.packageAirCheck, Form.webPlatformCheck)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "ANE Compiler", None, QtGui.QApplication.UnicodeUTF8))
        Form.groupBox_3.setTitle(QtGui.QApplication.translate("Form", "Compile Modes", None, QtGui.QApplication.UnicodeUTF8))
        Form.debugCheck.setText(QtGui.QApplication.translate("Form", "Debug", None, QtGui.QApplication.UnicodeUTF8))
        Form.liveCheck.setText(QtGui.QApplication.translate("Form", "Live", None, QtGui.QApplication.UnicodeUTF8))
        Form.packageAirCheck.setText(QtGui.QApplication.translate("Form", "Package AIR", None, QtGui.QApplication.UnicodeUTF8))
        Form.platformBox.setTitle(QtGui.QApplication.translate("Form", "Platforms To Compile", None, QtGui.QApplication.UnicodeUTF8))
        Form.webPlatformCheck.setText(QtGui.QApplication.translate("Form", "Web (Flash)", None, QtGui.QApplication.UnicodeUTF8))
        Form.desktopPlatformCheck.setText(QtGui.QApplication.translate("Form", "Desktop (AIR/Native)", None, QtGui.QApplication.UnicodeUTF8))
        Form.androidPlatformCheck.setText(QtGui.QApplication.translate("Form", "Android", None, QtGui.QApplication.UnicodeUTF8))
        Form.iosPlatformCheck.setText(QtGui.QApplication.translate("Form", "iOS", None, QtGui.QApplication.UnicodeUTF8))
        Form.label_3.setText(QtGui.QApplication.translate("Form", "Flash Player Version:", None, QtGui.QApplication.UnicodeUTF8))
        Form.label_4.setText(QtGui.QApplication.translate("Form", "AIR SDK Version:", None, QtGui.QApplication.UnicodeUTF8))
        Form.label_5.setText(QtGui.QApplication.translate("Form", "Remote Debugging:", None, QtGui.QApplication.UnicodeUTF8))
        Form.compileBtn.setText(QtGui.QApplication.translate("Form", "Compile", None, QtGui.QApplication.UnicodeUTF8))
        Form.mainTab.setTabText(Form.mainTab.indexOf(Form.settingsTabPage), QtGui.QApplication.translate("Form", "Compile", None, QtGui.QApplication.UnicodeUTF8))
        Form.sendEmailCheck.setText(QtGui.QApplication.translate("Form", "Send Email Notifications", None, QtGui.QApplication.UnicodeUTF8))
        Form.label_17.setText(QtGui.QApplication.translate("Form", "Summary", None, QtGui.QApplication.UnicodeUTF8))
        Form.summaryDefaultBtn.setText(QtGui.QApplication.translate("Form", "Set As Default", None, QtGui.QApplication.UnicodeUTF8))
        Form.label_19.setText(QtGui.QApplication.translate("Form", "New Additions", None, QtGui.QApplication.UnicodeUTF8))
        Form.additionsDefaultBtn.setText(QtGui.QApplication.translate("Form", "Set As Default", None, QtGui.QApplication.UnicodeUTF8))
        Form.label_18.setText(QtGui.QApplication.translate("Form", "Fixes & Changes", None, QtGui.QApplication.UnicodeUTF8))
        Form.fixesDefaultBtn.setText(QtGui.QApplication.translate("Form", "Set As Default", None, QtGui.QApplication.UnicodeUTF8))
        Form.label_20.setText(QtGui.QApplication.translate("Form", "Removals", None, QtGui.QApplication.UnicodeUTF8))
        Form.removalsDefaultBtn.setText(QtGui.QApplication.translate("Form", "Set As Default", None, QtGui.QApplication.UnicodeUTF8))
        Form.label_21.setText(QtGui.QApplication.translate("Form", "Release Information", None, QtGui.QApplication.UnicodeUTF8))
        Form.releaseInfoDefaultBtn.setText(QtGui.QApplication.translate("Form", "Set As Default", None, QtGui.QApplication.UnicodeUTF8))
        Form.deployBuildBtn.setText(QtGui.QApplication.translate("Form", "Deploy", None, QtGui.QApplication.UnicodeUTF8))
        Form.mainTab.setTabText(Form.mainTab.indexOf(Form.deployTabPage), QtGui.QApplication.translate("Form", "Deploy", None, QtGui.QApplication.UnicodeUTF8))
        Form.label.setText(QtGui.QApplication.translate("Form", "Version Label:", None, QtGui.QApplication.UnicodeUTF8))
        Form.label_13.setText(QtGui.QApplication.translate("Form", "Prefix", None, QtGui.QApplication.UnicodeUTF8))
        Form.label_14.setText(QtGui.QApplication.translate("Form", "Suffix", None, QtGui.QApplication.UnicodeUTF8))
        Form.label_2.setText(QtGui.QApplication.translate("Form", "Version Number:", None, QtGui.QApplication.UnicodeUTF8))
        Form.label_10.setText(QtGui.QApplication.translate("Form", "Major", None, QtGui.QApplication.UnicodeUTF8))
        Form.label_11.setText(QtGui.QApplication.translate("Form", "Minor", None, QtGui.QApplication.UnicodeUTF8))
        Form.label_12.setText(QtGui.QApplication.translate("Form", "Revision", None, QtGui.QApplication.UnicodeUTF8))
        Form.reloadSettingsBtn.setText(QtGui.QApplication.translate("Form", "Reload", None, QtGui.QApplication.UnicodeUTF8))
        Form.incrementSettingsBtn.setText(QtGui.QApplication.translate("Form", "Increment", None, QtGui.QApplication.UnicodeUTF8))
        Form.writeSettingsBtn.setText(QtGui.QApplication.translate("Form", "Write", None, QtGui.QApplication.UnicodeUTF8))
        Form.mainTab.setTabText(Form.mainTab.indexOf(Form.descriptorTabPage), QtGui.QApplication.translate("Form", "Version", None, QtGui.QApplication.UnicodeUTF8))
        Form.installApkBtn.setText(QtGui.QApplication.translate("Form", "Install APK", None, QtGui.QApplication.UnicodeUTF8))
        Form.runDebugBtn.setText(QtGui.QApplication.translate("Form", "Run Debug", None, QtGui.QApplication.UnicodeUTF8))
        Form.label_6.setText(QtGui.QApplication.translate("Form", "Android", None, QtGui.QApplication.UnicodeUTF8))
        Form.label_7.setText(QtGui.QApplication.translate("Form", "Android Device Utilities", None, QtGui.QApplication.UnicodeUTF8))
        Form.label_8.setText(QtGui.QApplication.translate("Form", "Desktop", None, QtGui.QApplication.UnicodeUTF8))
        Form.label_9.setText(QtGui.QApplication.translate("Form", "Desktop Device Utilities", None, QtGui.QApplication.UnicodeUTF8))
        Form.logcatDumpBtn.setText(QtGui.QApplication.translate("Form", "Echo Logcat Dump", None, QtGui.QApplication.UnicodeUTF8))
        Form.clearLogcatBtn.setText(QtGui.QApplication.translate("Form", "Clear Logcat", None, QtGui.QApplication.UnicodeUTF8))
        Form.flexDebugBtn.setText(QtGui.QApplication.translate("Form", "FDB Debug Session", None, QtGui.QApplication.UnicodeUTF8))
        Form.label_15.setText(QtGui.QApplication.translate("Form", "iOS", None, QtGui.QApplication.UnicodeUTF8))
        Form.label_16.setText(QtGui.QApplication.translate("Form", "iOS Device Utilities", None, QtGui.QApplication.UnicodeUTF8))
        Form.installIpaBtn.setText(QtGui.QApplication.translate("Form", "Install IPA", None, QtGui.QApplication.UnicodeUTF8))
        Form.mainTab.setTabText(Form.mainTab.indexOf(Form.utilsTabPage), QtGui.QApplication.translate("Form", "Utilities", None, QtGui.QApplication.UnicodeUTF8))
        Form.mainTab.setTabText(Form.mainTab.indexOf(Form.resultsTabPage), QtGui.QApplication.translate("Form", "Results", None, QtGui.QApplication.UnicodeUTF8))

