# ANECompileThread.py
# (C)2012-2013
# Scott Ernst

from pyglass.threading.RemoteExecutionThread import RemoteExecutionThread

from CompilerDeck.adobe.air.AirCompiler import AirCompiler
from CompilerDeck.adobe.flex.FlexCompiler import FlexCompiler
from CompilerDeck.adobe.flex.FlexProjectData import FlexProjectData

#___________________________________________________________________________________________________ ANECompileThread
class ANECompileThread(RemoteExecutionThread):
    """ Threaded external processor execution"""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        RemoteExecutionThread.__init__(self, parent, **kwargs)
        self._flexData = FlexProjectData(**kwargs)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _runImpl
    def _runImpl(self):
        pd = self._flexData

        # FLASH
        usePlatform = pd.platformSelection.get(FlexProjectData.FLASH_PLATFORM, False)
        if usePlatform and pd.hasPlatform(FlexProjectData.FLASH_PLATFORM):
            pd.setPlatform(FlexProjectData.FLASH_PLATFORM)
            if not FlexCompiler(self.parent(), pd, logger=self._log).compile():
                return 1

        # AIR
        usePlatform = pd.platformSelection.get(FlexProjectData.AIR_PLATFORM, False)
        if usePlatform and pd.hasPlatform(FlexProjectData.AIR_PLATFORM):
            pd.setPlatform(FlexProjectData.AIR_PLATFORM)
            if not FlexCompiler(self.parent(), pd, logger=self._log).compile():
                return 1

            if not AirCompiler(self.parent(), pd, logger=self._log).compile():
                return 1

        # NATIVE
        usePlatform = pd.platformSelection.get(FlexProjectData.NATIVE_PLATFORM, False)
        if usePlatform and pd.hasPlatform(FlexProjectData.NATIVE_PLATFORM):
            pd.setPlatform(FlexProjectData.NATIVE_PLATFORM)
            if not FlexCompiler(self.parent(), pd, logger=self._log).compile():
                return 1

            if not AirCompiler(self.parent(), pd, logger=self._log).compile():
                return 1

        # ANDROID
        usePlatform = pd.platformSelection.get(FlexProjectData.ANDROID_PLATFORM, False)
        if usePlatform and pd.hasPlatform(FlexProjectData.ANDROID_PLATFORM):
            pd.setPlatform(FlexProjectData.ANDROID_PLATFORM)
            if not FlexCompiler(self.parent(), pd, logger=self._log).compile():
                return 1

            if not AirCompiler(self.parent(), pd, logger=self._log).compile():
                return 1

        # IOS
        usePlatform = pd.platformSelection.get(FlexProjectData.IOS_PLATFORM, False)
        if usePlatform and pd.hasPlatform(FlexProjectData.IOS_PLATFORM):
            pd.setPlatform(FlexProjectData.IOS_PLATFORM)
            if not FlexCompiler(self.parent(), pd, logger=self._log).compile():
                return 1

            if not AirCompiler(self.parent(), pd, logger=self._log).compile():
                return 1

        return 0
