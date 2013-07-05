# FlexDebugThread.py
# (C)2012-2013
# Scott Ernst

from pyaid.system.SystemUtils import SystemUtils

from pyglass.threading.RemoteExecutionThread import RemoteExecutionThread

from CompilerDeck.adobe.flex.FlexProjectData import FlexProjectData
from CompilerDeck.local.ToolsEnvironment import ToolsEnvironment

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
            '"%s"' % ToolsEnvironment.getAndroidSDKPath('platform-tools', 'adb', isFile=True),
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

        self._log.write('Launching FDB session...')
        cmd = [
            'start',
            'cmd', '/c',
            ToolsEnvironment.getFlexSDKPath('bin', 'fdb.exe', isFile=True),
            '-p',
            str(FlexProjectData.USB_DEBUG_PORT)
        ]

        results = SystemUtils.executeCommand(cmd, remote=True)
        self._log.write(result['out'] + '\n' + result['error'])

        return result['code']


