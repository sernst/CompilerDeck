# DeployBuildDialog.py
# (C)2014
# Scott Ernst

from pyglass.dialogs.PyGlassDialog import PyGlassDialog

from CompilerDeck.views.dialogs.deploy.DeployWidget import DeployWidget

#___________________________________________________________________________________________________ DeployBuildDialog
class DeployBuildDialog(PyGlassDialog):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent =None, **kwargs):
        """Creates a new instance of PyGlassWindow."""

        PyGlassDialog.__init__(
            self,
            parent,
            title='Build Deployment Settings',
            widget=DeployWidget,
            **kwargs)
