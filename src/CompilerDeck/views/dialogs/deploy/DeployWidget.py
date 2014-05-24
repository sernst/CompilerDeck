# DeployWidget.py
# (C)2014
# Scott Ernst

from pyglass.elements.PyGlassElementUtils import PyGlassElementUtils

from pyglass.widgets.PyGlassWidget import PyGlassWidget

#___________________________________________________________________________________________________ DeployWidget
class DeployWidget(PyGlassWidget):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of DeployWidget."""
        PyGlassWidget.__init__(self, parent, **kwargs)

        self.deployBtn.clicked.connect(self._handleDeployClick)
        self.cancelBtn.clicked.connect(self._handleCancelClick)

        self._canceled = True
        self._includeEmails = False
        self._buildMessage = u''

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: canceled
    @property
    def canceled(self):
        return self._canceled

#___________________________________________________________________________________________________ GS: includeEmails
    @property
    def includeEmails(self):
        return self._includeEmails

#___________________________________________________________________________________________________ GS: buildMessage
    @property
    def buildMessage(self):
        return self._buildMessage

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _activateWidgetDisplayImpl
    def _activateWidgetDisplayImpl(self, **kwargs):
        PyGlassElementUtils.setCheckState(self.emailCheck, True)

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleCompileClick
    def _handleDeployClick(self, *args, **kwargs):
        self._buildMessage = self.messageText.toPlainText()
        self._includeEmails = self.emailCheck.isChecked()
        self._canceled = False
        self.parent().close()

#___________________________________________________________________________________________________ _handleCancelClick
    def _handleCancelClick(self, *args, **kwargs):
        self._buildMessage = u''
        self._includeEmails = False
        self._canceled = True
        self.parent().close()

