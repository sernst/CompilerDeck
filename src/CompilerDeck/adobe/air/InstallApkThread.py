# InstallApkThread.py
# (C)2012-2013
# Scott Ernst

from pyaid.OsUtils import OsUtils
from pyaid.file.FileUtils import FileUtils
from pyaid.system.SystemUtils import SystemUtils

from pyglass.threading.RemoteExecutionThread import RemoteExecutionThread

from CompilerDeck.adobe.flex.FlexProjectData import FlexProjectData

#___________________________________________________________________________________________________ InstallApkThread
class InstallApkThread(RemoteExecutionThread):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of InstallAPKThread."""
        RemoteExecutionThread.__init__(self, parent, **kwargs)
        self._settings = FlexProjectData(**kwargs)

#___________________________________________________________________________________________________ _internalMethod
    def _runImpl(self):
        sets = self._settings

        if not self._settings.hasPlatform(FlexProjectData.ANDROID_PLATFORM):
            self._log.write('ERROR: No Android platform information found. Install aborted.')
            return 1

        self._settings.setPlatform(FlexProjectData.ANDROID_PLATFORM)

        self._log.write(
            '<div style="font-size:24px">Installing APK...</div>\n'
            + '(This can take a few minutes. Please stand by)'
        )

        command = 'adb.exe' if OsUtils.isWindows() else 'adb'
        cmd = [
            '"%s"' % self.parent().mainWindow.getAndroidSDKPath('platform-tools', command),
            'install',
            '-r',
            FileUtils.createPath(
                sets.platformDistributionPath, sets.contentTargetFilename + '.' + sets.airExtension)
        ]

        result = SystemUtils.executeCommand(cmd)

        if result['out']:
            self._log.write(
                '<div style="color:#999999">'
                + '<div style="font-size:18px">Result:'
                + '</div>' + result['out']
                + ('' if result['code'] else ('<br/>' + result['error']))
                + '</div>'
            )

        if result['code'] and result['error']:
            self._log.write(
                '<div style="color:#993333">'
                + '<div style="font-size:18px">Error:'
                + '</div>' + result['error'] + '</div>'
            )

        return result['code']
