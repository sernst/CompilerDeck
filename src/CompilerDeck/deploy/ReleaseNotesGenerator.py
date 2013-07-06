# ReleaseNotesGenerator.py
# (C)2013
# Scott Ernst

#___________________________________________________________________________________________________ ReleaseNotesGenerator
class ReleaseNotesGenerator(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, owner, label, versionInfo, **kwargs):
        """Creates a new instance of ReleaseNotesGenerator."""
        self._owner          = owner
        self._label          = label
        self._versionInfo    = versionInfo
        self._summary        = None
        self._additions      = []
        self._fixes          = []
        self._removals       = []
        self._additionalInfo = None
        self.populate(**kwargs)

        self._output = None

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: text
    @property
    def text(self):
        return self._output
    @text.setter
    def text(self, value):
        pass

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ generate
    def generate(self, **kwargs):
        if kwargs:
            self.populate(**kwargs)

        self._output = (u"""%s Release\nVersion: %s.%s.%s\nID: %s-%s-%s\n%s%s%s%s%s""" % (
            self._label if self._label else u'Application',
            self._versionInfo.get('major', u'0'),
            self._versionInfo.get('minor', u'0'),
            self._versionInfo.get('revision', u'0'),
            self._versionInfo.get('prefix', u''),
            self._versionInfo.get('date', u'???'),
            self._versionInfo.get('suffix', u''),
            (u'\n\n' + self._summary) if self._summary else u'',
            self._getTextList(self._additions, u'+', u'New Additions'),
            self._getTextList(self._fixes, u'*', u'Changes & Fixes'),
            self._getTextList(self._removals, u'-', u'Removals'),
            self._getSection(self._additionalInfo, u'Build Information')
        )).strip()

        return self._output

#___________________________________________________________________________________________________ populate
    def populate(
            self, label =None, versionInfo =None, summary =None, additions =None, fixes =None,
            removals =None, info =None
    ):
        """Doc..."""
        if label is not None:
            self._label = label
        if versionInfo is not None:
            self._versionInfo = versionInfo
        if summary is not None:
            self._summary = summary.strip()
        if additions is not None:
            self._additions = self._createArrayFromString(additions)
        if fixes is not None:
            self._fixes = self._createArrayFromString(fixes)
        if removals is not None:
            self._removals = self._createArrayFromString(removals)
        if info is not None:
            self._additionalInfo = info.strip()

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getSection
    def _getSection(self, source, header):
        if not source:
            return u''
        return u'\n\n--- ' + header + u' ---\n' + source

#___________________________________________________________________________________________________ _getTextList
    def _getTextList(self, source, bullet, header):
        if not source:
            return u''

        out = []
        for item in source:
            out.append(u'    ' + bullet + u' ' + item)
        return self._getSection(u'\n'.join(out), header)

#___________________________________________________________________________________________________ _createArrayFromString
    def _createArrayFromString(self, source):
        """Doc..."""
        if isinstance(source, basestring):
            source = source.replace('\r', '').strip().split('\n')

        for i in range(len(source)):
            source[i] = source[i].strip().replace('\t', '    ')

        return source

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
