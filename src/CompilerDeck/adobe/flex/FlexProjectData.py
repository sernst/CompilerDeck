# FlexProjectData.py
# (C)2012-2013
# Scott Ernst

import os

from pyaid.ArgsUtils import ArgsUtils
from pyaid.file.FileUtils import FileUtils

from pyglass.app.PyGlassEnvironment import PyGlassEnvironment

from CompilerDeck.adobe.shared.ProjectData import ProjectData

#___________________________________________________________________________________________________ FlexProjectData
class FlexProjectData(ProjectData):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    FLASH_PLATFORM      = 'FLASH'
    AIR_PLATFORM        = 'AIR'
    NATIVE_PLATFORM     = 'NATIVE'
    ANDROID_PLATFORM    = 'ANDROID'
    IOS_PLATFORM        = 'IOS'
    USB_DEBUG_PORT      = '7936'

#___________________________________________________________________________________________________ __init__
    def __init__(self,  projectPath, **kwargs):
        """Creates a new instance of ClassTemplate."""
        ProjectData.__init__(self, projectPath=projectPath, **kwargs)

        self.advancedTelemetry  = ArgsUtils.get('telemetry', False, kwargs)

        self._currentPlatform   = None
        self._currentPlatformID = None
        self._iosInterpreter    = ArgsUtils.get('iosInterpreter', False, kwargs)
        self._live              = ArgsUtils.get('live', False, kwargs)
        self._packageAir        = ArgsUtils.get('packageAir', False, kwargs)
        self._quickCompile      = ArgsUtils.get('quickCompile', False, kwargs)
        self._usbDebug          = ArgsUtils.get('usbDebug', False, kwargs)
        self.remoteDebug        = ArgsUtils.get('remoteDebug', self._usbDebug, kwargs)
        self._versionInfo       = ArgsUtils.getAsDict('versionInfo', kwargs)
        self._platforms         = ArgsUtils.getAsDict('platforms', kwargs)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: platformSelection
    @property
    def platformSelection(self):
        return self._platforms

#___________________________________________________________________________________________________ GS: versionInfo
    @property
    def versionInfo(self):
        return self._versionInfo

#___________________________________________________________________________________________________ GS: versionInfoLabel
    @property
    def versionInfoLabel(self):
        return  self._versionInfo.get('prefix', u'') + u'-' + \
                self._versionInfo.get('date', u'???') + u'-' + \
                self._versionInfo.get('suffix', u'1')

#___________________________________________________________________________________________________ GS: versionInfoNumber
    @property
    def versionInfoNumber(self):
        return self._versionInfo.get('major', u'0') + u'.' + \
               self._versionInfo.get('minor', u'0') + u'.' + \
               self._versionInfo.get('revision', u'0')

#___________________________________________________________________________________________________ GS: platformBinPath
    @property
    def platformBinPath(self):
        return FileUtils.createPath(self.platformProjectPath, 'bin', isDir=True)

#___________________________________________________________________________________________________ GS: platformDistributionPath
    @property
    def platformDistributionPath(self):
        return FileUtils.createPath(self.platformProjectPath, 'dist', isDir=True)

#___________________________________________________________________________________________________ GS: externalIncludesPath
    @property
    def externalIncludesPath(self):
        return FileUtils.createPath(self.projectPath, 'includes', isDir=True)

#___________________________________________________________________________________________________ GS: platformExternalIncludesPath
    @property
    def platformExternalIncludesPath(self):
        pp = self.platformProjectPath
        if pp == self.projectPath:
            return None
        return FileUtils.createPath(self.platformProjectPath, 'includes', isDir=True)

#___________________________________________________________________________________________________ GS: appDescriptorPath
    @property
    def appDescriptorPath(self):
        return FileUtils.createPath(self.platformProjectPath, 'application.xml', isFile=True)

#___________________________________________________________________________________________________ GS: platformProjectPath
    @property
    def platformProjectPath(self):
        """The root project path for the currently active platform."""
        pid = self._currentPlatformID
        if pid == self.ANDROID_PLATFORM:
            return FileUtils.createPath(self.projectPath, 'android', isDir=True)
        elif pid == self.IOS_PLATFORM:
            return FileUtils.createPath(self.projectPath, 'ios', isDir=True)
        return self.projectPath

#___________________________________________________________________________________________________ GS: usbDebugPort
    @property
    def usbDebugPort(self):
        return FlexProjectData.USB_DEBUG_PORT if self._usbDebug else None

#___________________________________________________________________________________________________ GS: certificate
    @property
    def certificate(self):
        """Returns the absolute path to the certificate file needed for packaging."""
        certPath     = FileUtils.createPath(self.platformProjectPath, 'cert', isDir=True)
        certFileName = self.getSetting('CERTIFICATE', None)
        if certFileName is None:
            for path in FileUtils.getFilesOnPath(certPath):
                if path.endswith('.p12'):
                    return path
            return None

        certFileName = certFileName.replace('\\', '/').strip('/').split('/')
        certPath = FileUtils.createPath(certPath, certFileName, isFile=True)
        if not os.path.exists(certPath) and os.path.exists(certPath + '.p12'):
            certPath += '.p12'
        return certPath

#___________________________________________________________________________________________________ GS: certificatePassword
    @property
    def certificatePassword(self):
        return self.getSetting('CERT_PASSWORD', '')

#___________________________________________________________________________________________________ GS: appleProvisioningProfile
    @property
    def appleProvisioningProfile(self):
        if self._currentPlatformID != self.IOS_PLATFORM:
            return None

        certPath = FileUtils.createPath(self.platformProjectPath, 'cert', isDir=True)
        filename = self.getSetting('PROVISIONING_PROFILE', None)
        if filename is None:
            for path in FileUtils.getFilesOnPath(certPath):
                if path.endswith('.mobileprovision'):
                    return path
            return None

        filename = filename.replace('\\', '/').strip('/').split('/')
        path     = FileUtils.createPath(certPath, filename, isFile=True)
        if not os.path.exists(path) and os.path.exists(path + '.mobileprovision'):
            path += '.mobileprovision'
        return path

#___________________________________________________________________________________________________ GS: airExtension
    @property
    def airExtension(self):
        if self.currentPlatformID == FlexProjectData.IOS_PLATFORM:
            return 'ipa'
        elif self.currentPlatformID == FlexProjectData.ANDROID_PLATFORM:
            return 'apk'
        elif self.currentPlatformID == FlexProjectData.NATIVE_PLATFORM:
            return 'exe' if PyGlassEnvironment.isWindows else 'dmg'

        return 'air'

#___________________________________________________________________________________________________ GS: airIncludes
    @property
    def airIncludes(self):
        out = self.getSetting('AIR_INCLUDES', [])
        if isinstance(out, dict):
            out = out['DEBUG' if self.debug else 'RELEASE']
        return out

#___________________________________________________________________________________________________ GS: airTargetType
    @property
    def airTargetType(self):
        if self.currentPlatformID == FlexProjectData.ANDROID_PLATFORM:
            if self.debug:
                return 'apk-debug'
            else:
                return 'apk-captive-runtime'
        elif self.currentPlatformID == FlexProjectData.IOS_PLATFORM:
            if self.debug:
                if self.remoteDebug:
                    return 'ipa-debug-interpreter' if self._iosInterpreter else 'ipa-debug'
                else:
                    return 'ipa-test-interpreter' if self._iosInterpreter else 'ipa-test'
            else:
                return 'ipa-app-store'
        elif self.currentPlatformID == FlexProjectData.NATIVE_PLATFORM:
            return 'native'

        return 'air'

#___________________________________________________________________________________________________ GS: swcIncludes
    @property
    def swcIncludes(self):
        return self.getSetting('SWC_INCLUDES', [])

#___________________________________________________________________________________________________ GS: aneIncludes
    @property
    def aneIncludes(self):
        return self.getSetting('ANE_INCLUDES', [])

#___________________________________________________________________________________________________ GS: targetFilename
    @property
    def targetFilename(self):
        return self.getSetting('FILENAME', '')

#___________________________________________________________________________________________________ GS: targetFilePath
    @property
    def targetFilePath(self):
        return FileUtils.createPath(
            self.platformDistributionPath, self.targetFilename + '.' + self.airExtension)

#___________________________________________________________________________________________________ GS: platforms
    @property
    def platforms(self):
        return self.getSetting('PLATFORMS', [])

#___________________________________________________________________________________________________ GS: currentPlatform
    @property
    def currentPlatform(self):
        return self._currentPlatform

#___________________________________________________________________________________________________ GS: currentPlatformID
    @property
    def currentPlatformID(self):
        return self._currentPlatformID

#___________________________________________________________________________________________________ GS: packageAir
    @property
    def packageAir(self):
        return self._packageAir

#___________________________________________________________________________________________________ GS: live
    @property
    def live(self):
        return self._live

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ hasPlatform
    def hasPlatform(self, platformID):
        if isinstance(platformID, list):
            for pid in platformID:
                if pid in self.platforms:
                    return True
            return False

        return platformID in self.platforms

#___________________________________________________________________________________________________ setPlatform
    def setPlatform(self, platformID):
        if not self.hasPlatform(platformID):
            return False
        self._currentPlatformID = platformID
        self.overrideSettings   = self.platforms[platformID]
