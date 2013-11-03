# AirCompiler.py
# (C)2012-2013
# Scott Ernst

import os

from pyaid.file.FileUtils import FileUtils

from pyglass.app.PyGlassEnvironment import PyGlassEnvironment

from CompilerDeck.adobe.AdobeSystemCompiler import AdobeSystemCompiler
from CompilerDeck.adobe.air.AirUtils import AirUtils
from CompilerDeck.adobe.flex.FlexProjectData import FlexProjectData

#___________________________________________________________________________________________________ AirCompiler
class AirCompiler(AdobeSystemCompiler):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S



#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _compileImpl
    def _compileImpl(self):
        """Doc..."""
        if not self._settings.packageAir:
            return True

        cmd  = []
        sets = self._settings

        # Check to see if the app descriptor file exists. If no descriptor exists the target
        # cannot be compiled and the process should be aborted in failure.
        if not os.path.exists(sets.appDescriptorPath):
            self._log.write('ERROR: No app file found at: ' + sets.appDescriptorPath)
            return False

        if PyGlassEnvironment.isWindows:
            adtCommand = 'adt.bat'
        else:
            adtCommand = 'adt'

        # Adobe packager adt command path
        cmd.extend([
            self._owner.mainWindow.getRootAIRPath(sets.airVersion, 'bin', adtCommand, isFile=True),
            '-package' ])

        print sets.currentPlatformID, '|', sets.isDesktop, sets.isNative, sets.isAndroid, sets.isIOS

        # Add platform specific command flags
        if sets.isDesktop:
            self._addAIRSigningArguments(cmd)
            self._addAIRTargetArguments(cmd)
        else:
            self._addAIRTargetArguments(cmd)
            self._addAirConnectionArguments(cmd)
            self._addAIRSigningArguments(cmd)

        # Create the distribution path where the packaged output will reside
        distPath = sets.platformDistributionPath
        if not os.path.exists(distPath):
            os.makedirs(distPath)

        # The absolute path to the packaging target file
        targetPath = FileUtils.createPath(
            distPath, sets.contentTargetFilename + '.' + sets.airExtension, isFile=True, noTail=True)

        # Remove previous packaging target files
        if os.path.exists(targetPath):
            os.remove(targetPath)

        cmd.extend([
            '"%s"' % targetPath,
            '"%s"' % FileUtils.createPath(sets.platformProjectPath, 'application.xml', isFile=True),
            '"%s"' % (sets.contentTargetFilename + '.swf') ])

        if sets.isIOS and sets.useSimulator:
            cmd.extend(['-platformsdk', '"%s"' % sets.iosSimulatorSdkPath])

        # Deploy external includes
        deployResults = AirUtils.deployExternalIncludes(sets)
        self._copyMerges.extend(deployResults['merges'])
        cmd.extend(deployResults['itemNames'])

        self._addAIRNativeExtensionArguments(cmd)

        # Deploy iOS launch images
        if sets.currentPlatformID == FlexProjectData.IOS_PLATFORM:
            launchPath = FileUtils.createPath(sets.platformProjectPath, 'launch', isDir=True, noTail=True)
            if os.path.exists(launchPath) and os.path.isdir(launchPath):
                for item in os.listdir(launchPath):
                    itemPath = FileUtils.createPath(launchPath, item, isFile=True)
                    if os.path.isfile(itemPath) and item.endswith('.png'):
                        cmd.extend(['-C', '"%s"' % launchPath, '"%s"' % itemPath])

        # Update the application descriptor file with all settings specific to this build
        if not sets.updateApplicationConfigFile(deployResults['icons']):
            self._log.write([
                'ERROR: Unable to update the application descriptor file',
                'PATH: ' + sets.appDescriptorPath,
                'VERSION: ' + sets.airVersion,
                'ID: ' + sets.appId ])
            return False

        # Execute packaging process
        os.chdir(sets.platformBinPath)
        print 'AIR COMPILE COMMAND:\n', cmd
        if self.executeCommand(cmd, 'PACKAGING AIR FILE: "%s"' % sets.currentPlatformID):
            self._log.write('FAILED: AIR PACKAGING')
            return False

        self._log.write('SUCCESS: AIR PACKAGED')
        return True

#___________________________________________________________________________________________________ addAIRTargetArguments
    def _addAIRTargetArguments(self, cmd):
        cmd.extend(['-target', self._settings.airTargetType])

#___________________________________________________________________________________________________ _addAIRSigningArguments
    def _addAIRSigningArguments(self, cmd):
        sets = self._settings
        cmd.extend([
            '-storetype', 'pkcs12', '-keystore', sets.certificate,
            '-storepass', sets.certificatePassword ])

        # Add Apple provisioning profile target
        if sets.currentPlatformID == FlexProjectData.IOS_PLATFORM:
            cmd.extend(['-provisioning-profile', sets.appleProvisioningProfile])

#___________________________________________________________________________________________________ _addAirConnectionArguments
    def _addAirConnectionArguments(self, cmd):
        # If debug allow wifi or usb remote debugging.
        sets = self._settings
        if sets.remoteDebug:
            if sets.usbDebugPort:
                if sets.currentPlatformID == FlexProjectData.IOS_PLATFORM:
                    cmd.extend(['-listen', '16000'])
                else:
                    cmd.extend(['-listen', sets.usbDebugPort])
            elif sets.ipAddress:
                cmd.extend(['-connect', sets.ipAddress])

#___________________________________________________________________________________________________ _addAIRNativeExtensionArguments
    def _addAIRNativeExtensionArguments(self, cmd):
        sets = self._settings
        if not sets.aneIncludes:
            return

        for ane in sets.aneIncludes:
            cmd.extend(['-extdir', FileUtils.createPath(sets.projectPath, 'air', 'ane', ane)])

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __unicode__
    def __unicode__(self):
        return unicode(self.__str__())

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s>' % self.__class__.__name__

