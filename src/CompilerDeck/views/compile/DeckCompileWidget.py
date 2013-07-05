# DeckCompileWidget.py
# (C)2013
# Scott Ernst

from PySide import QtGui
from PySide import QtCore

from pyglass.widgets.PyGlassWidget import PyGlassWidget

from CompilerDeck.CompilerDeckEnvironment import CompilerDeckEnvironment
from CompilerDeck.adobe.air.AirDebugThread import AirDebugThread
from CompilerDeck.adobe.air.InstallApkThread import InstallApkThread
from CompilerDeck.adobe.ane.ANECompileThread import ANECompileThread
from CompilerDeck.adobe.flex.FlexDebugThread import FlexDebugThread
from CompilerDeck.adobe.flex.FlexProjectData import FlexProjectData
from CompilerDeck.android.AndroidLogcatThread import AndroidLogcatThread
from CompilerDeck.local.ToolsEnvironment import ToolsEnvironment

#___________________________________________________________________________________________________ DeckCompileWidget
class DeckCompileWidget(PyGlassWidget):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _AIR_SDK_VERSION_CFG      = 'AIR_SDK_VERSION'
    _FLASH_PLAYER_VERSION_CFG = 'FLASH_PLAYER_VERSION'
    _FLASH_PROJECT_PATH_CFG   = 'FLASH_PROJECT_PATH'
    _PACKAGE_AIR_CFG          = 'PACKAGE_AIR'
    _QUICK_COMPILE_CFG        = 'QUICK_COMPILE'
    _LIVE_CFG                 = 'LIVE'
    _DEBUG_CFG                = 'DEBUG'
    _COMPILE_WEB              = 'COMPILE_WEB'
    _COMPILE_DESKTOP          = 'COMPILE_DESKTOP'
    _COMPILE_ANDROID          = 'COMPILE_ANDROID'
    _COMPILE_IOS              = 'COMPILE_IOS'

#___________________________________________________________________________________________________ __init__
    def __init__(self, *args, **kwargs):
        """Creates a new instance of DeckCompileWidget."""
        super(DeckCompileWidget, self).__init__(*args, **kwargs)

        self._results    = ''
        self._compThread = None

        versions = ToolsEnvironment.listInstalledAirSDKs()
        if versions:
            version  = self.parent().appConfig.get(self._AIR_SDK_VERSION_CFG)
            if version is None:
                self.parent().appConfig.set(self._AIR_SDK_VERSION_CFG, versions[0])
                version = versions[0]
            for v in versions:
                self.airSDKComboBox.addItem(v)
            self.airSDKComboBox.setCurrentIndex(self.airSDKComboBox.findText(version))
        self.airSDKComboBox.currentIndexChanged.connect(self._handleAirVersionChanged)

        versions = ToolsEnvironment.listInstalledFlashPlayers()
        if versions:
            version  = self.parent().appConfig.get(self._FLASH_PLAYER_VERSION_CFG)
            if version is None:
                self.parent().appConfig.set(self._FLASH_PLAYER_VERSION_CFG, versions[0])
                version = versions[0]
            for v in versions:
                self.flashPlayerComboBox.addItem(v)
            self.flashPlayerComboBox.setCurrentIndex(self.flashPlayerComboBox.findText(version))
        self.flashPlayerComboBox.currentIndexChanged.connect(self._handleFlashVersionChanged)

        for item in ['None', 'WiFi Connection', 'USB Connection (Android)']:
            self.remoteDebugComboBox.addItem(item)

        self.resultsTextBrowser.setReadOnly(True)
        self.compileBtn.clicked.connect(self._handleCompileClick)
        self.runDebugBtn.clicked.connect(self._handleRunDebug)
        self.installApkBtn.clicked.connect(self._handleInstallApk)
        self.logcatDumpBtn.clicked.connect(self._handleGetLogcatDump)
        self.clearLogcatBtn.clicked.connect(self._handleClearLogcat)
        self.flexDebugBtn.clicked.connect(self._handleFlexDebugSession)
        self.mainTab.setCurrentIndex(0)

        self._setCheckState(
            self.debugCheck,
            self.parent().appConfig.get(self._DEBUG_CFG, True))
        self.debugCheck.stateChanged.connect(self._handleCheckStateChange)

        self._setCheckState(
            self.liveCheck,
            self.parent().appConfig.get(self._LIVE_CFG, False))
        self.liveCheck.stateChanged.connect(self._handleCheckStateChange)

        self._setCheckState(
            self.quickCompileCheck,
            self.parent().appConfig.get(self._QUICK_COMPILE_CFG, False))
        self.quickCompileCheck.stateChanged.connect(self._handleCheckStateChange)

        self._setCheckState(
            self.packageAirCheck,
            self.parent().appConfig.get(self._PACKAGE_AIR_CFG, False))
        self.packageAirCheck.stateChanged.connect(self._handleCheckStateChange)

        self._setCheckState(
            self.webPlatformCheck,
            self.parent().appConfig.get(self._COMPILE_WEB, True))
        self.webPlatformCheck.stateChanged.connect(self._handleCheckStateChange)

        self._setCheckState(
            self.desktopPlatformCheck,
            self.parent().appConfig.get(self._COMPILE_DESKTOP, True))
        self.webPlatformCheck.stateChanged.connect(self._handleCheckStateChange)

        self._setCheckState(
            self.androidPlatformCheck,
            self.parent().appConfig.get(self._COMPILE_ANDROID, True))
        self.androidPlatformCheck.stateChanged.connect(self._handleCheckStateChange)

        self._setCheckState(
            self.iosPlatformCheck,
            self.parent().appConfig.get(self._COMPILE_IOS, True))
        self.iosPlatformCheck.stateChanged.connect(self._handleCheckStateChange)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _setCheckState
    def _setCheckState(self, target, value):
        target.setCheckState(QtCore.Qt.Checked if value else QtCore.Qt.Unchecked)

#___________________________________________________________________________________________________ _executeRemoteThread
    def _executeRemoteThread(self, thread):
        self.resultsTextBrowser.clear()
        self.log.addPrintCallback(self._handleUpdateResults)
        self.resultsTextBrowser.setFocus()
        self.mainTab.setCurrentIndex(1)
        self._toggleInteractivity(False)
        self.refreshGui()

        self._compThread = thread
        thread.logSignal.signal.connect(self._handleUpdateResults)
        thread.completeSignal.signal.connect(self._handleRemoteThreadComplete)

        thread.start()

#___________________________________________________________________________________________________ _toggleInteractivity
    def _toggleInteractivity(self, value):
        self.compileBtn.setEnabled(value)
        self.settingsTabPage.setEnabled(value)
        self.utilsTabPage.setEnabled(value)

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleCompileClick
    def _handleCompileClick(self, *args, **kwargs):
        self._executeRemoteThread(ANECompileThread(
            parent=self,
            projectPath=CompilerDeckEnvironment.getProjectPath(),
            debug=self.debugCheck.isChecked(),
            live=self.liveCheck.isChecked(),
            quickCompile=self.quickCompileCheck.isChecked(),
            airVersion=str(self.airSDKComboBox.currentText()),
            flashVersion=str(self.flashPlayerComboBox.currentText()),
            packageAir=self.packageAirCheck.isChecked(),
            remoteDebug=(not self.remoteDebugComboBox.currentText().lower().startswith('none')),
            usbDebug=(self.remoteDebugComboBox.currentText().lower().startswith('usb')),
            platforms={
                FlexProjectData.NATIVE_PLATFORM:self.desktopPlatformCheck.isChecked(),
                FlexProjectData.AIR_PLATFORM:self.desktopPlatformCheck.isChecked(),
                FlexProjectData.FLASH_PLATFORM:self.webPlatformCheck.isChecked(),
                FlexProjectData.ANDROID_PLATFORM:self.androidPlatformCheck.isChecked(),
                FlexProjectData.IOS_PLATFORM:self.iosPlatformCheck.isChecked()
            }
        ))

#___________________________________________________________________________________________________ _handleRemoteThreadComplete
    def _handleRemoteThreadComplete(self, result):
        self.log.removePrintCallback(self._handleUpdateResults)
        self._toggleInteractivity(True)

#___________________________________________________________________________________________________ _handleUpdateResults
    def _handleUpdateResults(self, value):
        tb = self.resultsTextBrowser
        tb.moveCursor(QtGui.QTextCursor.End)
        tb.append(value.replace('\n', '<br />') + '<br />')
        self.refreshGui()

#___________________________________________________________________________________________________ _handleFlashVersionChanged
    def _handleFlashVersionChanged(self):
        self.parent().appConfig.set(
            self._FLASH_PLAYER_VERSION_CFG,
            self.flashPlayerComboBox.currentText()
        )

#___________________________________________________________________________________________________ _handleAirVersionChanged
    def _handleAirVersionChanged(self):
        self.parent().appConfig.set(
            self._AIR_SDK_VERSION_CFG,
            self.airSDKComboBox.currentText()
        )

#___________________________________________________________________________________________________ _handlePackageAirStateChange
    def _handleCheckStateChange(self):
        sender = self.sender()
        prop   = None
        if sender == self.packageAirCheck:
            prop = self._PACKAGE_AIR_CFG
        elif sender == self.quickCompileCheck:
            prop = self._QUICK_COMPILE_CFG
        elif sender == self.liveCheck:
            prop = self._LIVE_CFG
        elif sender == self.debugCheck:
            prop = self._DEBUG_CFG
        elif sender == self.webPlatformCheck:
            prop = self._COMPILE_WEB
        elif sender == self.desktopPlatformCheck:
            prop = self._COMPILE_DESKTOP
        elif sender == self.androidPlatformCheck:
            prop = self._COMPILE_ANDROID
        elif sender == self.iosPlatformCheck:
            prop = self._COMPILE_IOS

        if prop:
            self.owner.appConfig.set(prop, sender.isChecked())

#___________________________________________________________________________________________________ _handleRunDebug
    def _handleRunDebug(self):
        self._executeRemoteThread(AirDebugThread(
            parent=self,
            projectPath=CompilerDeckEnvironment.getProjectPath(),
            airVersion=str(self.airSDKComboBox.currentText()),
            flashVersion=str(self.flashPlayerComboBox.currentText()),
        ))

#___________________________________________________________________________________________________ _handleInstallApk
    def _handleInstallApk(self):
        self._executeRemoteThread(InstallApkThread(
            parent=self,
            projectPath=CompilerDeckEnvironment.getProjectPath(),
        ))

#___________________________________________________________________________________________________ _handleGetLogcatDump
    def _handleGetLogcatDump(self):
        self._executeRemoteThread(AndroidLogcatThread(
            parent=self,
            mode=AndroidLogcatThread.DUMP_MODE
        ))

#___________________________________________________________________________________________________ _handleClearLogcat
    def _handleClearLogcat(self):
        self._executeRemoteThread(AndroidLogcatThread(
            parent=self,
            mode=AndroidLogcatThread.CLEAR_MODE
        ))

#___________________________________________________________________________________________________ _handleFlexDebugSession
    def _handleFlexDebugSession(self):
        self._executeRemoteThread(FlexDebugThread(parent=self))

