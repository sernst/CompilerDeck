# ANECompileThread.py
# (C)2012-2013
# Scott Ernst

from pyaid.ArgsUtils import ArgsUtils

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
        self._projectPath   = ArgsUtils.get('projectPath', None, kwargs)
        self._debug         = ArgsUtils.get('debug', False, kwargs)
        self._live          = ArgsUtils.get('live', False, kwargs)
        self._airVersion    = ArgsUtils.get('airVersion', None, kwargs)
        self._flashVersion  = ArgsUtils.get('flashVersion', None, kwargs)
        self._packageAir    = ArgsUtils.get('packageAir', False, kwargs)
        self._autoVersion   = ArgsUtils.get('autoVersion', False, kwargs)
        self._usbDebug      = ArgsUtils.get('usbDebug', False, kwargs)
        self._remoteDebug   = ArgsUtils.get('remoteDebug', self._usbDebug, kwargs)
        self._platforms     = ArgsUtils.get('platforms', {}, kwargs)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _runImpl
    def _runImpl(self):
        pd = FlexProjectData(
            projectPath=self._projectPath,
            debug=self._debug,
            live=self._live,
            airVersion=self._airVersion,
            flashVersion=self._flashVersion,
            quickCompile=self._quickCompile,
            packageAir=self._packageAir,
            remoteDebug=self._remoteDebug,
            usbDebug=self._usbDebug
        )

        # FLASH
        usePlatform = self._platforms.get(FlexProjectData.FLASH_PLATFORM, False)
        if usePlatform and pd.hasPlatform(FlexProjectData.FLASH_PLATFORM):
            pd.setPlatform(FlexProjectData.FLASH_PLATFORM)
            if not FlexCompiler(pd, logger=self._log).compile():
                return 1

        # AIR
        usePlatform = self._platforms.get(FlexProjectData.AIR_PLATFORM, False)
        if usePlatform and pd.hasPlatform(FlexProjectData.AIR_PLATFORM):
            pd.setPlatform(FlexProjectData.AIR_PLATFORM)
            if not FlexCompiler(pd, logger=self._log).compile():
                return 1

            if not AirCompiler(pd, logger=self._log).compile():
                return 1

        # NATIVE
        usePlatform = self._platforms.get(FlexProjectData.NATIVE_PLATFORM, False)
        if usePlatform and pd.hasPlatform(FlexProjectData.NATIVE_PLATFORM):
            pd.setPlatform(FlexProjectData.NATIVE_PLATFORM)
            if not FlexCompiler(pd, logger=self._log).compile():
                return 1

            if not AirCompiler(pd, logger=self._log).compile():
                return 1

        # ANDROID
        usePlatform = self._platforms.get(FlexProjectData.ANDROID_PLATFORM, False)
        if usePlatform and pd.hasPlatform(FlexProjectData.ANDROID_PLATFORM):
            pd.setPlatform(FlexProjectData.ANDROID_PLATFORM)
            if not FlexCompiler(pd, logger=self._log).compile():
                return 1

            if not AirCompiler(pd, logger=self._log).compile():
                return 1

        # IOS
        usePlatform = self._platforms.get(FlexProjectData.IOS_PLATFORM, False)
        if usePlatform and pd.hasPlatform(FlexProjectData.IOS_PLATFORM):
            pd.setPlatform(FlexProjectData.IOS_PLATFORM)
            if not FlexCompiler(pd, logger=self._log).compile():
                return 1

            if not AirCompiler(pd, logger=self._log).compile():
                return 1

        return 0
