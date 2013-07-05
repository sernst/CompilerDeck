# AdobeSystemCompiler.py
# (C)2012-2013
# Scott Ernst

from CompilerDeck.adobe.SystemCompiler import SystemCompiler

#___________________________________________________________________________________________________ AdobeSystemCompiler
class AdobeSystemCompiler(SystemCompiler):
    """A class for..."""

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getStringDefinition
    def _getStringDefinition(self, name, value):
        return '--define=CONFIG::%s,%s' % (name, str(value))

#___________________________________________________________________________________________________ _getBooleanDefinition
    def _getBooleanDefinition(self, name, value, ifTrue ='true', ifFalse = 'false'):
        return self._getStringDefinition(name, self._getAsBooleanString(value, ifTrue, ifFalse))

#___________________________________________________________________________________________________ _getAsBooleanString
    def _getAsBooleanString(self, value, ifTrue ='true', ifFalse ='false'):
        return ifTrue if value else ifFalse
