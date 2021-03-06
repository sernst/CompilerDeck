# FlexCompiler.py
# (C)2012-2013
# Scott Ernst

import os

from pyaid.file.FileUtils import FileUtils

from pyglass.app.PyGlassEnvironment import PyGlassEnvironment

from CompilerDeck.adobe.AdobeSystemCompiler import AdobeSystemCompiler
from CompilerDeck.adobe.flex.FlexProjectData import FlexProjectData
from CompilerDeck.adobe.shared.FlashUtils import FlashUtils

#___________________________________________________________________________________________________ FlexCompiler
class FlexCompiler(AdobeSystemCompiler):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, owner, settings, **kwargs):
        """Creates a new instance of FlexCompiler."""
        AdobeSystemCompiler.__init__(self, owner, settings, **kwargs)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _compileImpl
    def _compileImpl(self):
        """Doc..."""

        cmd          = []
        sets         = self._settings
        airPath      = self._owner.mainWindow.getRootAIRPath()
        isAir        = sets.currentPlatformID != FlexProjectData.FLASH_PLATFORM
        isAndroid    = sets.currentPlatformID == FlexProjectData.ANDROID_PLATFORM
        isIOS        = sets.currentPlatformID == FlexProjectData.IOS_PLATFORM
        flashVersion = sets.getFlashVersion(self._owner.mainWindow.getRootAIRPath())

        fileParts = sets.targetClass.split('.')
        mainClass = FileUtils.createPath(
            sets.projectPath, 'src', fileParts[:-1], fileParts[-1] + '.as', isFile=True)

        cmd.append('-load-config+="%s"' % FileUtils.createPath(
            sets.projectPath, 'compiler', 'shared-targets-asc2.xml', isFile=True, noTail=True))

        cmd.append('-default-background-color=0x000000')

        if sets.aneIncludes:
            for ane in sets.aneIncludes:
                anePath = FileUtils.createPath(sets.projectPath, 'NativeExtensions', ane, isDir=True)
                aneSets = FlexProjectData(anePath)

                if not aneSets.setPlatform(sets.currentPlatformID):
                    aneSets.setPlatform(FlexProjectData.DEFAULT_PLATFORM)

                cmd.append('-external-library-path+="%s"' % FileUtils.createPath(
                    aneSets.projectPath, 'swc', aneSets.getSetting('FOLDER'), isDir=True, noTail=True))

        cmd.extend([
            '-library-path+="%s"' % os.path.join(sets.projectPath, 'lib'),
            '-source-path+="%s"'  % os.path.join(sets.projectPath, 'src') ])

        if sets.swcIncludes:
            for swc in sets.swcIncludes:
                cmd.append('-include-libraries+="%s"'
                    % os.path.join(sets.projectPath, 'lib', swc + '.swc'))

        if sets.advancedTelemetry:
            cmd.append('-advanced-telemetry=true')
            #if isIOS:
            #    cmd.append('-sampler=false')

        cmd.extend([
            self._getBooleanDefinition('LIVE', sets.live),
            self._getBooleanDefinition('DEBUG', sets.debug),
            self._getBooleanDefinition('REMOTE_DEBUG', sets.remoteDebug),
            self._getBooleanDefinition('RELEASE', not sets.debug),
            self._getBooleanDefinition('AIR', isAir),
            self._getBooleanDefinition('DESKTOP', isAir and not isAndroid and not isIOS),
            self._getBooleanDefinition('IOS', isIOS),
            self._getBooleanDefinition('ANDROID', isAndroid),
            self._getStringVarDefinition('VERSION_LABEL_PREFIX', sets.versionInfo.get('prefix', '')),
            self._getStringVarDefinition('VERSION_LABEL_DATE', sets.versionInfo.get('date', '')),
            self._getStringVarDefinition('VERSION_LABEL_SUFFIX', sets.versionInfo.get('suffix', '1')),
            self._getStringVarDefinition('VERSION_NUMBER_MAJOR', sets.versionInfo.get('major', '0')),
            self._getStringVarDefinition('VERSION_NUMBER_MINOR', sets.versionInfo.get('minor', '0')),
            self._getStringVarDefinition('VERSION_NUMBER_MICRO', sets.versionInfo.get('micro', '0')),
            self._getStringVarDefinition('VERSION_NUMBER_REVISION', sets.versionInfo.get('revision', '0')) ])

        # Create the bin path if it does not exist already
        if not os.path.exists(sets.platformBinPath):
            os.makedirs(sets.platformBinPath)

        cmd.extend([
            '-output="%s"' % (FileUtils.createPath(sets.platformBinPath, sets.contentTargetFilename + '.swf')),
            '-omit-trace-statements=' + self._getAsBooleanString(not sets.debug),
            '-verbose-stacktraces=' + self._getAsBooleanString(sets.debug),
            '-debug=' + self._getAsBooleanString(sets.debug),
            '-target-player=' + flashVersion,
            '-swf-version=' + str(FlashUtils.convertFlashToSwfVersion(flashVersion)),
            mainClass ])

        if PyGlassEnvironment.isWindows:
            commandFile = 'amxmlc.bat' if isAir else 'mxmlc.bat'
        else:
            commandFile = 'amxmlc' if isAir else 'mxmlc'

        cmd.insert(
            0, FileUtils.createPath(airPath, sets.airVersion, 'bin', commandFile, isFile=True))

        if self.executeCommand(cmd, 'COMPILING SWF: "%s"' % sets.currentPlatformID):
            self._log.write('FAILED: SWF COMPILATION')
            return False

        self._log.write('SUCCESS: SWF COMPILED')
        return True
