# ToolsEnvironment.py
# (C)2012-2013
# Scott Ernst

import sys
import os
import re
import requests.utils

from PySide.QtGui import *

from pyaid.ArgsUtils import ArgsUtils
from pyaid.decorators.ClassGetter import ClassGetter
from pyaid.file.FileUtils import FileUtils
from pyaid.interactive import queries
from pyaid.json.JSON import JSON

#___________________________________________________________________________________________________ ToolsEnvironment
class ToolsEnvironment(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _ENV_PATH             = os.path.dirname(os.path.abspath(__file__))
    _ENV_SETTINGS         = None
    _GLOBAL_SETTINGS_FILE = 'environment.vcd'

    _PROG_PATH            = 'C:\\Program Files (x86)\\'
    _PROG_64_PATH         = 'C:\\Program Files\\'
    _NUM_FINDER           = re.compile('[0-9]+')
    _JDK_PATH             = None

    _AIR_ROOT_PATH           = 'AIR_ROOT_PATH'
    _FLEX_SDK_PATH           = 'FLEX_SDK_PATH'
    _JAVA_ROOT_PATH          = 'JAVA_ROOT_PATH'
    _JAVA_ANT_PATH           = 'JAVA_ANT_PATH'
    _ANDROID_SDK_PATH        = 'ANDROID_SDK_PATH'
    _APPLE_PROVISION_PROFILE = 'APPLE_PROVISION_PROFILE'
    _BASE_UNIX_TIME          = 1293868800

    _qApplication = None
    _qMainWindow  = None
    _deployed     = None

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ BASE_UNIX_TIME
    @ClassGetter
    def BASE_UNIX_TIME(cls):
        return cls._BASE_UNIX_TIME

#___________________________________________________________________________________________________ requestsCABundle
    @ClassGetter
    def requestsCABundle(cls):
        if cls.deployed:
            return  cls.getToolsResourcePath(
                'pythonRoot',
                'Lib',
                'site-packages',
                'requests',
                'cacert.pem',
                isFile=True
            )
        return requests.utils.DEFAULT_CA_BUNDLE_PATH

#___________________________________________________________________________________________________ qApplication
    @ClassGetter
    def qApplication(cls):
        return cls._qApplication

#___________________________________________________________________________________________________ qMainWindow
    @ClassGetter
    def qMainWindow(cls):
        return cls._qMainWindow

#___________________________________________________________________________________________________ deployed
    @ClassGetter
    def deployed(cls):
        try:
            if cls._deployed is None:
                cls._deployed = cls._ENV_PATH.find(os.sep + 'library.zip' + os.sep) != -1
            return cls._deployed
        except Exception, err:
            return True

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ isWindows
    @classmethod
    def isWindows(cls):
        return sys.platform.startswith('win')

#___________________________________________________________________________________________________ setGuiApplication
    @classmethod
    def setGuiApplication(cls, value =None):
        cls._qApplication = value

#___________________________________________________________________________________________________ setGuiWindow
    @classmethod
    def setGuiWindow(cls, value =None):
        cls._qMainWindow = value

#___________________________________________________________________________________________________ refresh
    @classmethod
    def refresh(cls):
        cls._ENV_SETTINGS = None
        cls._JDK_PATH     = None
        return True

#___________________________________________________________________________________________________ settingsFileExists
    @classmethod
    def settingsFileExists(cls):
        return os.path.exists(
            cls.getToolsLocalResourcePath(cls._GLOBAL_SETTINGS_FILE, isFile=True)
        )

#___________________________________________________________________________________________________ getAppleProvisionProfile
    @classmethod
    def getAppleProvisionProfile(cls, **kwargs):
        res = cls._getEnvValue(cls._APPLE_PROVISION_PROFILE)
        if not res:
            if ArgsUtils.get('allowEmpty', False, kwargs):
                return ''

            res = cls._queryForPath('Apple Provisioning Profile')
            cls.setAppleProvisionProfile(res)

        return res

#___________________________________________________________________________________________________ getAppleProvisionProfile
    @classmethod
    def setAppleProvisionProfile(cls, path):
        return cls._setEnvValue(cls._APPLE_PROVISION_PROFILE, path)

#___________________________________________________________________________________________________ getRootAIRPath
    @classmethod
    def getRootAIRPath(cls, *args, **kwargs):
        """Doc..."""
        res = cls._getEnvValue(cls._AIR_ROOT_PATH)
        if not res:
            if ArgsUtils.get('allowEmpty', False, kwargs):
                return ''

            res = FileUtils.createPath(cls._queryForPath('Adobe Air Root Path'))
            cls.setRootAIRPath(res)

        return FileUtils.createPath(res, *args, **kwargs)

#___________________________________________________________________________________________________ setRootAIRPath
    @classmethod
    def setRootAIRPath(cls, path):
        """Doc..."""
        return cls._setEnvValue(cls._AIR_ROOT_PATH, path)

#___________________________________________________________________________________________________ getFlexSDKPath
    @classmethod
    def getFlexSDKPath(cls, *args, **kwargs):
        """Doc..."""
        res = cls._getEnvValue(cls._FLEX_SDK_PATH)
        if not res:
            if ArgsUtils.get('allowEmpty', False, kwargs):
                return ''

            res = FileUtils.createPath(cls._queryForPath('Flex SDK Path'))
            print 'RES:',res
            cls.setFlexSDKPath(res)

        return FileUtils.createPath(res, *args, **kwargs)

#___________________________________________________________________________________________________ setFlexSDKPath
    @classmethod
    def setFlexSDKPath(cls, path):
        """Doc..."""
        return cls._setEnvValue(cls._FLEX_SDK_PATH, path)

#___________________________________________________________________________________________________ getJavaJDKPath
    @classmethod
    def getJavaJDKPath(cls, *args, **kwargs):
        """Doc..."""
        return cls._getJDKPath(*args, **kwargs)

#___________________________________________________________________________________________________ getJavaAntPath
    @classmethod
    def getJavaAntPath(cls, *args, **kwargs):
        """Doc..."""
        res = cls._getEnvValue(cls._JAVA_ANT_PATH)
        if not res:
            if ArgsUtils.get('allowEmpty', False, kwargs):
                return ''

            res = FileUtils.createPath(cls._queryForPath('Java Ant Path'))
            cls.setJavaAntPath(res)

        return FileUtils.createPath(res, *args, **kwargs)

#___________________________________________________________________________________________________ setJavaAntPath
    @classmethod
    def setJavaAntPath(cls, path):
        """Doc..."""
        return cls._setEnvValue(cls._JAVA_ANT_PATH, path)

#___________________________________________________________________________________________________ getAndroidSDKPath
    @classmethod
    def getAndroidSDKPath(cls, *args, **kwargs):
        """Doc..."""
        res = cls._getEnvValue(cls._ANDROID_SDK_PATH)
        if not res:
            if ArgsUtils.get('allowEmpty', False, kwargs):
                return ''

            res = FileUtils.createPath(cls._queryForPath('Android SDK Path'))
            cls.setAndroidSDKPath(res)

        return FileUtils.createPath(res, *args, **kwargs)

#___________________________________________________________________________________________________ setAndroidSDKPath
    @classmethod
    def setAndroidSDKPath(cls, path):
        """Doc..."""
        return cls._setEnvValue(cls._ANDROID_SDK_PATH, path)

#___________________________________________________________________________________________________ getToolsPath
    @classmethod
    def getToolsPath(cls, *args, **kwargs):
        """Doc..."""
        if cls.deployed:
            if cls.isWindows():
                args = ('vizme',) + args
                return FileUtils.createPath(os.environ['LOCALAPPDATA'], *args, **kwargs)

        return FileUtils.createPath(
            cls._ENV_PATH[:cls._ENV_PATH.find(os.sep + 'tools' + os.sep)],
            'tools',
            *args, **kwargs
        )

#___________________________________________________________________________________________________ getToolsResourcePath
    @classmethod
    def getToolsResourcePath(cls, *args, **kwargs):
        """Doc..."""
        return cls.getToolsPath('resources', *args, **kwargs)

#___________________________________________________________________________________________________ getToolsSharedResourcesPath
    @classmethod
    def getToolsSharedResourcesPath(cls, *args, **kwargs):
        """Doc..."""
        return cls.getToolsPath('resources', 'shared', *args, **kwargs)

#___________________________________________________________________________________________________ getToolsLocalResourcePath
    @classmethod
    def getToolsLocalResourcePath(cls, *args, **kwargs):
        """Doc..."""
        if cls.deployed:
            if cls.isWindows():
                args = ('vizme', 'local_resources') + args
                return FileUtils.createPath(os.environ['LOCALAPPDATA'], *args, **kwargs)

        return cls.getToolsPath('resources', 'local', *args, **kwargs)

#___________________________________________________________________________________________________ listInstalledAirSDKs
    @classmethod
    def listInstalledAirSDKs(cls):
        out = []
        for item in os.listdir(cls.getRootAIRPath()):
            try:
                float(item)
                out.append(item)
            except Exception, err:
                continue
        out.sort(reverse=True)
        return out

#___________________________________________________________________________________________________ listInstalledFlashPlayers
    @classmethod
    def listInstalledFlashPlayers(cls):
        out = []
        for item in os.listdir(cls.getFlexSDKPath('frameworks', 'libs', 'player')):
            try:
                float(item)
                out.append(item)
            except Exception, err:
                continue
        out.sort(reverse=True)
        return out

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _setEnvValue
    @classmethod
    def _setEnvValue(cls, key, value):
        settings = cls._getEnvValue(None) if cls._ENV_SETTINGS is None else cls._ENV_SETTINGS
        if settings is None:
            settings = dict()
            cls._ENV_SETTINGS = settings

        if isinstance(key, basestring):
            key = [key]

        src = settings
        for k in key[:-1]:
            src = src[k]
        src[key[-1]] = value

        envPath = cls.getToolsLocalResourcePath(cls._GLOBAL_SETTINGS_FILE, isFile=True)
        envDir  = os.path.dirname(envPath)
        if not os.path.exists(envDir):
            os.makedirs(envDir)

        f = open(envPath, 'w+')
        try:
            f.write(JSON.asString(cls._ENV_SETTINGS))
        except Exception, err:
            print 'ERROR: Unable to write environmental settings file at: ' + envPath
            return False
        finally:
            f.close()

        return True

#___________________________________________________________________________________________________ _queryForPath
    @classmethod
    def _queryForPath(cls, dialogName):
        path = None
        while not path:
            if cls._qMainWindow:
                caption = 'Select %s Directory' % dialogName
                path    = QFileDialog.getExistingDirectory(cls._qMainWindow, caption=caption)
            else:
                caption = 'Specify %s directory: ' % dialogName
                path    = queries.queryGeneralValue(caption)
        return path

#___________________________________________________________________________________________________ _getEnvValue
    @classmethod
    def _getEnvValue(cls, key, defaultValue =None, refresh =False, error =False):
        if cls._ENV_SETTINGS is None or refresh:
            if not cls.settingsFileExists():
                print 'WARNING: No environmental settings file found.'
                return defaultValue

            envPath = cls.getToolsLocalResourcePath(cls._GLOBAL_SETTINGS_FILE, isFile=True)
            f       = open(envPath, 'r+')
            try:
                res = f.read()
            except Exception, err:
                print 'ERROR: Unable to read the environmental settings file at: ' + envPath
                return
            finally:
                f.close()

            try:
                settings = JSON.fromString(res)
            except Exception, err:
                print 'ERROR: Unable to parse environmental settings file at: ' + envPath
                return

            cls._ENV_SETTINGS = settings
        else:
            settings = cls._ENV_SETTINGS

        if key is None:
            return settings

        if isinstance(key, basestring):
            key = [key]
        value = settings
        for k in key:
            if k in value:
                value = value[k]
            else:
                if error:
                    raise Exception, 'Missing environmental setting: ' + str(key)
                return defaultValue

        return value

#___________________________________________________________________________________________________ getJDKPath
    @classmethod
    def _getJDKPath(cls, *args, **kwargs):
        if cls._JDK_PATH is None:
            jdkPath   = None
            lastParts = [0, 0, 0, 0]
            for root in [cls._PROG_64_PATH, cls._PROG_PATH]:
                for p in os.listdir(FileUtils.createPath(root, 'java')):
                    if not p.lower().startswith('jdk'):
                        continue

                    parts = cls._NUM_FINDER.findall(p)
                    skip  = False
                    index = 0
                    while index < len(lastParts) and index < len(parts):
                        if parts[index] < lastParts[index]:
                            skip = True
                            break
                        index += 1

                    if not skip:
                        lastParts = parts
                        jdkPath   = FileUtils.createPath(cls._PROG_64_PATH, 'java', p)
            cls._JDK_PATH = jdkPath

        if cls._JDK_PATH is None:
            raise Exception, 'Unable to locate a Java Development Kit installation.'

        return FileUtils.createPath(cls._JDK_PATH, *args, **kwargs)

