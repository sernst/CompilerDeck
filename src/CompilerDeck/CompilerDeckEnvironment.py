# CompilerDeckEnvironment.py
# (C)2013
# Scott Ernst

from pyaid.decorators.ClassGetter import ClassGetter
from pyaid.file.FileUtils import FileUtils

#___________________________________________________________________________________________________ CompilerDeckEnvironment
class CompilerDeckEnvironment(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    SETTINGS_FILE_NAME = 'settings.vcd'

    _rootProjectPath = None

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS projectSettingsPath
    @ClassGetter
    def projectSettingsPath(cls):
        if not cls._rootProjectPath:
            return None

        return cls.getCompileConfigsPath( cls.SETTINGS_FILE_NAME, isFile=True)

#___________________________________________________________________________________________________ GS: desktopAppXmlFilePath
    @ClassGetter
    def desktopAppXmlFilePath(self):
        return FileUtils.createPath(self._rootProjectPath, 'application.xml', isFile=True)

#___________________________________________________________________________________________________ GS: iosAppXmlFilePath
    @ClassGetter
    def iosAppXmlFilePath(self):
        return FileUtils.createPath(self._rootProjectPath, 'ios', 'application.xml', isFile=True)

#___________________________________________________________________________________________________ GS: androidAppXmlFilePath
    @ClassGetter
    def androidAppXmlFilePath(self):
        return FileUtils.createPath(self._rootProjectPath, 'android', 'application.xml', isFile=True)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getProjectPath
    @classmethod
    def getProjectPath(cls, *args, **kwargs):
        if not args:
            kwargs['isDir'] = True
        return FileUtils.createPath(cls._rootProjectPath, *args, **kwargs)

#___________________________________________________________________________________________________ getCompileConfigsPath
    @classmethod
    def getCompileConfigsPath(cls, *args, **kwargs):
        return cls.getProjectPath('compiler', *args, **kwargs)

#___________________________________________________________________________________________________ setRootProjectPath
    @classmethod
    def setRootProjectPath(cls, path):
        cls._rootProjectPath = path
