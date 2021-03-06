# FlexProjectData.py
# (C)2012-2013
# Scott Ernst

import os

from pyaid.ArgsUtils import ArgsUtils
from pyaid.OsUtils import OsUtils
from pyaid.aws.s3.S3Bucket import S3Bucket
from pyaid.file.FileUtils import FileUtils

from CompilerDeck.adobe.air.AirUtils import AirUtils
from CompilerDeck.adobe.shared.ProjectData import ProjectData

#___________________________________________________________________________________________________ FlexProjectData
class FlexProjectData(ProjectData):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    FLASH_PLATFORM      = 'FLASH'
    AIR_PLATFORM        = 'AIR'
    DEFAULT_PLATFORM    = 'DEFAULT'
    NATIVE_PLATFORM     = 'NATIVE'
    WINDOWS_PLATFORM    = 'WINDOWS'
    MAC_PLATFORM        = 'MAC'
    ANDROID_PLATFORM    = 'ANDROID'
    IOS_PLATFORM        = 'IOS'
    USB_DEBUG_PORT      = '7936'

#___________________________________________________________________________________________________ __init__
    def __init__(self,  projectPath, **kwargs):
        """Creates a new instance of ClassTemplate."""
        ProjectData.__init__(self, projectPath=projectPath, **kwargs)

        self.iosSimulatorSdkPath = '/Applications/Xcode.app/Contents/Developer/Platforms/' \
            + 'iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator7.0.sdk'

        self.nativeCaptiveRuntime = ArgsUtils.get('nativeCaptive', False, kwargs)
        self.advancedTelemetry    = ArgsUtils.get('telemetry', False, kwargs)
        self.iosAdHoc             = ArgsUtils.get('iosAdHoc', False, kwargs)
        self.platformUploads      = ArgsUtils.getAsDict('platformUploads', kwargs)

        self._currentPlatformID = None
        self._iosInterpreter    = ArgsUtils.get('iosInterpreter', False, kwargs)
        self._iosSimulator      = ArgsUtils.get('iosSimulator', False, kwargs)
        self._live              = ArgsUtils.get('live', False, kwargs)
        self._compileSwf        = ArgsUtils.get('compileSwf', True, kwargs)
        self._packageAir        = ArgsUtils.get('packageAir', False, kwargs)
        self._quickCompile      = ArgsUtils.get('quickCompile', False, kwargs)
        self._usbDebug          = ArgsUtils.get('usbDebug', False, kwargs)
        self._versionInfo       = ArgsUtils.getAsDict('versionInfo', kwargs)
        self._platforms         = ArgsUtils.getAsDict('platforms', kwargs)
        self.remoteDebug        = ArgsUtils.get('remoteDebug', self._usbDebug, kwargs)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: isPlatformUploaded
    @property
    def isPlatformUploaded(self):
        return self._currentPlatformID in self.platformUploads

#___________________________________________________________________________________________________ GS: compileSwf
    @property
    def compileSwf(self):
        return self._compileSwf or not self._packageAir

#___________________________________________________________________________________________________ GS: isBeta
    @property
    def isBeta(self):
        return self.iosAdHoc and not self.debug

#___________________________________________________________________________________________________ GS: useSimulator
    @property
    def useSimulator(self):
        return self._iosSimulator

#___________________________________________________________________________________________________ GS: isIOS
    @property
    def isIOS(self):
        return self._currentPlatformID == self.IOS_PLATFORM

#___________________________________________________________________________________________________ GS: isAndroid
    @property
    def isAndroid(self):
        return self._currentPlatformID == self.ANDROID_PLATFORM

#___________________________________________________________________________________________________ GS: isNative
    @property
    def isNative(self):
        return self.isDesktop and self._currentPlatformID in [
            self.NATIVE_PLATFORM,
            self.MAC_PLATFORM,
            self.WINDOWS_PLATFORM]

#___________________________________________________________________________________________________ GS: isDesktop
    @property
    def isDesktop(self):
        return not self.isIOS and not self.isAndroid

#___________________________________________________________________________________________________ GS: buildTypeFolderName
    @property
    def buildTypeFolderName(self):
        return 'debug' if self._debug else 'release'

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
               self._versionInfo.get('micro', u'0') + u'.' + \
               self._versionInfo.get('revision', u'0')

#___________________________________________________________________________________________________ GS: platformBinPath
    @property
    def platformBinPath(self):
        ptype = self.buildTypeFolderName

        if self.isNative:
            platform = 'win' if OsUtils.isWindows() else 'mac'
            return FileUtils.createPath(
                self.platformProjectPath,
                'bin', 'native', platform, ptype, isDir=True)

        return FileUtils.createPath(self.platformProjectPath, 'bin', ptype, isDir=True)

#___________________________________________________________________________________________________ GS: platformDistributionPath
    @property
    def platformDistributionPath(self):
        ptype = self.buildTypeFolderName

        if self.isNative:
            platform = 'win' if OsUtils.isWindows() else 'mac'
            return FileUtils.createPath(
                self.platformProjectPath,
                'dist', 'native', platform, ptype, isDir=True)

        return FileUtils.createPath(self.platformProjectPath, 'dist', ptype, isDir=True)

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

#___________________________________________________________________________________________________ GS: appId
    @property
    def appId(self):
        """The application identifier"""
        out = self.getSetting('APP_ID', None)
        if out is None:
            return out
        return out + self.getSetting('APP_SUFFIX', u'')

#___________________________________________________________________________________________________ GS: certificate
    @property
    def certificate(self):
        """Returns the absolute path to the certificate file needed for packaging."""
        certPaths = [
            FileUtils.createPath(
                self.platformProjectPath, 'cert', self.buildTypeFolderName, isDir=True),
            FileUtils.createPath(self.platformProjectPath, 'cert', isDir=True) ]

        for certPath in certPaths:
            if not os.path.exists(certPath):
                continue

            certFileName = self.getSetting('CERTIFICATE')
            if certFileName is None:
                for path in FileUtils.getFilesOnPath(certPath):
                    if path.endswith('.p12'):
                        return path
                continue

            certFileName = certFileName.replace('\\', '/').strip('/').split('/')
            certPath     = FileUtils.createPath(certPath, certFileName, isFile=True)

            if not os.path.exists(certPath) and os.path.exists(certPath + '.p12'):
                certPath += '.p12'

            if os.path.exists(certPath):
                return certPath

        return None

#___________________________________________________________________________________________________ GS: certificatePassword
    @property
    def certificatePassword(self):
        return self.getSetting('CERT_PASSWORD', '')

#___________________________________________________________________________________________________ GS: appleProvisioningProfile
    @property
    def appleProvisioningProfile(self):
        if self._currentPlatformID != self.IOS_PLATFORM:
            return None

        certPaths = [
            FileUtils.createPath(
                self.platformProjectPath, 'cert', self.buildTypeFolderName, isDir=True),
            FileUtils.createPath(self.platformProjectPath, 'cert', isDir=True) ]

        if self.iosAdHoc:
            certPaths.insert(0, FileUtils.createPath(
                self.platformProjectPath, 'cert', 'adhoc', isDir=True))

        for certPath in certPaths:
            if not os.path.exists(certPath):
                continue

            filename = self.getSetting('PROVISIONING_PROFILE', None)
            if filename is None:
                for path in FileUtils.getFilesOnPath(certPath):
                    if path.endswith('.mobileprovision'):
                        return path
                continue

            filename = filename.replace('\\', '/').strip('/').split('/')
            path     = FileUtils.createPath(certPath, filename, isFile=True)
            if not os.path.exists(path) and os.path.exists(path + '.mobileprovision'):
                path += '.mobileprovision'

            if os.path.exists(path):
                return path

        return None

#___________________________________________________________________________________________________ GS: airExtension
    @property
    def airExtension(self):
        if self.currentPlatformID == FlexProjectData.IOS_PLATFORM:
            return 'ipa'
        elif self.currentPlatformID == FlexProjectData.ANDROID_PLATFORM:
            return 'apk'
        elif self.currentPlatformID == FlexProjectData.NATIVE_PLATFORM:
            return 'exe' if OsUtils.isWindows() else 'dmg'
        elif self._currentPlatformID == FlexProjectData.WINDOWS_PLATFORM:
            return 'exe'
        elif self._currentPlatformID == FlexProjectData.MAC_PLATFORM:
            return 'dmg'

        return 'air'

#___________________________________________________________________________________________________ GS: airIncludes
    @property
    def airIncludes(self):
        return self.getSetting('AIR_INCLUDES', [])

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
                if self._iosSimulator:
                    return 'ipa-debug-interpreter-simulator'
                elif self.remoteDebug:
                    return 'ipa-debug-interpreter' if self._iosInterpreter else 'ipa-debug'
                else:
                    return 'ipa-test-interpreter' if self._iosInterpreter else 'ipa-test'
            else:
                return 'ipa-test-interpreter-simulator' if self._iosSimulator else 'ipa-app-store'
        elif self.isNative:
            return 'bundle' if self.nativeCaptiveRuntime else 'native'

        return 'air'

#___________________________________________________________________________________________________ GS: swcIncludes
    @property
    def swcIncludes(self):
        return self.getSetting('SWC_INCLUDES', [])

#___________________________________________________________________________________________________ GS: aneIncludes
    @property
    def aneIncludes(self):
        return self.getSetting('ANE_INCLUDES', [])

#___________________________________________________________________________________________________ GS: contentTargetFilename
    @property
    def contentTargetFilename(self):
        return self.getSetting('FILENAME', 'application').replace(' ', '_')

#___________________________________________________________________________________________________ GS: targetFilename
    @property
    def targetFilename(self):
        return self.getSetting('FILENAME')

#___________________________________________________________________________________________________ GS: targetFilePath
    @property
    def targetFilePath(self):
        return FileUtils.createPath(
            self.platformDistributionPath, self.contentTargetFilename + '.' + self.airExtension)

#___________________________________________________________________________________________________ GS: platforms
    @property
    def platforms(self):
        return self.getSetting('PLATFORMS', [])

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

#___________________________________________________________________________________________________ createBucket
    def createBucket(self, groupKey ='S3'):
        return S3Bucket(
            self.getSetting([groupKey, 'BUCKET']),
            self.getSetting([groupKey, 'AWS_ID']),
            self.getSetting([groupKey, 'AWS_SECRET']))

#___________________________________________________________________________________________________ updateApplicationConfigFile
    def updateApplicationConfigFile(self, iconDefs =None):
        if not AirUtils.updateDescriptorNamespace(self.appDescriptorPath, self.airVersion):
            return False

        appFilename     = self.targetFilename
        contentFilename = self.contentTargetFilename
        if appFilename and not AirUtils.updateAppFilename(self.appDescriptorPath, appFilename, contentFilename):
            return False

        appId = self.appId
        if appId and not AirUtils.updateAppId(self.appDescriptorPath, appId):
            return False

        if iconDefs and not AirUtils.updateAppIconList(self.appDescriptorPath, iconDefs):
            return False

        return True

#___________________________________________________________________________________________________ isPlatformActive
    def isPlatformActive(self, platformId):
        return self.hasPlatform(platformId) and self.platformSelection.get(platformId, False)

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
        return True

#___________________________________________________________________________________________________ getFlashVersion
    def getFlashVersion(self, airPath):
        if self.currentPlatformID == FlexProjectData.FLASH_PLATFORM:
            return self.flashVersion

        playersPath = FileUtils.createPath(
            airPath, self.airVersion, 'frameworks', 'libs', 'player', isDir=True)

        playerVersion = None
        for item in os.listdir(playersPath):
            itemPath = FileUtils.createPath(playersPath, item, isDir=True)
            if not os.path.exists(itemPath) or not os.path.isdir(itemPath):
                continue

            try:
                versionValue = float(item)
            except Exception, err:
                continue

            if playerVersion is None or versionValue > float(playerVersion):
                playerVersion = item

        if playerVersion is None:
            return self.flashVersion

        return playerVersion
