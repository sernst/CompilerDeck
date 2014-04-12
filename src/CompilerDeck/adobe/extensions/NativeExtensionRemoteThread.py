# NativeExtensionRemoteThread.py
# (C)2014
# Scott Ernst

from pyglass.threading.RemoteExecutionThread import RemoteExecutionThread

#___________________________________________________________________________________________________ NativeExtensionRemoteThread
from CompilerDeck.adobe.extensions.NativeExtensionCompiler import NativeExtensionCompiler
from CompilerDeck.adobe.flex.FlexProjectData import FlexProjectData
from CompilerDeck.adobe.flex.SWCCompiler import SWCCompiler


class NativeExtensionRemoteThread(RemoteExecutionThread):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, settings, **kwargs):
        """Creates a new instance of NativeExtensionRemoteThread."""
        super(NativeExtensionRemoteThread, self).__init__(parent, **kwargs)
        self._settings = settings
        self._package  = kwargs.get('package', True)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _runImpl
    def _runImpl(self):
        """Doc..."""

        sets = self._settings
        if sets.setPlatform(FlexProjectData.DEFAULT_PLATFORM):
            swcCompiler = SWCCompiler(self.parent(), self._settings, logger=self._log)
            if not swcCompiler.compile():
                return 1

        if sets.setPlatform(FlexProjectData.WINDOWS_PLATFORM):
            swcCompiler = SWCCompiler(self.parent(), self._settings, logger=self._log)
            if not swcCompiler.compile():
                return 1

        if sets.setPlatform(FlexProjectData.MAC_PLATFORM):
            swcCompiler = SWCCompiler(self.parent(), self._settings, logger=self._log)
            if not swcCompiler.compile():
                return 1

        if sets.setPlatform(FlexProjectData.ANDROID_PLATFORM):
            swcCompiler = SWCCompiler(self.parent(), self._settings, logger=self._log)
            if not swcCompiler.compile():
                return 1

        if sets.setPlatform(FlexProjectData.IOS_PLATFORM):
            swcCompiler = SWCCompiler(self.parent(), self._settings, logger=self._log)
            if not swcCompiler.compile():
                return 1

        if not self._package:
            return 0

        packager = NativeExtensionCompiler(self.parent(), self._settings, logger=self._log)
        if not packager.compile():
            return 1

        return 0
