# LocalSettingsWidget.py
# (C)2012-2013
# Scott Ernst

from PySide.QtGui import *

from pyglass.widgets.PyGlassWidget import PyGlassWidget

#___________________________________________________________________________________________________ LocalSettingsWidget
class LocalSettingsWidget(PyGlassWidget):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of LocalSettingsWidget."""
        PyGlassWidget.__init__(self, parent, **kwargs)

        self.saveBtn.clicked.connect(self._handleSaveClick)
        self.cancelBtn.clicked.connect(self._handleCancelClick)

        self.airLineEdit.setText(self.mainWindow.getRootAIRPath(allowEmpty=True))
        self.airToolBtn.clicked.connect(self._handleBrowseAirRootPath)

        self.flexLineEdit.setText(self.mainWindow.getFlexSDKPath(allowEmpty=True))
        self.flexToolBtn.clicked.connect(self._handleBrowseFlexPath)

        self.androidLineEdit.setText(self.mainWindow.getAndroidSDKPath(allowEmpty=True))
        self.androidToolBtn.clicked.connect(self._handleBrowseAndroidPath)

        self.antLineEdit.setText(self.mainWindow.getJavaAntPath(allowEmpty=True))
        self.antToolBtn.clicked.connect(self._handleBrowseAntPath)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _browseForPath
    def _browseForPath(self, lineWidget, title):
        result = QFileDialog.getExistingDirectory(self.parent(), title)
        if result:
            lineWidget.setText(result)

#___________________________________________________________________________________________________ _browseForFile
    def _browseForFile(self, lineWidget, title, filter =None):
        result = QFileDialog.getOpenFileName(
            self.parent(),
            title,
            filter=(filter if filter else u'')
        )

        if result and result[0]:
            try:
                lineWidget.setText(result[0])
            except Exception, err:
                print 'Invalid result:',result

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleCompileClick
    def _handleSaveClick(self, *args, **kwargs):
        self.mainWindow.setRootAIRPath(self.airLineEdit.text())
        self.mainWindow.setFlexSDKPath(self.flexLineEdit.text())
        self.mainWindow.setAndroidSDKPath(self.androidLineEdit.text())
        self.mainWindow.setJavaAntPath(self.antLineEdit.text())
        self.parent().close()

#___________________________________________________________________________________________________ _handleCancelClick
    def _handleCancelClick(self, *args, **kwargs):
        self.parent().close()

#___________________________________________________________________________________________________ _handleBrowseAirRootPath
    def _handleBrowseAirRootPath(self, *args, **kwargs):
        self._browseForPath(self.airLineEdit, 'Select Adobe AIR Path')

#___________________________________________________________________________________________________ _handleBrowseFlexPath
    def _handleBrowseFlexPath(self, *args, **kwargs):
        self._browseForPath(self.flexLineEdit, 'Select Flex SDK Path')

#___________________________________________________________________________________________________ _handleBrowseAndroidPath
    def _handleBrowseAndroidPath(self, *args, **kwargs):
        self._browseForPath(self.androidLineEdit, 'Select Android SDK Path')

#___________________________________________________________________________________________________ _handleBrowseAntPath
    def _handleBrowseAntPath(self, *args, **kwargs):
        self._browseForPath(self.antLineEdit, 'Select Java Ant Path')

