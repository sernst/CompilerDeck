# AirDebugThread.py
# (C)2012-2013
# Scott Ernst

import os

from pyaid.ArgsUtils import ArgsUtils
from pyaid.OsUtils import OsUtils
from pyaid.file.FileList import FileList
from pyaid.file.FileUtils import FileUtils
from pyaid.system.SystemUtils import SystemUtils

from pyglass.app.PyGlassEnvironment import PyGlassEnvironment
from pyglass.threading.RemoteExecutionThread import RemoteExecutionThread

from CompilerDeck.adobe.air.AirUtils import AirUtils
from CompilerDeck.adobe.flex.FlexProjectData import FlexProjectData

#___________________________________________________________________________________________________ AirDebugThread
class AirDebugThread(RemoteExecutionThread):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of AirDebugThread."""
        RemoteExecutionThread.__init__(self, parent, **kwargs)
        self._log.trace = True
        projectPath     = ArgsUtils.extract('projectPath', None, kwargs)
        self._projectData  = FlexProjectData(projectPath, **kwargs)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _runImpl
    def _runImpl(self):
        """Doc..."""
        self._log.write('<div style="font-size:24px;">Executing debug...</div>')

        pd = self._projectData

        if pd.hasPlatform([FlexProjectData.AIR_PLATFORM, FlexProjectData.NATIVE_PLATFORM]):
            out = self._runAirDebug()
        elif pd.hasPlatform(FlexProjectData.FLASH_PLATFORM):
            out = self._runFlashDebug()
        else:
            out = self._runAirDebug()

        self._log.write('Debug execution complete.')
        return out

#___________________________________________________________________________________________________ _runAirDebug
    def _runAirDebug(self):
        pd = self._projectData

        if OsUtils.isWindows() and pd.hasPlatform(FlexProjectData.WINDOWS_PLATFORM):
            pd.setPlatform(FlexProjectData.WINDOWS_PLATFORM)
        elif OsUtils.isMac() and pd.hasPlatform(FlexProjectData.MAC_PLATFORM):
            pd.setPlatform(FlexProjectData.MAC_PLATFORM)
        elif pd.hasPlatform(FlexProjectData.AIR_PLATFORM):
            pd.setPlatform(FlexProjectData.AIR_PLATFORM)

        if not pd.updateApplicationConfigFile():
            self._log.write([
                'ERROR: Unable to update the application descriptor file',
                'PATH: ' + pd.appDescriptorPath,
                'VERSION: ' + pd.airVersion,
                'ID: ' + pd.appId ])
            return 1


        adlCommand    = 'adl.exe' if PyGlassEnvironment.isWindows else 'adl'
        appDescriptor = FileUtils.createPath(pd.projectPath, 'application.xml', isFile=True)

        cmd = [
            self.parent().mainWindow.getRootAIRPath(pd.airVersion, 'bin', adlCommand),
            '-profile', 'extendedDesktop']

        aneDebugPath = AirUtils.deployDebugNativeExtensions(cmd, pd)

        cmd += [appDescriptor, pd.platformBinPath]

        deployment = AirUtils.deployExternalIncludes(self._projectData)
        code       = 0
        try:
            os.chdir(FileUtils.createPath(pd.projectPath, isDir=True))
            print 'PLATFORM:', pd.currentPlatformID
            print 'LOCATION:', os.path.abspath(os.curdir)
            print 'COMMAND:', cmd

            result = SystemUtils.executeCommand(cmd)
            if result['code']:
                self._log.write('RESULT ERROR CODE: ' + str(result['code']) + '\n' + result['out'])
                code = 1
        except Exception, err:
            self._log.writeError('DEBUG ATTEMPT FAILED', err)
            code = 1

        # Cleanup deployment
        for item in deployment['merges']:
            item.removeFiltered(FileList.CREATED)

        if aneDebugPath is not None:
            SystemUtils.remove(aneDebugPath)

        return code

#___________________________________________________________________________________________________ _runFlashDebug
    def _runFlashDebug(self):
        sets = self._projectData

        cmd = [
            'C:\\Program Files (x86)\\Internet Explorer\\iexplore.exe',
            FileUtils.createPath(sets.platformBinPath, sets.contentTargetFilename + '.swf') ]

        result = SystemUtils.executeCommand(cmd)
        if result['code']:
            self._log.write(result['out'])
            return 1

        return 0
