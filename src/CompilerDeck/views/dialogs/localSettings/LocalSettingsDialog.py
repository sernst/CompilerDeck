# LocalSettingsDialog.py
# (C)2012-2013
# Scott Ernst

from pyglass.dialogs.PyGlassDialog import PyGlassDialog

from CompilerDeck.views.dialogs.localSettings.LocalSettingsWidget import LocalSettingsWidget

#___________________________________________________________________________________________________ LocalSettingsDialog
class LocalSettingsDialog(PyGlassDialog):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent =None, **kwargs):
        """Creates a new instance of PyGlassWindow."""

        PyGlassDialog.__init__(
            self,
            parent,
            title='Modify Environment Paths',
            widget=LocalSettingsWidget,
            **kwargs
        )
