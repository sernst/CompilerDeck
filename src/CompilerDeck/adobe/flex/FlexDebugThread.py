# FlexDebugThread.py
# (C)2012-2013
# Scott Ernst

from pyaid.system.SystemUtils import SystemUtils

from pyglass.app.PyGlassEnvironment import PyGlassEnvironment
from pyglass.threading.RemoteExecutionThread import RemoteExecutionThread

from CompilerDeck.adobe.flex.FlexProjectData import FlexProjectData

#___________________________________________________________________________________________________ FlexDebugThread
class FlexDebugThread(RemoteExecutionThread):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of FlexDebugThread."""
        RemoteExecutionThread.__init__(self, parent, **kwargs)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _runImpl
    def _runImpl(self):
        """Doc..."""

        self._log.write('Refreshing ADB port management...')
        cmd = [
            '"%s"' % self._owner.mainWindow.getAndroidSDKPath('platform-tools', 'adb', isFile=True),
            'forward',
            'tcp:%s' % str(FlexProjectData.USB_DEBUG_PORT),
            'tcp:%s' % str(FlexProjectData.USB_DEBUG_PORT)
        ]

        result = SystemUtils.executeCommand(cmd)
        if result['out'] or result['error']:
            self._log.write(result['out'] + '\n' + result['error'])
        if result['code']:
            self._log.write('FAILED: ADB port management update.')
            return result['code']
        self._log.write('SUCCESS: ADB port management update.')

        fdbCommand = 'fdb.exe' if PyGlassEnvironment.isWindows else 'fdb'

        self._log.write('Launching FDB session...')
        cmd = [
            'start',
            'cmd', '/c',
            self._owner.mainWindow.getFlexSDKPath('bin', fdbCommand, isFile=True),
            '-p',
            str(FlexProjectData.USB_DEBUG_PORT)
        ]

        results = SystemUtils.executeCommand(cmd, remote=True)
        self._log.write(result['out'] + '\n' + result['error'])

        return result['code']


