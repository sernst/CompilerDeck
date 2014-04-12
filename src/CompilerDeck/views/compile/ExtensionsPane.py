# ExtensionsPane.py
# (C)2014
# Scott Ernst

import os

from pyaid.file.FileUtils import FileUtils
from pyaid.json.JSON import JSON

from pyglass.elements.DataListWidgetItem import DataListWidgetItem

from CompilerDeck.CompilerDeckEnvironment import CompilerDeckEnvironment

#___________________________________________________________________________________________________ ExtensionsPane
from CompilerDeck.adobe.extensions.NativeExtensionRemoteThread import NativeExtensionRemoteThread
from CompilerDeck.adobe.flex.FlexProjectData import FlexProjectData


class ExtensionsPane(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, widget):
        """Creates a new instance of ExtensionsPane."""
        self.widget     = widget
        self._settings  = dict()

        self.widget.aneCompileBtn.clicked.connect(self._handleCompile)
        self.widget.anePackageBtn.clicked.connect(self._handlePackage)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ activate
    def activate(self):
        """Doc..."""
        self.widget.aneList.clear()

        path = CompilerDeckEnvironment.getProjectPath('NativeExtensions', isDir=True)
        for item in os.listdir(path):
            itemPath = FileUtils.createPath(path, item)
            if not os.path.isdir(itemPath):
                continue

            settingsPath = FileUtils.createPath(itemPath, 'compiler', 'settings.vcd', isFile=True)
            if not os.path.exists(settingsPath):
                continue

            settings = JSON.fromFile(settingsPath)
            if not settings:
                continue

            DataListWidgetItem(settings.get('LABEL', item), self.widget.aneList, ident=item, data={
                'folder':item,
                'path':itemPath,
                'settings':settings })

        self.widget.aneList.sortItems()

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getSelectedAne
    def _getSelectedAne(self):
        """Doc..."""
        out = self.widget.aneList.selectedItems()
        if not out:
            return None
        return out[0]

#___________________________________________________________________________________________________ _doCompile
    def _doCompile(self, doPackage =False):
        item = self._getSelectedAne()
        if not item:
            return False

        data     = item.itemData
        sets     = FlexProjectData(
            data['path'],
            versionInfo=data['settings'].get('VERSION', dict()))

        thread = NativeExtensionRemoteThread(self.widget, sets, package=doPackage)
        self.widget.executeRemoteThread(thread, completeCallback=self._handleRemoteThreadComplete)
        return True

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleCompile
    def _handleCompile(self):
        self._doCompile(False)

#___________________________________________________________________________________________________ _handlePackage
    def _handlePackage(self):
        self._doCompile(True)

#___________________________________________________________________________________________________ _handlePackageComplete
    def _handleRemoteThreadComplete(self, result):
        self.widget.remoteThreadResult(result)

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
