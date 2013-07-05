# AirCompiler.py
# (C)2012-2013
# Scott Ernst

import os
import re

from pyaid.file.FileUtils import FileUtils

from CompilerDeck.adobe.AdobeSystemCompiler import AdobeSystemCompiler
from CompilerDeck.adobe.air.AirUtils import AirUtils
from CompilerDeck.adobe.flex.FlexProjectData import FlexProjectData
from CompilerDeck.local.ToolsEnvironment import ToolsEnvironment

#___________________________________________________________________________________________________ AirCompiler
class AirCompiler(AdobeSystemCompiler):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _APP_MODIFIER_PATTERN = re.compile(
        '(?P<prefix><application xmlns="http://ns.adobe.com/air/application/)[0-9\.]+(?P<suffix>">)')

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

        if not self._modifyAppXML(sets.appDescriptorPath):
            return False

        cmd.extend([
            ToolsEnvironment.getRootAIRPath(sets.airVersion, 'bin', 'adt.bat', isFile=True),
            '-package'
        ])

        if sets.currentPlatformID in (sets.AIR_PLATFORM, sets.NATIVE_PLATFORM):
            self._addAIRSigningArguments(cmd)
            self._addAIRTargetArguments(cmd)
        else:
            self._addAIRTargetArguments(cmd)
            self._addAirConnectionArguments(cmd)
            self._addAIRSigningArguments(cmd)

        cmd.extend([
            '..' + os.sep + 'dist' + os.sep + sets.targetFilename + '.' + sets.airExtension,
            '..' + os.sep + 'application.xml',
            sets.targetFilename + '.swf'
        ])

        for inc in sets.airIncludes:
            cmd.append(inc)

        if sets.currentPlatformID == FlexProjectData.IOS_PLATFORM:
            launchPath = FileUtils.createPath(sets.targetPath, 'launch')
            if os.path.exists(launchPath) and os.path.isdir(launchPath):
                for item in os.listdir(launchPath):
                    itemPath = FileUtils.createPath(launchPath, item, isFile=True)
                    if not os.path.isfile(itemPath) or not item.endswith('.png'):
                        continue

                    cmd.extend(['-C', '"' + launchPath + '"', itemPath])

        incs = sets.airIncludes + []
        for inc in self._deployPlatformFiles():
            if inc in incs:
                continue
            cmd.append(inc)
            incs.append(inc)

        for inc in self._deployNativeExtensionAssets():
            if inc in incs:
                continue
            cmd.append(inc)
            incs.append(inc)

        self._addAIRNativeExtensionArguments(cmd)

        os.chdir(sets.projectBinPath)
        print 'CMD:', cmd
        if self.executeCommand(cmd, 'PACKAGING AIR FILE: "%s"' % sets.currentPlatformID):
            self._log.write('FAILED: AIR PACKAGING')
            return False

        self._log.write('SUCCESS: AIR PACKAGED')
        return True

#___________________________________________________________________________________________________ _modifyAppXML
    def _modifyAppXML(self, appPath):
        """Doc..."""
        sets = self._settings
        data = FileUtils.getContents(appPath)
        data = AirCompiler._APP_MODIFIER_PATTERN.sub(
            '\g<prefix>' + sets.airVersion + '\g<suffix>', data)
        return FileUtils.putContents(data, appPath)

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

#___________________________________________________________________________________________________ _deployNativeExtensionAssets
    def _deployNativeExtensionAssets(self):
        out  = []
        sets = self._settings

        print 'ANE Includes:', sets.aneIncludes
        if not sets.aneIncludes:
            return []

        if sets.currentPlatformID == FlexProjectData.ANDROID_PLATFORM:
            aneType = 'android'
        elif sets.currentPlatformID == FlexProjectData.IOS_PLATFORM:
            aneType = 'ios'
        else:
            aneType = 'default'

        for ane in sets.aneIncludes:
            aneAssetPath = FileUtils.createPath(
                self.projectPath, 'air', 'ane', ane, aneType, 'assets'
            )
            print 'ANE Asset Path:', aneAssetPath
            if not os.path.exists(aneAssetPath):
                print 'ANE Asset path does not exist:', aneAssetPath
                continue
            print 'ANE asset path:', os.listdir(aneAssetPath)
            for item in os.listdir(aneAssetPath):
                itemPath = FileUtils.createPath(aneAssetPath, item)
                if item == '.svn' or not os.path.isdir(itemPath):
                    continue
                copyResults = FileUtils.mergeCopy(
                    itemPath,
                    FileUtils.createPath(sets.targetPath, item),
                    overwriteExisting=False
                )
                self._copyMerges.append(copyResults)
                out.append(item)

        print 'ANE OUT:', out
        return out

#___________________________________________________________________________________________________ _deployPlatformFiles
    def _deployPlatformFiles(self):
        result = AirUtils.deployPlatformFiles(self._settings)
        self._copyMerges += result['merges']
        return result['dirs']

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

