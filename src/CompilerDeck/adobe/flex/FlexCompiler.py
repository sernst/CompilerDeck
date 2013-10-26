# FlexCompiler.py
# (C)2012-2013
# Scott Ernst

import os

from pyaid.file.FileUtils import FileUtils

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
        flashVersion = self._getFlashVersion()

        fileParts = sets.targetClass.split('.')
        mainClass = FileUtils.createPath(
            sets.projectPath, 'src', fileParts[:-1], fileParts[-1] + '.as', isFile=True)

        if isAir:
            cmd.append('+configname=air')

        cmd.append('-load-config+=' + FileUtils.createPath(
            sets.projectPath, 'compiler', 'shared-targets-asc2.xml', isFile=True))

        flashGlobals = FileUtils.createPath(airPath, sets.airVersion, 'frameworks', isDir=True)

        if sets.aneIncludes:
            aneType = 'android' if isAndroid else ('ios' if isIOS else 'default')
            for ane in sets.aneIncludes:
                cmd.append('-external-library-path+=' + FileUtils.createPath(
                    sets.projectPath, 'air', 'ane', ane, 'bin', aneType, isDir=True))

        if isAir:
            airRoot    = FileUtils.createPath(airPath, sets.airVersion, 'frameworks', isDir=True)
            airGlobals = FileUtils.createPath(airRoot, 'libs', 'air', isDir=True)
            cmd.extend([
                '-external-library-path+=' + os.path.join(airGlobals, 'airglobal.swc'),
                '-library-path+=' + FileUtils.createPath(airRoot, 'libs', isDir=True),
                '-library-path+=' + FileUtils.createPath(airRoot, 'libs', 'air', isDir=True),
                '-library-path+=' + FileUtils.createPath(flashGlobals, 'locale', 'en_US', isDir=True) ])
        else:
            flashGlobals += 'libs'
            cmd.extend([
                '-external-library-path+='
                    + os.path.join(flashGlobals, 'player', sets.flashVersion, 'playerglobal.swc'),
                '-library-path+=' + flashGlobals,
                '-library-path+=' + os.path.join(flashGlobals, 'mobile'),
                '-library-path+=' + os.path.join(flashGlobals, 'automation') ])

        cmd.extend([
            '-library-path+=' + os.path.join(sets.projectPath, 'lib'),
            '-source-path+='  + os.path.join(sets.projectPath, 'src') ])

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
            self._getStringVarDefinition('VERSION_NUMBER_REVISION', sets.versionInfo.get('revision', '0'))
        ])

        if sets.swcIncludes:
            for swc in sets.swcIncludes:
                cmd.append('-include-libraries+='
                    + os.path.join(sets.projectPath, 'lib', swc + '.swc'))

        if sets.advancedTelemetry:
            cmd.append('-advanced-telemetry=true')
            #if isIOS:
            #    cmd.append('-sampler=false')

        # Create the bin path if it does not exist already
        if not os.path.exists(sets.platformBinPath):
            os.makedirs(sets.platformBinPath)

        cmd.extend([
            '-output=' + FileUtils.createPath(sets.platformBinPath, sets.targetFilename + '.swf'),
            '-omit-trace-statements=' + self._getAsBooleanString(not sets.debug),
            '-verbose-stacktraces=' + self._getAsBooleanString(sets.debug),
            '-debug=' + self._getAsBooleanString(sets.debug),
            '-target-player=' + flashVersion,
            '-swf-version=' + str(FlashUtils.convertFlashToSwfVersion(flashVersion)),
            mainClass ])

        cmd.insert(0, os.path.join(airPath, sets.airVersion, 'bin', 'amxmlc.bat' if isAir else 'mxmlc.bat'))

        if self.executeCommand(cmd, 'COMPILING SWF: "%s"' % sets.currentPlatformID):
            self._log.write('FAILED: SWF COMPILATION')
            return False

        self._log.write('SUCCESS: SWF COMPILED')
        return True


#___________________________________________________________________________________________________ _getFlashVersion
    def _getFlashVersion(self):
        sets = self._settings
        if sets.currentPlatformID == FlexProjectData.FLASH_PLATFORM:
            return sets.flashVersion

        airPath     = self._owner.mainWindow.getRootAIRPath()
        playersPath = FileUtils.createPath(
            airPath, sets.airVersion, 'frameworks', 'libs', 'player', isDir=True)
        print 'PLAYERS PATH:', playersPath

        playerVersion = None
        for item in os.listdir(playersPath):
            itemPath = FileUtils.createPath(playersPath, item, isDir=True)
            if not os.path.exists(itemPath) or not os.path.isdir(itemPath):
                continue

            try:
                versionValue = float(item)
            except Exception, err:
                self._log.writeError('Unrecognized Flash player directory: ' + str(item), err)
                continue

            if playerVersion is None or versionValue > float(playerVersion):
                playerVersion = item

        if playerVersion is None:
            return sets.flashVersion

        return playerVersion
