# SWCCompiler.py
# (C)2012-2014
# Scott Ernst

import os
import zipfile

from pyaid.file.FileUtils import FileUtils
from pyaid.system.SystemUtils import SystemUtils
from pyglass.app.PyGlassEnvironment import PyGlassEnvironment

from CompilerDeck.adobe.AdobeSystemCompiler import AdobeSystemCompiler
from CompilerDeck.adobe.flex.FlexProjectData import FlexProjectData
from CompilerDeck.adobe.shared.FlashUtils import FlashUtils

#___________________________________________________________________________________________________ SWCCompiler
class SWCCompiler(AdobeSystemCompiler):

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, owner, settings, **kwargs):
        super(SWCCompiler, self).__init__(owner, settings, **kwargs)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _compileImpl
    def _compileImpl(self):

        sets         = self._settings
        airPath      = self._owner.mainWindow.getRootAIRPath()
        commandFile  = 'acompc.bat' if PyGlassEnvironment.isWindows else 'acompc'
        isDefault    = sets.currentPlatformID == FlexProjectData.DEFAULT_PLATFORM
        isWindows    = sets.currentPlatformID == FlexProjectData.WINDOWS_PLATFORM
        isMac        = sets.currentPlatformID == FlexProjectData.MAC_PLATFORM
        isAndroid    = sets.currentPlatformID == FlexProjectData.ANDROID_PLATFORM
        isIOS        = sets.currentPlatformID == FlexProjectData.IOS_PLATFORM
        flashVersion = sets.getFlashVersion(self._owner.mainWindow.getRootAIRPath())

        libPath = FileUtils.createPath(
            sets.projectPath, sets.getSetting('LIB_PATH', 'lib'), isDir=True)
        if not os.path.exists(libPath):
            os.makedirs(libPath)

        sourcePath = FileUtils.createPath(
                sets.projectPath, sets.getSetting('SOURCE_PATH', 'src'), isDir=True)
        if not os.path.exists(sourcePath):
            os.makedirs(sourcePath)

        cmd = [
            FileUtils.createPath(airPath, sets.airVersion, 'bin', commandFile, isFile=True),
            '-library-path+="%s"' % libPath,
            '--source-path+="%s"' % sourcePath,
            '-target-player=' + flashVersion,
            '-swf-version=' + str(FlashUtils.convertFlashToSwfVersion(flashVersion)) ]

        cmd.extend([
            self._getBooleanDefinition('DEFAULT', isDefault),
            self._getBooleanDefinition('DESKTOP', isMac or isWindows),
            self._getBooleanDefinition('WINDOWS', isWindows),
            self._getBooleanDefinition('MAC', isMac),
            self._getBooleanDefinition('IOS', isIOS),
            self._getBooleanDefinition('ANDROID', isAndroid),
            self._getStringVarDefinition('ID', sets.getSetting('ID', '')),
            self._getStringVarDefinition('VERSION_NUMBER_MAJOR', sets.versionInfo.get('major', '0')),
            self._getStringVarDefinition('VERSION_NUMBER_MINOR', sets.versionInfo.get('minor', '0')),
            self._getStringVarDefinition('VERSION_NUMBER_MICRO', sets.versionInfo.get('micro', '0')),
            self._getStringVarDefinition('VERSION_NUMBER_REVISION', sets.versionInfo.get('revision', '0')) ])

        swcFolderPath = self.getTargetPath('swc', sets.getSetting('FOLDER'), isDir=True)
        if not os.path.exists(swcFolderPath):
            os.makedirs(swcFolderPath)

        swcPath = FileUtils.createPath(swcFolderPath, sets.getSetting('FILENAME') + '.swc')
        SystemUtils.remove(swcPath)

        cmd.append('--include-classes')
        sharedClasses = sets.getSetting('SHARED_CLASSES')
        if sharedClasses:
            for c in sharedClasses:
                cmd.append(c)
        cmd.append(self._settings.targetClass)
        cmd.append('-output="%s"' % swcPath)

        header = 'COMPILING SWC: "%s" (%s)' % (
            sets.getSetting('LABEL', 'Unknown'), sets.currentPlatformID)

        if self.executeCommand(cmd, header):
            self._log.write('FAILED: SWC COMPILATION')
            return False
        self._log.write('SUCCESS: SWC COMPILATION')

        zipFolderPath = FileUtils.createPath(swcFolderPath, 'extracted', isDir=True)
        SystemUtils.remove(zipFolderPath)

        try:
            z = zipfile.ZipFile(swcPath)
            z.extractall(zipFolderPath)
        except Exception, err:
            self._log.writeError('FAILED: SWC EXTRACTION', err)
            return False

        self._log.write('SUCCESS: SWC EXTRACTION')

        return True
