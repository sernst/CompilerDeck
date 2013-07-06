# CompilerDeckCompiler.py
# (C)2013
# Scott Ernst

from pyglass.compile.PyGlassApplicationCompiler import PyGlassApplicationCompiler
from pyglass.compile.SiteLibraryEnum import SiteLibraryEnum

from CompilerDeck.CompilerDeckApplication import CompilerDeckApplication

#___________________________________________________________________________________________________ CompilerDeckCompiler
class CompilerDeckCompiler(PyGlassApplicationCompiler):
    """A class for..."""

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: siteLibraries
    @property
    def siteLibraries(self):
        return [SiteLibraryEnum.PYSIDE]

#___________________________________________________________________________________________________ GS: binPath
    @property
    def binPath(self):
        return ['..', '..', 'bin']

#___________________________________________________________________________________________________ GS: appFilename
    @property
    def appFilename(self):
        return 'CompilerDeck'

#___________________________________________________________________________________________________ GS: appDisplayName
    @property
    def appDisplayName(self):
        return 'CompilerDeck'

#___________________________________________________________________________________________________ GS: applicationClass
    @property
    def applicationClass(self):
        return CompilerDeckApplication

#___________________________________________________________________________________________________ GS: iconPath
    @property
    def iconPath(self):
        return ['apps', 'CompilerDeckApplication', 'icons']

####################################################################################################
####################################################################################################

if __name__ == '__main__':
    CompilerDeckCompiler().run()

