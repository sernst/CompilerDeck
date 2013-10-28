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
        pd          = self._flexData
        useFlash    = pd.isPlatformActive(FlexProjectData.FLASH_PLATFORM)
        useAir      = pd.isPlatformActive(FlexProjectData.AIR_PLATFORM)
        useNative   = pd.isPlatformActive(FlexProjectData.NATIVE_PLATFORM)
        useAndroid  = pd.isPlatformActive(FlexProjectData.ANDROID_PLATFORM)
        useIOS      = pd.isPlatformActive(FlexProjectData.IOS_PLATFORM)

        # In cases where nothing was set (usual because debugging will be run on the default
        # platform) pick the platform to compile if such a platform exists
        useAny = useFlash or useAir or useNative or useAndroid or useIOS
        if not useAny:
            if pd.hasPlatform(FlexProjectData.AIR_PLATFORM):
                useAir = True
            elif pd.hasPlatform(FlexProjectData.NATIVE_PLATFORM):
                useNative = True
            elif pd.hasPlatform(FlexProjectData.FLASH_PLATFORM):
                useFlash = True
            elif pd.hasPlatform(FlexProjectData.ANDROID_PLATFORM):
                useAndroid = True
            elif pd.hasPlatform(FlexProjectData.IOS_PLATFORM):
                useIOS = True
            else:
                return 1

        if useFlash:
            pd.setPlatform(FlexProjectData.FLASH_PLATFORM)
            if not FlexCompiler(self.parent(), pd, logger=self._log).compile():
                return 1

        if useAir:
            pd.setPlatform(FlexProjectData.AIR_PLATFORM)
            if not FlexCompiler(self.parent(), pd, logger=self._log).compile():
                return 1

            if not AirCompiler(self.parent(), pd, logger=self._log).compile():
                return 1

        if useNative:
            pd.setPlatform(FlexProjectData.NATIVE_PLATFORM)
            if not FlexCompiler(self.parent(), pd, logger=self._log).compile():
                return 1

            if not AirCompiler(self.parent(), pd, logger=self._log).compile():
                return 1

        if useAndroid:
            pd.setPlatform(FlexProjectData.ANDROID_PLATFORM)
            if not FlexCompiler(self.parent(), pd, logger=self._log).compile():
                return 1

            if not AirCompiler(self.parent(), pd, logger=self._log).compile():
                return 1

        if useIOS:
            pd.setPlatform(FlexProjectData.IOS_PLATFORM)
            if not FlexCompiler(self.parent(), pd, logger=self._log).compile():
                return 1

            if not AirCompiler(self.parent(), pd, logger=self._log).compile():
                return 1

        return 0
