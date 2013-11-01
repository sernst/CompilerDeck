# InstallIpaThread.py
# (C)2012-2013
# Scott Ernst

from pyaid.ArgsUtils import ArgsUtils
from pyaid.file.FileUtils import FileUtils
from pyaid.system.SystemUtils import SystemUtils

from pyglass.app.PyGlassEnvironment import PyGlassEnvironment
from pyglass.threading.RemoteExecutionThread import RemoteExecutionThread

from CompilerDeck.adobe.flex.FlexProjectData import FlexProjectData

#___________________________________________________________________________________________________ InstallIpaThread
class InstallIpaThread(RemoteExecutionThread):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of InstallIpaThread."""
        RemoteExecutionThread.__init__(self, parent, **kwargs)
        self._settings = FlexProjectData(**kwargs)

#___________________________________________________________________________________________________ _internalMethod
    def _runImpl(self):
        sets = self._settings

        if not self._settings.hasPlatform(FlexProjectData.IOS_PLATFORM):
            self._log.write('ERROR: No iOS platform information found. Install aborted.')
            return 1

        self._settings.setPlatform(FlexProjectData.IOS_PLATFORM)

        self._log.write(
            '<div style="font-size:24px">Installing IPA...</div>\n'
            + '(This can take a few minutes. Please stand by)'
        )

        if PyGlassEnvironment.isWindows:
            adtCommand = 'adt.bat'
        else:
            adtCommand = 'adt'

        cmd = [
            '"%s"' % self.parent().mainWindow.getRootAIRPath(
                sets.airVersion, 'bin', adtCommand, isFile=True),
            '-installApp',
            '-platform',
            'ios',
            '-package',
            FileUtils.createPath(
                sets.platformDistributionPath, sets.contentTargetFilename + '.' + sets.airExtension)
        ]

        self.log.write('<div style="color:#9999CC">' + '\n'.join(cmd) + '</div>')
        result = SystemUtils.executeCommand(cmd)
        print 'IPA Install:', result

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

        self._log.write('Installation attempt complete')

        return result['code']
