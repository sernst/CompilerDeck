# AirCompiler.py
# (C)2012-2013
# Scott Ernst

import os

from pyaid.file.FileUtils import FileUtils

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

        if not os.path.exists(sets.appDescriptorPath):
            self._log.write('ERROR: No app file found at: ' + sets.appDescriptorPath)
            return False

        if not AirUtils.updateDescriptorNamespace(sets.appDescriptorPath, sets.airVersion):
            self._log.write([
                'ERROR: Unable to update the application descriptor file namespace version',
                'PATH: ' + sets.appDescriptorPath,
                'VERSION: ' + sets.airVersion
            ])
            return False

        cmd.extend([
            self._owner.mainWindow.getRootAIRPath(sets.airVersion, 'bin', 'adt.bat', isFile=True),
            '-package'
        ])

        if sets.currentPlatformID in (sets.AIR_PLATFORM, sets.NATIVE_PLATFORM):
            self._addAIRSigningArguments(cmd)
            self._addAIRTargetArguments(cmd)
        else:
            self._addAIRTargetArguments(cmd)
            self._addAirConnectionArguments(cmd)
            self._addAIRSigningArguments(cmd)

        distPath = sets.platformDistributionPath
        if not os.path.exists(distPath):
            os.makedirs(distPath)

        targetPath = FileUtils.createPath(
            distPath, sets.targetFilename + '.' + sets.airExtension, isFile=True)
        # Remove previous builds
        if os.path.exists(targetPath):
            os.remove(targetPath)

        cmd.extend([
            targetPath,
            FileUtils.createPath(sets.platformProjectPath, 'application.xml', isFile=True),
            sets.targetFilename + '.swf'
        ])

        # Adds the launch display images for iOS compilation if they exist
        if sets.currentPlatformID == FlexProjectData.IOS_PLATFORM:
            launchPath = FileUtils.createPath(sets.platformProjectPath, 'launch')
            if os.path.exists(launchPath) and os.path.isdir(launchPath):
                for item in os.listdir(launchPath):
                    itemPath = FileUtils.createPath(launchPath, item, isFile=True)
                    if os.path.isfile(itemPath) and item.endswith('.png'):
                        cmd.extend(['-C', '"' + launchPath + '"', itemPath])

        results = AirUtils.deployExternalIncludes(sets)
        self._copyMerges.extend(results['merges'])
        cmd.extend(results['itemNames'])

        self._addAIRNativeExtensionArguments(cmd)

        os.chdir(sets.platformBinPath)
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
            '-storepass', sets.certificatePassword
        ])

        # Add Apple provisioning profile target
        if sets.currentPlatformID == FlexProjectData.IOS_PLATFORM:
            cmd.extend(['-provisioning-profile', sets.appleProvisioningProfile])

#___________________________________________________________________________________________________ _addAirConnectionArguments
    def _addAirConnectionArguments(self, cmd):
        # If debug allow wifi or usb remote debugging.
        sets = self._settings
        if sets.remoteDebug:
            if sets.usbDebugPort:
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

