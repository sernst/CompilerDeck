# CompilerDeckMainWindow.py
# (C)2013
# Scott Ernst

from PySide import QtGui

from pyglass.windows.PyGlassWindow import PyGlassWindow

from CompilerDeck.views.compile.DeckCompileWidget import DeckCompileWidget
from CompilerDeck.views.home.DeckHomeWidget import DeckHomeWidget

#___________________________________________________________________________________________________ CompilerDeckMainWindow
class CompilerDeckMainWindow(PyGlassWindow):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, **kwargs):
        PyGlassWindow.__init__(
            self,
            widgets={
                'home':DeckHomeWidget,
                'compile':DeckCompileWidget
            },
            title='ActionScript Compiler Deck',
            **kwargs
        )
        self.setMinimumSize(1020, 600)
        self.setContentsMargins(0, 0, 0, 0)

        widget = self._createCentralWidget()
        layout = QtGui.QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        widget.setLayout(layout)

        self.setActiveWidget('home')
