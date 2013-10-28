# AirDebugThread.py
# (C)2012-2013
# Scott Ernst

import os

from pyaid.ArgsUtils import ArgsUtils
from pyaid.file.FileList import FileList
from pyaid.file.FileUtils import FileUtils
from pyaid.system.SystemUtils import SystemUtils

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
        self._settings  = FlexProjectData(projectPath, **kwargs)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _runImpl
    def _runImpl(self):
        """Doc..."""
        self._log.write('<div style="font-size:24px;">Executing debug...</div>')

        sets = self._settings

        if sets.hasPlatform([FlexProjectData.AIR_PLATFORM, FlexProjectData.NATIVE_PLATFORM]):
            out = self._runAirDebug()
        elif sets.hasPlatform(FlexProjectData.FLASH_PLATFORM):
            out = self._runFlashDebug()
        else:
            out = self._runAirDebug()

        self._log.write('Debug execution complete.')
        return out

#___________________________________________________________________________________________________ _runAirDebug
    def _runAirDebug(self):
        sets = self._settings

        if not sets.updateApplicationConfigFile():
            self._log.write([
                'ERROR: Unable to update the application descriptor file',
                'PATH: ' + sets.appDescriptorPath,
                'VERSION: ' + sets.airVersion,
                'ID: ' + sets.appId ])
            return 1

        cmd = [
            self.parent().mainWindow.getRootAIRPath(sets.airVersion, 'bin', 'adl.exe'),
            FileUtils.createPath(sets.projectPath, 'application.xml', isFile=True),
            sets.platformBinPath ]

        deployment = AirUtils.deployExternalIncludes(self._settings)
        code       = 0
        try:
            os.chdir(FileUtils.createPath(sets.projectPath, isDir=True))
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

        return code

#___________________________________________________________________________________________________ _runFlashDebug
    def _runFlashDebug(self):
        sets = self._settings

        cmd = [
            'C:\\Program Files (x86)\\Internet Explorer\\iexplore.exe',
            FileUtils.createPath(sets.platformBinPath, sets.contentTargetFilename + '.swf') ]

        result = SystemUtils.executeCommand(cmd)
        if result['code']:
            self._log.write(result['out'])
            return 1

        return 0
