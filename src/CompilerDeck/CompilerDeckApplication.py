# CompilerDeckApplication.py
# (C)2013
# Scott Ernst

from pyglass.app.PyGlassApplication import PyGlassApplication

#___________________________________________________________________________________________________ CompilerDeckApplication
class CompilerDeckApplication(PyGlassApplication):

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: debugRootResourcePath
    @property
    def debugRootResourcePath(self):
        return ['..', '..', 'resources']

#___________________________________________________________________________________________________ GS: appGroupID
    @property
    def appGroupID(self):
        return 'compilerDeck'

#___________________________________________________________________________________________________ GS: mainWindowClass
    @property
    def mainWindowClass(self):
        from CompilerDeck.CompilerDeckMainWindow import CompilerDeckMainWindow
        return CompilerDeckMainWindow

####################################################################################################
####################################################################################################

if __name__ == '__main__':
    CompilerDeckApplication().run()
