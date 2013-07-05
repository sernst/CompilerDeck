# DeckHomeWidget.py
# (C)2013
# Scott Ernst

from PySide import QtGui

from pyaid.file.FileUtils import FileUtils

from pyglass.widgets.PyGlassWidget import PyGlassWidget

from CompilerDeck.CompilerDeckEnvironment import CompilerDeckEnvironment
from CompilerDeck.views.dialogs.localSettings.LocalSettingsDialog import LocalSettingsDialog

#___________________________________________________________________________________________________ DeckHomeWidget
class DeckHomeWidget(PyGlassWidget):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _LAST_PROJECT_PATH = 'LAST_PROJECT_PATH'

#___________________________________________________________________________________________________ __init__
    def __init__(self, *args, **kwargs):
        """Creates a new instance of DeckHomeWidget."""
        super(DeckHomeWidget, self).__init__(*args, **kwargs)

        lastPath = self.appConfig.get(self._LAST_PROJECT_PATH, u'')

        self.openBtn.clicked.connect(self._handleOpenProject)
        self.openBtn.setEnabled(lastPath is not None)
        self.pathLine.setText(lastPath)

        self.settingsBtn.clicked.connect(self._handleSettings)
        self.browseBtn.clicked.connect(self._handleBrowseFolders)

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleBrowseFolders
    def _handleBrowseFolders(self):

        path = QtGui.QFileDialog.getExistingDirectory(
            self,
            'Select Project Folder',
            self.appConfig.get(self._LAST_PROJECT_PATH, u''))

        if not path:
            return

        path = FileUtils.cleanupPath(path, isDir=True)
        self.appConfig.set(self._LAST_PROJECT_PATH, path)
        self.pathLine.setText(path)
        self.openBtn.setEnabled(True)

#___________________________________________________________________________________________________ _handleOpenProject
    def _handleOpenProject(self):
        CompilerDeckEnvironment.setRootProjectPath(self.pathLine.text())
        self.mainWindow.setActiveWidget('compile')

#___________________________________________________________________________________________________ _handleSettings
    def _handleSettings(self):
        LocalSettingsDialog(self.mainWindow).open()
