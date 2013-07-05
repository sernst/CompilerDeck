# CompilerDeckMainWindow.py
# (C)2013
# Scott Ernst

import os
import re

from PySide import QtGui

from pyaid.file.FileUtils import FileUtils

from pyglass.windows.PyGlassWindow import PyGlassWindow

from CompilerDeck.views.compile.DeckCompileWidget import DeckCompileWidget
from CompilerDeck.views.home.DeckHomeWidget import DeckHomeWidget

#___________________________________________________________________________________________________ CompilerDeckMainWindow
class CompilerDeckMainWindow(PyGlassWindow):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _PROG_PATH          = 'C:\\Program Files (x86)\\'
    _PROG_64_PATH       = 'C:\\Program Files\\'
    _NUM_FINDER         = re.compile('[0-9]+')
    _JDK_PATH           = None

    _AIR_ROOT_PATH      = 'AIR_ROOT_PATH'
    _FLEX_SDK_PATH      = 'FLEX_SDK_PATH'
    _JAVA_ROOT_PATH     = 'JAVA_ROOT_PATH'
    _JAVA_ANT_PATH      = 'JAVA_ANT_PATH'
    _ANDROID_SDK_PATH   = 'ANDROID_SDK_PATH'

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
        self.setMinimumSize(820, 480)
        self.setContentsMargins(0, 0, 0, 0)

        widget = self._createCentralWidget()
        layout = QtGui.QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        widget.setLayout(layout)

        self.setActiveWidget('home')

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getRootAIRPath
    def getRootAIRPath(self, *args, **kwargs):
        """Doc..."""
        res = self.appConfig.get(self._AIR_ROOT_PATH)
        if not res:
            return ''

        return FileUtils.createPath(res, *args, **kwargs)

#___________________________________________________________________________________________________ setRootAIRPath
    def setRootAIRPath(self, path):
        """Doc..."""
        return self.appConfig.set(self._AIR_ROOT_PATH, path)

#___________________________________________________________________________________________________ getFlexSDKPath
    def getFlexSDKPath(self, *args, **kwargs):
        """Doc..."""
        res = self.appConfig.get(self._FLEX_SDK_PATH)
        if not res:
            return ''

        return FileUtils.createPath(res, *args, **kwargs)

#___________________________________________________________________________________________________ setFlexSDKPath
    def setFlexSDKPath(self, path):
        """Doc..."""
        return self.appConfig.set(self._FLEX_SDK_PATH, path)

#___________________________________________________________________________________________________ getJavaJDKPath
    def getJavaJDKPath(self, *args, **kwargs):
        """Doc..."""
        return self._getJDKPath(*args, **kwargs)

#___________________________________________________________________________________________________ getJavaAntPath
    def getJavaAntPath(self, *args, **kwargs):
        """Doc..."""
        res = self.appConfig.get(self._JAVA_ANT_PATH)
        if not res:
            return ''

        return FileUtils.createPath(res, *args, **kwargs)

#___________________________________________________________________________________________________ setJavaAntPath
    def setJavaAntPath(self, path):
        """Doc..."""
        return self.appConfig.set(self._JAVA_ANT_PATH, path)

#___________________________________________________________________________________________________ getAndroidSDKPath
    def getAndroidSDKPath(self, *args, **kwargs):
        """Doc..."""
        res = self.appConfig.get(self._ANDROID_SDK_PATH)
        if not res:
            return ''

        return FileUtils.createPath(res, *args, **kwargs)

#___________________________________________________________________________________________________ setAndroidSDKPath
    def setAndroidSDKPath(self, path):
        """Doc..."""
        return self.appConfig.set(self._ANDROID_SDK_PATH, path)

#___________________________________________________________________________________________________ listInstalledAirSDKs
    def listInstalledAirSDKs(self):
        out = []
        for item in os.listdir(self.getRootAIRPath()):
            try:
                float(item)
                out.append(item)
            except Exception, err:
                continue
        out.sort(reverse=True)
        return out

#___________________________________________________________________________________________________ listInstalledFlashPlayers
    def listInstalledFlashPlayers(self):
        out = []
        for item in os.listdir(self.getFlexSDKPath('frameworks', 'libs', 'player')):
            try:
                float(item)
                out.append(item)
            except Exception, err:
                continue
        out.sort(reverse=True)
        return out

#___________________________________________________________________________________________________ getJDKPath
    @classmethod
    def _getJDKPath(cls, *args, **kwargs):
        if cls._JDK_PATH is None:
            jdkPath   = None
            lastParts = [0, 0, 0, 0]
            for root in [cls._PROG_64_PATH, cls._PROG_PATH]:
                for p in os.listdir(FileUtils.createPath(root, 'java')):
                    if not p.lower().startswith('jdk'):
                        continue

                    parts = cls._NUM_FINDER.findall(p)
                    skip  = False
                    index = 0
                    while index < len(lastParts) and index < len(parts):
                        if parts[index] < lastParts[index]:
                            skip = True
                            break
                        index += 1

                    if not skip:
                        lastParts = parts
                        jdkPath   = FileUtils.createPath(cls._PROG_64_PATH, 'java', p)
            cls._JDK_PATH = jdkPath

        if cls._JDK_PATH is None:
            raise Exception, 'Unable to locate a Java Development Kit installation.'

        return FileUtils.createPath(cls._JDK_PATH, *args, **kwargs)
