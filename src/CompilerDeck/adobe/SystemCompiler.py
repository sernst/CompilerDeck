# SystemCompiler.py
# (C)2012-2013
# Scott Ernst

import os

from pyaid.ArgsUtils import ArgsUtils
from pyaid.debug.Logger import Logger
from pyaid.file.FileUtils import FileUtils
from pyaid.file.FileList import FileList
from pyaid.system.SystemUtils import SystemUtils

from CompilerDeck.local.ToolsEnvironment import ToolsEnvironment

#___________________________________________________________________________________________________ SystemCompiler
class SystemCompiler(object):

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, settings, **kwargs):
        """Creates a new instance of SystemCompiler."""
        self._settings = settings

        self._log = ArgsUtils.get('logger', None, kwargs)
        if self._log is None:
            self._log = Logger('ANE_Compile_Log', logFolder=FileUtils.createPath(
                settings.projectPath, 'compiler', 'compile.log', isFile=True))
        self._log.trace = True

        self._commandBuffer = []
        self._batchIndex    = 0
        self._copyMerges    = []

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: projectPath
    @property
    def projectPath(self):
        return self._settings.projectPath

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getProjectPath
    def compile(self, *args, **kwargs):
        try:
            result = self._compileImpl(*args, **kwargs)
        except Exception, err:
            self._cleanup()
            raise

        self._cleanup()
        return result

#___________________________________________________________________________________________________ getProjectPath
    def getProjectPath(self, *args, **kwargs):
        return FileUtils.createPath(self.projectPath, *args)

#___________________________________________________________________________________________________ getAirPath
    def getAirPath(self, *args, **kwargs):
        return ToolsEnvironment.getRootAIRPath(self._settings.airVersion, *args, **kwargs)

#___________________________________________________________________________________________________ getAirLibraryPath
    def getAirLibraryPath(self, *args, **kwargs):
        return self.getAirPath('frameworks', 'libs', 'air', *args, **kwargs)

#___________________________________________________________________________________________________ getFlashLibraryPath
    def getFlashLibraryPath(self, *args, **kwargs):
        return ToolsEnvironment.getFlexSDKPath('frameworks', 'libs', *args, **kwargs)

#___________________________________________________________________________________________________ getTargetPath
    def getTargetPath(self, *args, **kwargs):
        return FileUtils.createPath(self._settings.projectPath, *args)

#___________________________________________________________________________________________________ printCommand
    def printCommand(self, cmd =None, header =None):
        out = ''
        if header:
            out += '<br /><hr /><span style="font-size:24px">%s</span><hr />' % header

        if not cmd and out:
            self._log.write(out)
            return

        cmd = cmd.split(' -')
        out +=  '<div style="font-size:10px;color:#9999CC;">' + cmd[0]
        for c in cmd[1:]:
            out += '\n    -' + c
        self._log.write(out + '</div>')

#___________________________________________________________________________________________________ executeBatchCommand
    def executeBatchCommand(self, cmd, rootPath =None, messageHeader =None):
        if rootPath is None:
            rootPath = self.getTargetPath()

        self._batchIndex += 1

        src = '@echo off\nset errorlevel = 0\n'
        src += '\n'.join(cmd) if isinstance(cmd, list) else cmd
        src += '\nexit /b %errorlevel%'

        batFilename = os.path.join(rootPath, 'compiler_temp_%s.bat' % str(self._batchIndex))
        f = open(batFilename, 'w')
        f.write(src.strip())
        f.close()

        out = self.executeCommand(batFilename, messageHeader=messageHeader, message=src.strip())
        os.remove(batFilename)
        return out

#___________________________________________________________________________________________________ executeCommand
    def executeCommand(self, cmd, messageHeader =None, message =None):
        if isinstance(cmd, list):
            cmd = ' '.join(cmd)

        if messageHeader:
            self.printCommand(message if message else cmd, messageHeader)

        result = SystemUtils.executeCommand(cmd)
        self._commandBuffer.append([result['error'], result['out']])

        out = ''
        if result['out']:
            out += '<br /><br />' \
                   + '<div style="color:#999999"><span style="font-size:16px">RESULTS:</span>\n' \
                   + 50*'- ' + '\n' + str(result['out']) + '</div>'
        if result['error']:
            out += '<br /><br />' \
                   + '<div style="color:#993333"><span style="font-size:16px">ERRORS:</span>\n' \
                   + 50*'- ' + '\n' + str(result['error']) + '</div>'
        if out:
            self._log.write(out + '\n\n')

        self._checkOutput(result['code'], result['out'], result['error'])

        if result['code']:
            return result['code']
        return 0

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _compileImpl
    def _compileImpl(self, *args, **kwargs):
        return True

#___________________________________________________________________________________________________ _checkOutput
    def _cleanup(self):
        while len(self._copyMerges) > 0:
            self._copyMerges.pop().removeFiltered(FileList.CREATED)

#___________________________________________________________________________________________________ _checkOutput
    def _checkOutput(self, code, raw, error):
        pass
