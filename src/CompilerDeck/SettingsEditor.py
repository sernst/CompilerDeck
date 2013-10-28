# SettingsEditor.py
# (C)2013
# Scott Ernst


import re
import datetime
from collections import namedtuple

from pyaid.ArgsUtils import ArgsUtils
from pyaid.file.FileUtils import FileUtils
from pyaid.json.JSON import JSON
from pyaid.radix.Base36 import Base36
from pyaid.time.TimeUtils import TimeUtils

from CompilerDeck.CompilerDeckEnvironment import CompilerDeckEnvironment

#___________________________________________________________________________________________________ SettingsEditor
class SettingsEditor(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    DEF_PREFIX   = u'Build'
    DEF_SUFFIX   = u'1'
    DEF_MAJOR    = u'0'
    DEF_MINOR    = u'0'
    DEF_REVISION = u'0'

    _UNSET    = 0
    _FILE_SET = 1
    _USER_SET = 2

    _SETTING_NT      = namedtuple('CLIENT_SETTING_NT', ('key', 'value', 'setLevel'))
    _TAG_PATTERN_DEF = '(?P<open><#TAG#>)(?P<value>[^<]*)(?P<close></#TAG#>)'

#___________________________________________________________________________________________________ __init__
    def __init__(self, **kwargs):
        """Creates a new instance of SettingsEditor."""
        self.reset(**kwargs)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: prefix
    @property
    def prefix(self):
        return self._prefix.value
    @prefix.setter
    def prefix(self, value):
        self._prefix = self._putSetting(self._prefix, unicode(value), self._UNSET)

#___________________________________________________________________________________________________ GS: suffixInteger
    @property
    def suffixInteger(self):
        return Base36.from36(self._suffix.value)
    @suffixInteger.setter
    def suffixInteger(self, value):
        self.suffix = Base36.to36(value)

#___________________________________________________________________________________________________ GS: suffix
    @property
    def suffix(self):
        return self._suffix.value
    @suffix.setter
    def suffix(self, value):
        if not isinstance(value, basestring):
            value = Base36.to36(value).upper()
        self._suffix = self._putSetting(self._suffix, unicode(value).upper(), self._UNSET)

#___________________________________________________________________________________________________ GS: major
    @property
    def major(self):
        return self._major.value
    @major.setter
    def major(self, value):
        self._major = self._putSetting(self._major, unicode(value), self._UNSET)

#___________________________________________________________________________________________________ GS: minor
    @property
    def minor(self):
        return self._minor.value
    @minor.setter
    def minor(self, value):
        self._minor = self._putSetting(self._minor, unicode(value), self._UNSET)

#___________________________________________________________________________________________________ GS: revision
    @property
    def revision(self):
        return self._revision.value
    @revision.setter
    def revision(self, value):
        self._revision = self._putSetting(self._revision, unicode(value), self._UNSET)

#___________________________________________________________________________________________________ GS: versionLabel
    @property
    def versionLabel(self):
        return self._prefix.value + u'-' + self._date.value + u'-' + self._suffix.value

#___________________________________________________________________________________________________ GS: versionNumber
    @property
    def versionNumber(self):
        return self._major.value + u'.' + self._minor.value + u'.' + self._revision.value

#___________________________________________________________________________________________________ GS: dateValue
    @property
    def dateValue(self):
        return self._dateValue

#___________________________________________________________________________________________________ GS: buildLogFilePath
    @property
    def buildLogFilePath(self):
        return CompilerDeckEnvironment.getProjectPath('compiler', 'builds.log', isFile=True)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ toDict
    def toDict(self):
        return {
            'prefix':self._prefix.value,
            'suffix':self._suffix.value,
            'major':self._major.value,
            'date':self._date.value,
            'minor':self._minor.value,
            'revision':self._revision.value }

#___________________________________________________________________________________________________ fromDict
    def fromDict(self, data):
        self.setTo(**data)

#___________________________________________________________________________________________________ setTo
    def setTo(self, **kwargs):
        if kwargs.has_key('prefix'):
            self.prefix = kwargs['prefix']
        if kwargs.has_key('suffix'):
            self.suffix = kwargs['suffix']
        if kwargs.has_key('major'):
            self.major = kwargs['major']
        if kwargs.has_key('minor'):
            self.minor = kwargs['minor']
        if kwargs.has_key('revision'):
            self.revision = kwargs['revision']

#___________________________________________________________________________________________________ logBuild
    def logBuild(self, builtDesktop =False, builtNative =False, builtAndroid =False, builtIOS =False):
        if not builtDesktop and not builtAndroid and not builtIOS:
            return

        out = '\t'.join([
            TimeUtils.getNowDatetime().strftime('[%a %m-%d %H:%M]'),
            'DSK' if builtDesktop else '---',
            'NAT' if builtNative else '---',
            'AND' if builtAndroid else '---',
            'IOS' if builtIOS else '---',
            '<<' + self.versionNumber + '>>',
            '<<' + self.versionLabel + '>>'
        ]) + '\n'
        FileUtils.putContents(out, self.buildLogFilePath, True)
        return out

#___________________________________________________________________________________________________ makeUnique
    def makeUnique(self):
        builds = FileUtils.getContents(self.buildLogFilePath)
        if not builds:
            return

        while builds.find('<<' + self.versionLabel + '>>') != -1:
            index = Base36.from36(self._suffix.value.upper())
            self._suffix = self._putSetting(self._suffix, Base36.to36(index + 1), 1)

        while builds.find('<<' + self.versionNumber + '>>') != -1:
            self._revision = self._putSetting(
                self._revision, unicode(int(self._revision.value) + 1), 1)

#___________________________________________________________________________________________________ reset
    def reset(self, **kwargs):
        self._prefix        = self._getSetting('prefix', self.DEF_PREFIX, kwargs)
        self._suffix        = self._getSetting('suffix', self.DEF_SUFFIX, kwargs)
        self._major         = self._getSetting('major', self.DEF_MAJOR, kwargs)
        self._minor         = self._getSetting('minor', self.DEF_MINOR, kwargs)
        self._revision      = self._getSetting('revision', self.DEF_REVISION, kwargs)
        self._dateValue     = datetime.datetime.utcnow().strftime('%b.%d.%y')
        self._date          = self._getSetting('date', self._dateValue, kwargs)

#___________________________________________________________________________________________________ populate
    def populate(self):
        """Doc..."""
        settings = JSON.fromFile(CompilerDeckEnvironment.projectSettingsPath).get('VERSION')
        if not settings:
            settings = dict()

        self._major     = self._updateSetting(self._major, settings)
        self._minor     = self._updateSetting(self._minor, settings)
        self._prefix    = self._updateSetting(self._prefix, settings)
        self._revision  = self._updateSetting(self._revision, settings)

        # Only load the suffix value from file if the last date and the current date match.
        # Otherwise, the suffix should reset for the new day builds.
        lastDate        = self._updateSetting(self._date, settings)
        if lastDate.value == self._dateValue:
            self._suffix    = self._updateSetting(self._suffix, settings)
        else:
            self._suffix = self._SETTING_NT(self._suffix.key, self.DEF_SUFFIX, 0)

        self.makeUnique()

#___________________________________________________________________________________________________ echo
    def echo(self):
        print 'VERSION LABEL:', self.versionLabel
        print 'VERSION NUMBER:', self.versionNumber

#___________________________________________________________________________________________________ write
    def write(self):
        settings = JSON.fromFile(CompilerDeckEnvironment.projectSettingsPath)
        settings['VERSION'] = {
            'major':self._major.value,
            'minor':self._minor.value,
            'revision':self._revision.value,
            'prefix':self._prefix.value,
            'suffix':self._suffix.value,
            'date':self._date.value
        }
        JSON.toFile(CompilerDeckEnvironment.projectSettingsPath, settings, True)

        desktopAppXml = FileUtils.getContents(
            CompilerDeckEnvironment.desktopAppXmlFilePath, raiseErrors=True)
        iosAppXml     = FileUtils.getContents(
            CompilerDeckEnvironment.iosAppXmlFilePath, raiseErrors=True)
        androidAppXml = FileUtils.getContents(
            CompilerDeckEnvironment.androidAppXmlFilePath, raiseErrors=True)

        tagName       = 'versionLabel'
        value         = self.versionLabel
        desktopAppXml = self._setAppXmlValue(desktopAppXml, tagName, value)
        iosAppXml     = self._setAppXmlValue(iosAppXml, tagName, value)
        androidAppXml = self._setAppXmlValue(androidAppXml, tagName, value)

        tagName       = 'versionNumber'
        value         = self.versionNumber
        desktopAppXml = self._setAppXmlValue(desktopAppXml, tagName, value)
        iosAppXml     = self._setAppXmlValue(iosAppXml, tagName, value)
        androidAppXml = self._setAppXmlValue(androidAppXml, tagName, value)

        FileUtils.putContents(
            desktopAppXml, CompilerDeckEnvironment.desktopAppXmlFilePath, raiseErrors=True)
        FileUtils.putContents(
            iosAppXml, CompilerDeckEnvironment.iosAppXmlFilePath, raiseErrors=True)
        FileUtils.putContents(
            androidAppXml, CompilerDeckEnvironment.androidAppXmlFilePath, raiseErrors=True)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _setAppXmlValue
    def _setAppXmlValue(self, appXml, tagName, value):
        if value is None:
            value = appXml
        value = unicode(value)

        pattern = re.compile(self._TAG_PATTERN_DEF.replace('#TAG#', tagName))
        appXml  = pattern.sub(u'\g<open>' + value + u'\g<close>', appXml)
        return appXml

#___________________________________________________________________________________________________ _getAppXmlValue
    def _getAppXmlValue(self, appXml, tagName, currentValue):
        """Doc..."""
        if currentValue is not None:
            return unicode(currentValue)

        pattern = re.compile(self._TAG_PATTERN_DEF.replace('#TAG#', tagName))
        result  = pattern.search(appXml)
        if not result:
            return u''

        out = result.groupdict().get('value', None)
        return u'' if not out else out

#___________________________________________________________________________________________________ _putSetting
    def _putSetting(self, setting, value, setLevel):
        return self._SETTING_NT(setting.key, value, setLevel)

#___________________________________________________________________________________________________ _getSetting
    def _getSetting(self, key, defaultValue, kwargs):
        return self._SETTING_NT(
            key, ArgsUtils.get(key, defaultValue, kwargs), 1 if kwargs.has_key(key) else 0)

#___________________________________________________________________________________________________ _updateSetting
    def _updateSetting(self, setting, kwargs):
        return self._SETTING_NT(
            setting.key,
            ArgsUtils.get(setting.key, setting.value, kwargs),
            self._UNSET)

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


