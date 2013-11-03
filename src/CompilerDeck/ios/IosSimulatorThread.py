# IosSimulatorThread.py
# (C)2013
# Scott Ernst

from pyaid.ArgsUtils import ArgsUtils
from pyaid.file.FileUtils import FileUtils
from pyaid.system.SystemUtils import SystemUtils

from pyglass.app.PyGlassEnvironment import PyGlassEnvironment
from pyglass.threading.RemoteExecutionThread import RemoteExecutionThread

from CompilerDeck.adobe.air.AirUtils import AirUtils
from CompilerDeck.adobe.flex.FlexProjectData import FlexProjectData

#___________________________________________________________________________________________________ IosSimulatorThread
class IosSimulatorThread(RemoteExecutionThread):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of IosSimulatorThread."""
        RemoteExecutionThread.__init__(self, parent, **kwargs)
        self._log.trace = True
        self._settings  = FlexProjectData(**ArgsUtils.get('snapshot', None, kwargs))

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _runImpl
    def _runImpl(self):
        """Doc..."""
        self._log.write('<div style="font-size:24px;">Deploying IOS Simulator</div>')

        sets = self._settings
        sets.setPlatform(FlexProjectData.IOS_PLATFORM)

        adtCommand = self.parent().mainWindow.getRootAIRPath(
            sets.airVersion, 'bin', 'adt', isFile=True)

        targetPath = FileUtils.createPath(
            sets.platformDistributionPath,
            sets.contentTargetFilename + '.' + sets.airExtension,
            isFile=True)

        cmd = [adtCommand, '-installApp', '-platform', 'ios', '-platformsdk',
            '"%s"' % sets.iosSimulatorSdkPath, '-device', 'ios-simulator',
            '-package', targetPath]

        result = SystemUtils.executeCommand(cmd)
        if result['code']:
            self._log.write('Failed simulator installation')
            return 1
        self._log.write('Application installed to simulator')

        cmd = [adtCommand, '-launchApp', '-platform', 'ios', '-platformsdk',
            '"%s"' % sets.iosSimulatorSdkPath, '-device', 'ios-simulator',
            '-appid', '"%s"' % sets.appId]

        self._log.write('Launching simulator')

        result = SystemUtils.executeCommand(cmd)
        if result['code']:
            print result
            self._log.write('Failed simulator execution')
            return 1
        self._log.write('Simulator execution complete')

        return 0



