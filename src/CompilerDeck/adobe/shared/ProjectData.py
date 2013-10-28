# ProjectData.py
# (C)2012-2013
# Scott Ernst

import os
import socket

from pyaid.ArgsUtils import ArgsUtils
from pyaid.NullUtils import NullUtils
from pyaid.config.ConfigsDict import ConfigsDict
from pyaid.config.SettingsConfig import SettingsConfig
from pyaid.file.FileUtils import FileUtils

from CompilerDeck.CompilerDeckEnvironment import CompilerDeckEnvironment
from CompilerDeck.adobe.shared.FlashUtils import FlashUtils

#___________________________________________________________________________________________________ ClassTemplate
class ProjectData(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, projectPath, **kwargs):
        """Creates a new instance of ClassTemplate."""

        # The absolute path to the top-level directory where the actionscript project resides
        self._projectPath  = projectPath
        if not os.path.exists(projectPath):
            raise Exception, 'Invalid project path: ' + projectPath

        # Specified the debug mode
        self._debug        = ArgsUtils.get('debug', None, kwargs)

        # The version of the AIR runtime to use for compiling/debugging/packaging
        self._airVersion   = ArgsUtils.get('airVersion', '3.9', kwargs)

        # The version of the Flash player to use for compiling/debugging
        self._flashVersion = ArgsUtils.get('flashVersion', '11.8', kwargs)

        # Loads the settings file where the project settings are stored
        self._settings = SettingsConfig(CompilerDeckEnvironment.projectSettingsPath, pretty=True)
        self._overrideSettings = None

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: overrideSettings
    @property
    def overrideSettings(self):
        return self._overrideSettings
    @overrideSettings.setter
    def overrideSettings(self, value):
        if value:
            value = ConfigsDict(value)
        self._overrideSettings = value

#___________________________________________________________________________________________________ GS: ipAddress
    @property
    def ipAddress(self):
        res = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
               if not ip.startswith("127.")][:1]
        return res[0] if res else None

#___________________________________________________________________________________________________ GS: targetClass
    @property
    def targetClass(self):
        return self.getSetting('TARGET_CLASS', None)

#___________________________________________________________________________________________________ GS: androidTargetVersion
    @property
    def androidTargetVersion(self):
        return self.getSetting(['ANDROID', 'TARGET_VERSION'], error=True)

#___________________________________________________________________________________________________ GS: androidMinVersion
    @property
    def androidMinVersion(self):
        return self.getSetting(['ANDROID', 'MIN_VERSION'], error=True)

#___________________________________________________________________________________________________ GS: airVersion
    @property
    def airVersion(self):
        return self._airVersion

#___________________________________________________________________________________________________ GS: flashVersion
    @property
    def flashVersion(self):
        return self._flashVersion

#___________________________________________________________________________________________________ GS: swfVersion
    @property
    def swfVersion(self):
        return FlashUtils.convertFlashToSwfVersion(self.flashVersion)

#___________________________________________________________________________________________________ GS: debug
    @property
    def debug(self):
        return self._debug

#___________________________________________________________________________________________________ GS: projectPath
    @property
    def projectPath(self):
        return FileUtils.cleanupPath(self._projectPath)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getSetting
    def getSetting(
            self, key, defaultValue =None, error =False, forceRelease =False, forceDebug =False
    ):
        if forceRelease:
            deepKey = 'RELEASE'
        elif forceDebug:
            deepKey = 'DEBUG'
        else:
            deepKey = 'DEBUG' if self._debug else 'RELEASE'

        if isinstance(key, basestring):
            deepKey = [deepKey, key]
        else:
            deepKey = [deepKey] + key

        out = self._getProjectSetting(deepKey, defaultValue=NullUtils.UNIVERSAL_NULL)

        if out != NullUtils.UNIVERSAL_NULL:
            return out

        return self._getProjectSetting(key, defaultValue, error)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getSetting
    def _getProjectSetting(self, key, defaultValue =None, error =False):
        if self._overrideSettings:
            res = self._overrideSettings.get(key, NullUtils.UNIVERSAL_NULL)
            if res != NullUtils.UNIVERSAL_NULL:
                return res

        return self._settings.get(key, defaultValue=defaultValue)

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __unicode__
    def __unicode__(self):
        return unicode(self.__str__())

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s>' % self.__class__.__name__
