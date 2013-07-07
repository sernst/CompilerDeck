# DeckCompileWidget.py
# (C)2013
# Scott Ernst

from PySide import QtGui
from PySide import QtCore

from pyaid.config.SettingsConfig import SettingsConfig

from pyglass.widgets.PyGlassWidget import PyGlassWidget

from CompilerDeck.CompilerDeckEnvironment import CompilerDeckEnvironment
from CompilerDeck.SettingsEditor import SettingsEditor
from CompilerDeck.adobe.air.AirDebugThread import AirDebugThread
from CompilerDeck.adobe.air.InstallApkThread import InstallApkThread
from CompilerDeck.adobe.air.InstallIpaThread import InstallIpaThread
from CompilerDeck.adobe.ane.ANECompileThread import ANECompileThread
from CompilerDeck.adobe.flex.FlexDebugThread import FlexDebugThread
from CompilerDeck.adobe.flex.FlexProjectData import FlexProjectData
from CompilerDeck.android.AndroidLogcatThread import AndroidLogcatThread
from CompilerDeck.deploy.S3DeployerThread import S3DeployerThread

#___________________________________________________________________________________________________ DeckCompileWidget
class DeckCompileWidget(PyGlassWidget):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _AIR_SDK_VERSION_CFG      = 'AIR_SDK_VERSION'
    _FLASH_PLAYER_VERSION_CFG = 'FLASH_PLAYER_VERSION'
    _FLASH_PROJECT_PATH_CFG   = 'FLASH_PROJECT_PATH'
    _PACKAGE_AIR_CFG          = 'PACKAGE_AIR'
    _AUTO_VERSION_CFG         = 'AUTO_VERSION'
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

        self._results       = ''
        self._compThread    = None
        self._buildSnapshot = None
        self._package       = False

        versions = self.mainWindow.listInstalledAirSDKs()
        if versions:
            version  = self.parent().appConfig.get(self._AIR_SDK_VERSION_CFG)
            if version is None:
                self.parent().appConfig.set(self._AIR_SDK_VERSION_CFG, versions[0])
                version = versions[0]
            for v in versions:
                self.airSDKComboBox.addItem(v)
            self.airSDKComboBox.setCurrentIndex(self.airSDKComboBox.findText(version))
        self.airSDKComboBox.currentIndexChanged.connect(self._handleAirVersionChanged)

        versions = self.mainWindow.listInstalledFlashPlayers()
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

        self.releaseInfoDefaultBtn.clicked.connect(self._handleDefaultReleaseText)
        self.removalsDefaultBtn.clicked.connect(self._handleDefaultReleaseText)
        self.fixesDefaultBtn.clicked.connect(self._handleDefaultReleaseText)
        self.additionsDefaultBtn.clicked.connect(self._handleDefaultReleaseText)
        self.summaryDefaultBtn.clicked.connect(self._handleDefaultReleaseText)

        self.resultsTextBrowser.setReadOnly(True)
        self.compileBtn.clicked.connect(self._handleCompileClick)
        self.compileDebugBtn.clicked.connect(self._handleCompileDebugClick)
        self.packageBtn.clicked.connect(self._handlePackageClick)
        self.runDebugBtn.clicked.connect(self._handleRunDebug)
        self.installApkBtn.clicked.connect(self._handleInstallApk)
        self.installIpaBtn.clicked.connect(self._handleInstallIpa)
        self.logcatDumpBtn.clicked.connect(self._handleGetLogcatDump)
        self.clearLogcatBtn.clicked.connect(self._handleClearLogcat)
        self.flexDebugBtn.clicked.connect(self._handleFlexDebugSession)
        self.deployBuildBtn.clicked.connect(self._handleDeployBuild)
        self.saveDeployBtn.clicked.connect(self._handleSaveDeployInfo)
        self.reloadDeployBtn.clicked.connect(self._handleReloadDeployInfo)
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

        self._settingsEditor = SettingsEditor()
        self._settingsEditor.populate()
        self._updateSettings()

        self.reloadSettingsBtn.clicked.connect(self._handleReloadSettings)
        self.incrementSettingsBtn.clicked.connect(self._handleIncrementSettings)
        self.writeSettingsBtn.clicked.connect(self._handleWriteSettings)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _activateWidgetDisplayImpl
    def _activateWidgetDisplayImpl(self, **kwargs):
        self._reloadDeployText()

#___________________________________________________________________________________________________ _reloadDeployText
    def _reloadDeployText(self):
        settings = SettingsConfig(CompilerDeckEnvironment.projectSettingsPath, pretty=True)
        self._populateDeployText('SUMMARY', self.summaryText, settings)
        self._populateDeployText('ADDITIONS', self.additionsText, settings)
        self._populateDeployText('FIXES', self.fixesText, settings)
        self._populateDeployText('REMOVALS', self.removalsText, settings)
        self._populateDeployText('INFO', self.releaseInfoText, settings)

#___________________________________________________________________________________________________ _populateDeployText
    def _populateDeployText(self, key, target, settings):
        val = settings.get(['DEPLOY', 'STORED', key])
        if val:
            target.setPlainText(val)
            return

        val = settings.get(['DEPLOY', 'DEFAULTS', key])
        if val:
            target.setPlainText(val)
            return

        val = settings.get(['DEPLOY', 'LAST', key])
        if val:
            target.setPlainText(val)

#___________________________________________________________________________________________________ _setCheckState
    def _setCheckState(self, target, value):
        target.setCheckState(QtCore.Qt.Checked if value else QtCore.Qt.Unchecked)

#___________________________________________________________________________________________________ _executeRemoteThread
    def _executeRemoteThread(self, thread, completeCallback = None):
        self.resultsTextBrowser.clear()
        self.log.addPrintCallback(self._handleUpdateResults)
        self.resultsTextBrowser.setFocus()
        self.mainTab.setCurrentWidget(self.resultsTabPage)
        self._toggleInteractivity(False)
        self.refreshGui()

        self._compThread = thread
        thread.logSignal.signal.connect(self._handleUpdateResults)
        if completeCallback is None:
            thread.completeSignal.signal.connect(self._handleRemoteThreadComplete)
        else:
            thread.completeSignal.signal.connect(completeCallback)

        thread.start()

#___________________________________________________________________________________________________ _toggleInteractivity
    def _toggleInteractivity(self, value):
        self.compileBtn.setEnabled(value)
        self.deployBuildBtn.setEnabled(value)
        self.settingsTabPage.setEnabled(value)
        self.descriptorTabPage.setEnabled(value)
        self.utilsTabPage.setEnabled(value)

#___________________________________________________________________________________________________ _updateSettings
    def _updateSettings(self):
        self.prefixLine.setText(self._settingsEditor.prefix)
        self.suffixSpin.setValue(int(self._settingsEditor.suffixInteger))
        self.majorSpin.setValue(int(self._settingsEditor.major))
        self.minorSpin.setValue(int(self._settingsEditor.minor))
        self.revisionSpin.setValue(int(self._settingsEditor.revision))

#___________________________________________________________________________________________________ _executeCompilation
    def _executeCompilation(self, callback):
        self._settingsEditor.setTo(
            prefix=self.prefixLine.text(),
            suffix=self.suffixSpin.value(),
            major=self.majorSpin.value(),
            minor=self.minorSpin.value(),
            revision=self.revisionSpin.value()
        )
        self._settingsEditor.write()

        self._buildSnapshot = dict(
            parent=self,
            versionInfo=self._settingsEditor.toDict(),
            projectPath=CompilerDeckEnvironment.getProjectPath(),
            debug=self.debugCheck.isChecked(),
            live=self.liveCheck.isChecked(),
            airVersion=str(self.airSDKComboBox.currentText()),
            flashVersion=str(self.flashPlayerComboBox.currentText()),
            packageAir=self._package,
            remoteDebug=(not self.remoteDebugComboBox.currentText().lower().startswith('none')),
            usbDebug=(self.remoteDebugComboBox.currentText().lower().startswith('usb')),
            platforms={
                FlexProjectData.NATIVE_PLATFORM:self.desktopPlatformCheck.isChecked(),
                FlexProjectData.AIR_PLATFORM:self.desktopPlatformCheck.isChecked(),
                FlexProjectData.FLASH_PLATFORM:self.webPlatformCheck.isChecked(),
                FlexProjectData.ANDROID_PLATFORM:self.androidPlatformCheck.isChecked(),
                FlexProjectData.IOS_PLATFORM:self.iosPlatformCheck.isChecked()
            }
        )

        self._executeRemoteThread(ANECompileThread(**self._buildSnapshot), callback)

#___________________________________________________________________________________________________ _executeDebugProcess
    def _executeDebugProcess(self):
        self._executeRemoteThread(AirDebugThread(
            parent=self,
            projectPath=CompilerDeckEnvironment.getProjectPath(),
            airVersion=str(self.airSDKComboBox.currentText()),
            flashVersion=str(self.flashPlayerComboBox.currentText()),
        ))

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleCompileDebugClick
    def _handleCompileDebugClick(self):
        self._package = False
        self._executeCompilation(self._handleDebugCompilation)

#___________________________________________________________________________________________________ _handleDebugCompilation
    def _handleDebugCompilation(self, result):
        if result['response'] == 0:
            self._executeDebugProcess()
        else:
            self._handleRemoteThreadComplete(result)

#___________________________________________________________________________________________________ _handleCompileClick
    def _handleCompileClick(self):
        self._package = False
        self._executeCompilation(self._handleCompilationComplete)

#___________________________________________________________________________________________________ _handlePackageClick
    def _handlePackageClick(self):
        self._package = True
        self._executeCompilation(self._handleCompilationComplete)

#___________________________________________________________________________________________________ _handleCompilationComplete
    def _handleCompilationComplete(self, result):
        if self._package and result['response'] == 0:
            self._settingsEditor.logBuild(
                self.desktopPlatformCheck.isChecked(),
                self.androidPlatformCheck.isChecked(),
                self.iosPlatformCheck.isChecked(),
            )
        self._handleRemoteThreadComplete(result)
        self._package = False

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
        self.mainWindow.appConfig.set(
            self._FLASH_PLAYER_VERSION_CFG,
            self.flashPlayerComboBox.currentText()
        )

#___________________________________________________________________________________________________ _handleAirVersionChanged
    def _handleAirVersionChanged(self):
        self.mainWindow.appConfig.set(
            self._AIR_SDK_VERSION_CFG,
            self.airSDKComboBox.currentText()
        )

#___________________________________________________________________________________________________ _handlePackageAirStateChange
    def _handleCheckStateChange(self):
        sender = self.sender()
        prop   = None
        if sender == self.liveCheck:
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
        self._executeDebugProcess()

#___________________________________________________________________________________________________ _handleInstallApk
    def _handleInstallApk(self):
        self._executeRemoteThread(InstallApkThread(
            parent=self,
            projectPath=CompilerDeckEnvironment.getProjectPath(),
        ))

#___________________________________________________________________________________________________ _handleInstallIpa
    def _handleInstallIpa(self):
        self._executeRemoteThread(InstallIpaThread(
            parent=self,
            airVersion=str(self.airSDKComboBox.currentText()),
            projectPath=CompilerDeckEnvironment.getProjectPath()
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

#___________________________________________________________________________________________________ _handleWriteSettings
    def _handleWriteSettings(self):
        sets                = self._settingsEditor
        sets.prefix         = self.prefixLine.text()
        sets.suffixInteger  = self.suffixSpin.value()
        sets.major          = self.majorSpin.value()
        sets.minor          = self.minorSpin.value()
        sets.revision       = self.revisionSpin.value()
        sets.write()
        sets.reset()
        sets.populate()

#___________________________________________________________________________________________________ _handleIncrementSettings
    def _handleIncrementSettings(self):
        self._settingsEditor.populate()
        self._updateSettings()

#___________________________________________________________________________________________________ _handleReloadSettings
    def _handleReloadSettings(self):
        self._settingsEditor.reset()
        self._settingsEditor.populate()
        self._updateSettings()

#___________________________________________________________________________________________________ _handleDeployBuild
    def _handleDeployBuild(self):
        if not self._buildSnapshot:
            print 'No build snapshot to deploy:', self._buildSnapshot
            return

        releaseNotes = dict(
            summary=self.summaryText.toPlainText(),
            additions=self.additionsText.toPlainText(),
            fixes=self.fixesText.toPlainText(),
            removals=self.removalsText.toPlainText(),
            info=self.releaseInfoText.toPlainText())

        self._executeRemoteThread(
            S3DeployerThread(
                parent=self,
                snapshot=self._buildSnapshot,
                sendEmails=self.sendEmailCheck.isChecked(),
                releaseNotes=releaseNotes),
            self._handleDeployResult)

#___________________________________________________________________________________________________ _handleDeployResult
    def _handleDeployResult(self, result):
        if result['response'] == 0:
            settings = SettingsConfig(CompilerDeckEnvironment.projectSettingsPath, pretty=True)
            settings.set(['DEPLOY', 'LAST', 'SUMMARY'], self.summaryText.toPlainText())
            settings.set(['DEPLOY', 'LAST', 'ADDITIONS'], self.additionsText.toPlainText())
            settings.set(['DEPLOY', 'LAST', 'FIXES'], self.fixesText.toPlainText())
            settings.set(['DEPLOY', 'LAST', 'REMOVALS'], self.removalsText.toPlainText())
            settings.set(['DEPLOY', 'LAST', 'INFO'], self.releaseInfoText.toPlainText())
            settings.remove(['DEPLOY', 'STORED'])

        self._handleRemoteThreadComplete(result)

#___________________________________________________________________________________________________ _handleDefaultReleaseText
    def _handleDefaultReleaseText(self):
        btn = self.sender()
        settings = SettingsConfig(CompilerDeckEnvironment.projectSettingsPath, pretty=True)
        if btn == self.summaryDefaultBtn:
            settings.set(['DEPLOY', 'DEFAULTS', 'SUMMARY'], self.summaryText.toPlainText())
        elif btn == self.additionsDefaultBtn:
            settings.set(['DEPLOY', 'DEFAULTS', 'ADDITIONS'], self.additionsText.toPlainText())
        elif btn == self.fixesDefaultBtn:
            settings.set(['DEPLOY', 'DEFAULTS', 'FIXES'], self.fixesText.toPlainText())
        elif btn == self.removalsDefaultBtn:
            settings.set(['DEPLOY', 'DEFAULTS', 'REMOVALS'], self.removalsText.toPlainText())
        elif btn == self.releaseInfoDefaultBtn:
            settings.set(['DEPLOY', 'DEFAULTS', 'INFO'], self.releaseInfoText.toPlainText())

#___________________________________________________________________________________________________ _handleSaveDeployInfo
    def _handleSaveDeployInfo(self):
        settings = SettingsConfig(CompilerDeckEnvironment.projectSettingsPath, pretty=True)
        settings.set(['DEPLOY', 'STORED', 'SUMMARY'], self.summaryText.toPlainText())
        settings.set(['DEPLOY', 'STORED', 'ADDITIONS'], self.additionsText.toPlainText())
        settings.set(['DEPLOY', 'STORED', 'FIXES'], self.fixesText.toPlainText())
        settings.set(['DEPLOY', 'STORED', 'REMOVALS'], self.removalsText.toPlainText())
        settings.set(['DEPLOY', 'STORED', 'INFO'], self.releaseInfoText.toPlainText())

#___________________________________________________________________________________________________ _handleReloadDeployInfo
    def _handleReloadDeployInfo(self):
        self._reloadDeployText()
