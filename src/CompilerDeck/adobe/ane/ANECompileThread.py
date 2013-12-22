# ANECompileThread.py
# (C)2012-2013
# Scott Ernst

import os
import imp
import time

from pyaid.ArgsUtils import ArgsUtils
from pyaid.file.FileUtils import FileUtils

from pyglass.threading.RemoteExecutionThread import RemoteExecutionThread

from CompilerDeck.adobe.air.AirCompiler import AirCompiler
from CompilerDeck.adobe.flex.FlexCompiler import FlexCompiler
from CompilerDeck.adobe.flex.FlexProjectData import FlexProjectData

#___________________________________________________________________________________________________ ANECompileThread
class ANECompileThread(RemoteExecutionThread):
    """ Threaded external processor execution"""

#===================================================================================================
#                                                                                       C L A S S

    STAGE_COMPLETE = 'stageComplete'

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        RemoteExecutionThread.__init__(self, parent, explicitComplete=True, **kwargs)
        self._pausePackageSteps = ArgsUtils.get('pausePackageSteps', False, kwargs)
        self._flexData          = FlexProjectData(**kwargs)
        self._queue             = []
        self._isProcessingQueue = False
        self._isAbortingQueue   = False

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ resumeQueueProcessing
    def resumeQueueProcessing(self):
        self._isProcessingQueue = True

#___________________________________________________________________________________________________ abortQueueProcessing
    def abortQueueProcessing(self):
        self._isAbortingQueue = True

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
                self._runComplete(1)
                return

        q = self._queue

        if useFlash:
            q.append([self._doCompile, FlexProjectData.FLASH_PLATFORM, 'Flash SWF Compiled'])

        if useAir:
            q.append([self._doCompile, FlexProjectData.AIR_PLATFORM, 'Air SWF Compiled'])
            q.append([self._doPackage, FlexProjectData.AIR_PLATFORM, 'Air Packaged'])

        if useNative:
            q.append([self._doCompile, FlexProjectData.NATIVE_PLATFORM, 'Native SWF Compiled'])
            q.append([self._doPackage, FlexProjectData.NATIVE_PLATFORM, 'Native Packaged'])

        if useAndroid:
            q.append([self._doCompile, FlexProjectData.ANDROID_PLATFORM, 'Android SWF Compiled'])
            q.append([self._doPackage, FlexProjectData.ANDROID_PLATFORM, 'Android Packaged'])

        if useIOS:
            q.append([self._doCompile, FlexProjectData.IOS_PLATFORM, 'iOS SWF Compiled'])
            q.append([self._doPackage, FlexProjectData.IOS_PLATFORM, 'iOS Packaged'])

        self._isProcessingQueue = True
        while self._queue:
            if self._isAbortingQueue:
                self._runComplete(1)
                return

            if not self._isProcessingQueue:
                time.sleep(1)
                continue

            # Get the first item in the list and execute it
            try:
                item = self._queue.pop(0)
                item[0](item[1], item[2])
            except Exception, err:
                self._log.writeError('Failed Compilation/Package Step', err)
                self._runComplete(1)
                return

        self._runComplete(0)

#___________________________________________________________________________________________________ _doCompile
    def _doCompile(self, platformID, pauseMessage):
        if not self._flexData.compileSwf:
            return

        self._flexData.setPlatform(platformID)

        if not FlexCompiler(self.parent(), self._flexData, logger=self._log).compile():
            raise Exception, 'Swf Compilation Failed'

        self._executeBuildScript('postCompile')

        if not self._notifyPause('Compilation', pauseMessage):
            raise Exception, 'Compilation/Packaging Process Aborted'

#___________________________________________________________________________________________________ _doPackage
    def _doPackage(self, platformID, pauseMessage):
        if not self._flexData.packageAir:
            return

        self._flexData.setPlatform(platformID)

        if not AirCompiler(self.parent(), self._flexData, logger=self._log).compile():
            raise Exception, 'Air Packaging Failed'

        self._executeBuildScript('postPackage')

        if not self._notifyPause('Packaging', pauseMessage):
            raise Exception, 'Compilation/Packaging Process Aborted'

#___________________________________________________________________________________________________ _notifyPause
    def _notifyPause(self, actionType, message):
        if not self._pausePackageSteps:
            return True

        self._isProcessingQueue = False
        self.dispatchEvent(self.STAGE_COMPLETE, data={'message':message, 'type':actionType})
        return True

#___________________________________________________________________________________________________ _executeBuildScript
    def _executeBuildScript(self, scriptName):
        pd = self._flexData

        scriptsPath = FileUtils.createPath(pd.projectPath, 'compiler', 'scripts', isDir=True)
        if not os.path.exists(scriptsPath):
            return False

        typePath = FileUtils.createPath(scriptsPath, self._flexData.buildTypeFolderName, isDir=True)
        if not os.path.exists(typePath):
            return False

        platformPath = FileUtils.createPath(typePath, pd.currentPlatformID.lower(), isDir=True)
        if not os.path.exists(platformPath):
            return False

        targetPath = FileUtils.createPath(platformPath, scriptName, isFile=True)
        if not os.path.exists(targetPath):
            targetPath += '.py'
            if not os.path.exists(targetPath):
                return False

        self._log.write('Running post build script: ' + scriptName)
        f = open(targetPath, 'r')
        script = f.read()
        f.close()

        module = imp.new_module('postBuildScriptModule')
        setattr(module, '__file__', targetPath)
        setattr(module, 'flexProjectData', self._flexData)
        exec script in module.__dict__
        self._log.write('Post build script execution complete')
