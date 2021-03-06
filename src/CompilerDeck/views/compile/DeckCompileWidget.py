# DeckCompileWidget.py
# (C)2013-2014
# Scott Ernst

import os

from PySide import QtGui
from PySide import QtCore

from pyaid.ArgsUtils import ArgsUtils
from pyaid.OsUtils import OsUtils
from pyaid.config.SettingsConfig import SettingsConfig
from pyaid.dict.DictUtils import DictUtils
from pyaid.file.FileUtils import FileUtils
from pyaid.json.JSON import JSON
from pyaid.system.SystemUtils import SystemUtils
from pyaid.time.TimeUtils import TimeUtils

from pyglass.dialogs.PyGlassBasicDialogManager import PyGlassBasicDialogManager
from pyglass.elements.PyGlassElementUtils import PyGlassElementUtils
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
from CompilerDeck.deploy.UploaderThread import UploaderThread
from CompilerDeck.ios.IosSimulatorThread import IosSimulatorThread
from CompilerDeck.views.compile.ExtensionsPane import ExtensionsPane

#___________________________________________________________________________________________________ DeckCompileWidget
from CompilerDeck.views.dialogs.deploy.DeployBuildDialog import DeployBuildDialog


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
    _COMPILE_MODE_CFG         = 'COMPILE_MODE'
    _COMPILE_WEB              = 'COMPILE_WEB'
    _COMPILE_AIR              = 'COMPILE_AIR'
    _COMPILE_NATIVE           = 'COMPILE_NATIVE'
    _COMPILE_ANDROID          = 'COMPILE_ANDROID'
    _COMPILE_IOS              = 'COMPILE_IOS'
    _IOS_INTERP               = 'IOS_INTERP'
    _ADV_TELEMETRY            = 'ADV_TELEMETRY'
    _APPEND_TO_PACKAGE        = 'APPEND_TO_PACKAGE'
    _IOS_SIMULATOR            = 'IOS_SIMULATOR'
    _NATIVE_CAPTIVE_RUNTIME   = 'NATIVE_CAPTIVE_RUNTIME'
    _PAUSE_PACKAGE_STEPS      = 'PAUSE_PACKAGE_STEPS'
    _COMPILE_BEFORE_PACKAGE   = 'COMPILE_BEFORE_PACKAGE'
    _UPLOAD_AFTER_PACKAGE     = 'UPLOAD_AFTER_PACKAGE'

#___________________________________________________________________________________________________ __init__
    def __init__(self, *args, **kwargs):
        """Creates a new instance of DeckCompileWidget."""
        super(DeckCompileWidget, self).__init__(*args, **kwargs)

        self._results           = ''
        self._compThread        = None
        self._buildSnapshot     = None
        self._package           = False
        self._extensionsPane    = ExtensionsPane(self)

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
            version  = self.appConfig.get(self._FLASH_PLAYER_VERSION_CFG)
            if version is None:
                self.appConfig.set(self._FLASH_PLAYER_VERSION_CFG, versions[0])
                version = versions[0]
            for v in versions:
                self.flashPlayerComboBox.addItem(v)
            self.flashPlayerComboBox.setCurrentIndex(self.flashPlayerComboBox.findText(version))
        self.flashPlayerComboBox.currentIndexChanged.connect(self._handleFlashVersionChanged)

        #--- Compile Mode Combo Box INI ---#
        for item in [u'Alpha', u'Beta', u'Pre-Release', u'Release']:
            self.compileModeComboBox.addItem(item)
        compileMode = self.appConfig.get(self._COMPILE_MODE_CFG, u'Debug')
        self.compileModeComboBox.setCurrentIndex(self.compileModeComboBox.findText(compileMode))
        self.compileModeComboBox.currentIndexChanged.connect(self._handleCompileModeChanged)

        debugTypes = [
            u'None',
            u'WiFi Connection',
            u'USB Connection (%s)' % str(FlexProjectData.USB_DEBUG_PORT)]
        for item in debugTypes:
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
        self.resetDeployBtn.clicked.connect(self._handleResetDeployInfo)
        self.simulateBtn.clicked.connect(self._handleSimulateApp)
        self.openSimDocsBtn.clicked.connect(self._handleOpenDocumentsInFinder)
        self.uploadPackagesBtn.clicked.connect(self._handleUploadPackages)
        self.mainTab.setCurrentIndex(0)

        self._checkProperties = dict()
        self._initializeCheck(self.simulatorCheck, self._IOS_SIMULATOR, False)
        self._initializeCheck(self.iosInterpCheck, self._IOS_INTERP, False)
        self._initializeCheck(self.liveCheck, self._LIVE_CFG, False)
        self._initializeCheck(self.webPlatformCheck, self._COMPILE_WEB, True)
        self._initializeCheck(self.airPlatformCheck, self._COMPILE_AIR, True)
        self._initializeCheck(self.nativePlatformCheck, self._COMPILE_NATIVE, True)
        self._initializeCheck(self.androidPlatformCheck, self._COMPILE_ANDROID, True)
        self._initializeCheck(self.iosPlatformCheck, self._COMPILE_IOS, True)
        self._initializeCheck(self.telemetryCheck, self._ADV_TELEMETRY, False)
        self._initializeCheck(self.expandPackageChk, self._APPEND_TO_PACKAGE, False)
        self._initializeCheck(self.packagePauseChk, self._PAUSE_PACKAGE_STEPS, False)
        self._initializeCheck(self.nativeCaptiveChk, self._NATIVE_CAPTIVE_RUNTIME, False)
        self._initializeCheck(self.compileBeforePackageChk, self._COMPILE_BEFORE_PACKAGE, True)
        self._initializeCheck(self.uploadPackageCheck, self._UPLOAD_AFTER_PACKAGE, False)

        self._settingsEditor = SettingsEditor()
        self._settingsEditor.populate()
        self._updateSettings()

        self.reloadSettingsBtn.clicked.connect(self._handleReloadSettings)
        self.incrementSettingsBtn.clicked.connect(self._handleIncrementSettings)
        self.writeSettingsBtn.clicked.connect(self._handleWriteSettings)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: isAlpha
    @property
    def isAlpha(self):
        return self.compileModeComboBox.currentText().lower() == u'alpha'

#___________________________________________________________________________________________________ GS: isBeta
    @property
    def isBeta(self):
        return self.compileModeComboBox.currentText().lower() == u'beta'

#___________________________________________________________________________________________________ GS: isReleaseCandidate
    @property
    def isReleaseCandidate(self):
        return self.compileModeComboBox.currentText().lower() == u'pre-release'

#___________________________________________________________________________________________________ GS: isRelease
    @property
    def isRelease(self):
        return self.compileModeComboBox.currentText().lower() == u'release'

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ executeRemoteThread
    def executeRemoteThread(self, thread, completeCallback =None):
        self._executeRemoteThread(thread, completeCallback=completeCallback)

#___________________________________________________________________________________________________ remoteThreadResult
    def remoteThreadResult(self, event):
        self.log.removePrintCallback(self._handleUpdateResults)
        self._toggleInteractivity(True)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _initializeCheck
    def _initializeCheck(self, checkBox, configValue, defaultValue):
        self._checkProperties[configValue] = checkBox
        self._setCheckState(checkBox, self.parent().appConfig.get(configValue, defaultValue))
        checkBox.stateChanged.connect(self._handleCheckStateChange)

#___________________________________________________________________________________________________ _activateWidgetDisplayImpl
    def _activateWidgetDisplayImpl(self, **kwargs):
        self._buildSnapshot = None
        self._loadBuildSnapshot()
        self._reloadDeployText()

        self._extensionsPane.activate()

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
    def _executeRemoteThread(self, thread, completeCallback =None):
        self.resultsTextBrowser.clear()
        self.log.addPrintCallback(self._handleUpdateResults)
        self.resultsTextBrowser.setFocus()
        self.mainTab.setCurrentWidget(self.resultsTabPage)
        self._toggleInteractivity(False)
        self.refreshGui()

        self._compThread = thread
        if completeCallback is None:
            completeCallback = self._handleRemoteThreadComplete

        thread.execute(
            callback=completeCallback,
            logCallback=self._handleUpdateResults,
            eventCallback=self._handleCompileEvent)

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
        self.microSpin.setValue(int(self._settingsEditor.micro))
        self.revisionSpin.setValue(int(self._settingsEditor.revision))

#___________________________________________________________________________________________________ _executeCompilation
    def _executeCompilation(self, callback, buildSnapshot =None):
        if self._package and self.expandPackageChk.isChecked():
            if buildSnapshot is None:
                if self._buildSnapshot is None:
                    self._loadBuildSnapshot()
            buildSnapshot = self._buildSnapshot
            buildSnapshot['combinedPlatforms'] \
                = self._createPlatformsSnapshot(buildSnapshot['platforms'])
            buildSnapshot['platforms'] = self._createPlatformsSnapshot()
        else:
            self._settingsEditor.setTo(
                prefix=self.prefixLine.text(),
                suffix=self.suffixSpin.value(),
                major=self.majorSpin.value(),
                minor=self.minorSpin.value(),
                micro=self.microSpin.value(),
                revision=self.revisionSpin.value() )
            self._settingsEditor.write(isDebug=self.isAlpha or self.isBeta)

        self._buildSnapshot = self._createBuildSnapshot() if buildSnapshot is None else buildSnapshot

        self._executeRemoteThread(ANECompileThread(
            parent=self,
            pausePackageSteps=self._package and self.packagePauseChk.isChecked(),
            uploadAfterPackage=self._package and self.uploadPackageCheck.isChecked(),
            **self._buildSnapshot), callback)

#___________________________________________________________________________________________________ _executeDebugProcess
    def _executeDebugProcess(self):
        self._executeRemoteThread(AirDebugThread(parent=self, **self._createBuildSnapshot()))

#___________________________________________________________________________________________________ _createPackageSnapshot
    def _createPlatformsSnapshot(self, overrides =None):
        out = dict()
        platforms = {
            FlexProjectData.NATIVE_PLATFORM:self.nativePlatformCheck,
            FlexProjectData.WINDOWS_PLATFORM:self.nativePlatformCheck,
            FlexProjectData.MAC_PLATFORM:self.nativePlatformCheck,
            FlexProjectData.AIR_PLATFORM:self.airPlatformCheck,
            FlexProjectData.FLASH_PLATFORM:self.webPlatformCheck,
            FlexProjectData.ANDROID_PLATFORM:self.androidPlatformCheck,
            FlexProjectData.IOS_PLATFORM:self.iosPlatformCheck }
        for pid, check in platforms.iteritems():
            out[pid] = check.isChecked() or ArgsUtils.get(pid, False, overrides)

        out[FlexProjectData.WINDOWS_PLATFORM] \
            = out[FlexProjectData.WINDOWS_PLATFORM] and OsUtils.isWindows()
        out[FlexProjectData.MAC_PLATFORM] \
            = out[FlexProjectData.MAC_PLATFORM] and OsUtils.isMac()

        return out

#___________________________________________________________________________________________________ _createBuildSnapshot
    def _createBuildSnapshot(self):
        return dict(
            nativeCaptive=self.nativeCaptiveChk.isChecked(),
            iosSimulator=self.simulatorCheck.isChecked(),
            iosInterpreter=self.iosInterpCheck.isChecked(),
            iosAdHoc=self.isReleaseCandidate,
            versionInfo=self._settingsEditor.toDict(),
            projectPath=CompilerDeckEnvironment.getProjectPath(),
            debug=self.isAlpha or self.isBeta,
            telemetry=self.telemetryCheck.isChecked(),
            live=self.liveCheck.isChecked(),
            airVersion=str(self.airSDKComboBox.currentText()),
            flashVersion=str(self.flashPlayerComboBox.currentText()),
            packageAir=self._package,
            compileSwf=self.compileBeforePackageChk.isChecked() or not self._package,
            remoteDebug=(not self.remoteDebugComboBox.currentText().lower().startswith('none')),
            usbDebug=(self.remoteDebugComboBox.currentText().lower().startswith('usb')),
            platformUploads={},
            platforms=self._createPlatformsSnapshot() )

#___________________________________________________________________________________________________ _storeBuildSnapshot
    def _storeBuildSnapshot(self):
        if not self._buildSnapshot:
            return

        snap = dict()
        for n,v in self._buildSnapshot.iteritems():
            if n in ['parent']:
                continue

            snap[n] = v

        settings = SettingsConfig(CompilerDeckEnvironment.projectSettingsPath, pretty=True)
        settings.set(['BUILD', 'LAST_SNAPSHOT'], JSON.asString(snap))

#___________________________________________________________________________________________________ _loadBuildSnapshot
    def _loadBuildSnapshot(self):
        settings = SettingsConfig(CompilerDeckEnvironment.projectSettingsPath, pretty=True)
        snap = settings.get(['BUILD', 'LAST_SNAPSHOT'])
        if snap is None:
            return

        try:
            self._buildSnapshot = JSON.fromString(snap)
        except Exception, err:
            pass

#___________________________________________________________________________________________________ _getLatestBuildSnapshot
    def _getLatestBuildSnapshot(self, override =None):
        if override is not None:
            return override

        if self._buildSnapshot is None:
            self._loadBuildSnapshot()
        return self._buildSnapshot

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleCompileDebugClick
    def _handleCompileDebugClick(self):
        self._package = False
        snap      = self._createBuildSnapshot()
        platforms = snap['platforms']
        platforms[FlexProjectData.IOS_PLATFORM]     = False
        platforms[FlexProjectData.ANDROID_PLATFORM] = False
        platforms[FlexProjectData.AIR_PLATFORM]     = False
        platforms[FlexProjectData.FLASH_PLATFORM]   = False
        platforms[FlexProjectData.NATIVE_PLATFORM]  = False
        platforms[FlexProjectData.MAC_PLATFORM]     = False
        platforms[FlexProjectData.WINDOWS_PLATFORM] = False
        self._executeCompilation(self._handleDebugCompilation, snap)

#___________________________________________________________________________________________________ _handleDebugCompilation
    def _handleDebugCompilation(self, event):
        if event.target.success:
            self._executeDebugProcess()
        else:
            self._handleRemoteThreadComplete(event)

#___________________________________________________________________________________________________ _handleCompileClick
    def _handleCompileClick(self):
        self._package = False
        self._executeCompilation(self._handleCompilationComplete)

#___________________________________________________________________________________________________ _handlePackageClick
    def _handlePackageClick(self):
        self._package = True
        self._executeCompilation(self._handleCompilationComplete)

#___________________________________________________________________________________________________ _handleCompilationComplete
    def _handleCompilationComplete(self, event):
        snap = self._buildSnapshot

        if self._package and event.target.success:

            # If this was an appended package then prior to storing the snapshot the combined
            # platforms should be stored as the result instead of the platforms stored in this
            # particular case
            if 'combinedPlatforms' in snap:
                platforms = snap['combinedPlatforms']
                snap['platforms'] = platforms
                del snap['combinedPlatforms']
            else:
                platforms = snap['platforms']

            # Any package uploads conducted as part of the compilation process should be included
            # in the build snapshot for reference to prevent uploading them again in the future
            output = event.target.output
            if 'urls' in output:
                snap['platformUploads'] = DictUtils.merge(
                    snap['platformUploads'], output['urls'])

            self._storeBuildSnapshot()

            FileUtils.putContents('\t'.join([
                    TimeUtils.getNowDatetime().strftime('[%a %m-%d %H:%M]'),
                    'DSK' if platforms.get(FlexProjectData.AIR_PLATFORM, False) else '---',
                    'AND' if platforms.get(FlexProjectData.ANDROID_PLATFORM, False) else '---',
                    'IOS' if platforms.get(FlexProjectData.IOS_PLATFORM, False) else '---',
                    'WIN' if platforms.get(FlexProjectData.WINDOWS_PLATFORM, False) else '---',
                    'MAC' if platforms.get(FlexProjectData.MAC_PLATFORM, False) else '---',
                    '<<' + snap['versionInfo']['number'] + '>>',
                    '<<' + snap['versionInfo']['label'] + '>>' ]) + '\n',
                self._settingsEditor.buildLogFilePath,
                True )

            self._settingsEditor.reset()
            self._settingsEditor.populate()
            self._updateSettings()

        self._handleRemoteThreadComplete(event)
        self._package = False

#___________________________________________________________________________________________________ _handleRemoteThreadComplete
    def _handleRemoteThreadComplete(self, event):
        self.remoteThreadResult(event)

#___________________________________________________________________________________________________ _handleUpdateResults
    def _handleUpdateResults(self, event):
        value = event.get('message', '')
        tb = self.resultsTextBrowser
        tb.moveCursor(QtGui.QTextCursor.End)
        tb.append(value.replace('\n', '<br />') + '<br />')
        self.refreshGui()

#___________________________________________________________________________________________________ _handleFlashVersionChanged
    def _handleFlashVersionChanged(self):
        self.mainWindow.appConfig.set(
            self._FLASH_PLAYER_VERSION_CFG,
            self.flashPlayerComboBox.currentText() )

#___________________________________________________________________________________________________ _handleAirVersionChanged
    def _handleAirVersionChanged(self):
        self.mainWindow.appConfig.set(
            self._AIR_SDK_VERSION_CFG,
            self.airSDKComboBox.currentText() )

#___________________________________________________________________________________________________ _handlePackageAirStateChange
    def _handleCheckStateChange(self):
        sender = self.sender()
        prop = None
        for key,value in self._checkProperties.iteritems():
            if value != sender:
                continue
            prop = key
            break

        if prop:
            self.owner.appConfig.set(prop, sender.isChecked())

#___________________________________________________________________________________________________ _handleRunDebug
    def _handleRunDebug(self):
        self._executeDebugProcess()

#___________________________________________________________________________________________________ _handleInstallApk
    def _handleInstallApk(self):
        self._executeRemoteThread(InstallApkThread(
            parent=self,
            **self._getLatestBuildSnapshot() ))

#___________________________________________________________________________________________________ _handleInstallIpa
    def _handleInstallIpa(self):
        self._executeRemoteThread(InstallIpaThread(
            parent=self,
            **self._getLatestBuildSnapshot() ))

#___________________________________________________________________________________________________ _handleGetLogcatDump
    def _handleGetLogcatDump(self):
        self._executeRemoteThread(AndroidLogcatThread(
            parent=self,
            mode=AndroidLogcatThread.DUMP_MODE ))

#___________________________________________________________________________________________________ _handleClearLogcat
    def _handleClearLogcat(self):
        self._executeRemoteThread(AndroidLogcatThread(
            parent=self,
            mode=AndroidLogcatThread.CLEAR_MODE ))

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
        sets.micro          = self.microSping.value()
        sets.revision       = self.revisionSpin.value()
        sets.write(self.isAlpha or self.isBeta)
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
        self._getLatestBuildSnapshot()
        if not self._buildSnapshot:
            print 'No build snapshot to deploy:', self._buildSnapshot
            return

        DeployBuildDialog(self.mainWindow, callback=self._handleDeployDialogResult).open()

#___________________________________________________________________________________________________ _handleDeployDialogResult
    def _handleDeployDialogResult(self, dialog):
        widget = dialog.contentWidget

        if widget.canceled:
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
                sendEmails=widget.includeEmails,
                message=widget.buildMessage,
                releaseNotes=releaseNotes),
            self._handleDeployResult)

#___________________________________________________________________________________________________ _handleDeployResult
    def _handleDeployResult(self, event):
        if event.target.success:

            # Any new Urls added by uploads during the deployment should be stored in the build
            # snapshot to save the information for future reference
            self._buildSnapshot['platformUploads'] = DictUtils.merge(
                self._buildSnapshot['platformUploads'], event.target.output['urls'])
            self._storeBuildSnapshot()

            settings = SettingsConfig(CompilerDeckEnvironment.projectSettingsPath, pretty=True)
            settings.set(['DEPLOY', 'LAST', 'SUMMARY'], self.summaryText.toPlainText())
            settings.set(['DEPLOY', 'LAST', 'ADDITIONS'], self.additionsText.toPlainText())
            settings.set(['DEPLOY', 'LAST', 'FIXES'], self.fixesText.toPlainText())
            settings.set(['DEPLOY', 'LAST', 'REMOVALS'], self.removalsText.toPlainText())
            settings.set(['DEPLOY', 'LAST', 'INFO'], self.releaseInfoText.toPlainText())

        self._handleRemoteThreadComplete(event)

#___________________________________________________________________________________________________ _handleResetDeployInfo
    def _handleResetDeployInfo(self):
        result = PyGlassBasicDialogManager.openYesNo(
            parent=self,
            header=u'Reset Deploy Information',
            message=u'Are you sure you want to reset the deployment information fields?',
            defaultToYes=False)
        if not result:
            return

        settings = SettingsConfig(CompilerDeckEnvironment.projectSettingsPath, pretty=True)
        settings.remove(['DEPLOY', 'STORED'])

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

#___________________________________________________________________________________________________ _handleSimulateApp
    def _handleSimulateApp(self):
        self._executeRemoteThread(
            IosSimulatorThread(
                parent=self,
                snapshot=self._getLatestBuildSnapshot()),
            self._handleSimulatorComplete)

#___________________________________________________________________________________________________ _handleSimulateComplete
    def _handleSimulatorComplete(self):
        self._toggleInteractivity(True)

#___________________________________________________________________________________________________ _handleOpenDocumentsInFinder
    def _handleOpenDocumentsInFinder(self):
        snap = self._getLatestBuildSnapshot()
        data = FlexProjectData(**snap)
        path = FileUtils.createPath(
            os.path.expanduser('~'), 'Library', 'Application Support',
            'iPhone Simulator', '7.0.3', 'Applications', data.appId, isDir=True)

        cmd = ['open', '"%s"' % path]

        print 'COMMAND:', cmd
        SystemUtils.executeCommand(cmd)

#___________________________________________________________________________________________________ _handleCompileModeChanged
    def _handleCompileModeChanged(self):
        self.mainWindow.appConfig.set(
            self._COMPILE_MODE_CFG,
            self.compileModeComboBox.currentText() )

        if self.isReleaseCandidate or self.isRelease:
            PyGlassElementUtils.setCheckState(self.packagePauseChk, True)

#___________________________________________________________________________________________________ _handleCompileEvent
    def _handleCompileEvent(self, event):
        if event.id == ANECompileThread.STAGE_COMPLETE:
            response = PyGlassBasicDialogManager.openYesNo(
                self,
                event.get('type') + ' Notification (Paused)',
                event.get('message') + '\nContinue to next step?')
            if response:
                event.target.resumeQueueProcessing()
            else:
                event.target.abortQueueProcessing()

#___________________________________________________________________________________________________ _handleUploadPackages
    def _handleUploadPackages(self):
        if not self._buildSnapshot:
            return

        self._executeRemoteThread(
            UploaderThread(parent=self, snapshot=self._buildSnapshot),
            self._handleUploadResult)

#___________________________________________________________________________________________________ _handleUploadResult
    def _handleUploadResult(self, event):
        self._toggleInteractivity(True)

        if not event.target.success:
            return

        # Add the upload urls to the build snapshot
        output = event.target.output
        if 'urls' in output:
            self._buildSnapshot['platformUploads'] = DictUtils.merge(
                self._buildSnapshot['platformUploads'], output['urls'])

        self._storeBuildSnapshot()
