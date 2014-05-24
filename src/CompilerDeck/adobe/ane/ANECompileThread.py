# ANECompileThread.py
# (C)2012-2013
# Scott Ernst

import os
import imp
import time

from pyaid.ArgsUtils import ArgsUtils
from pyaid.OsUtils import OsUtils
from pyaid.file.FileUtils import FileUtils

from pyglass.threading.RemoteExecutionThread import RemoteExecutionThread

from CompilerDeck.adobe.air.AirCompiler import AirCompiler
from CompilerDeck.adobe.flex.FlexCompiler import FlexCompiler
from CompilerDeck.adobe.flex.FlexProjectData import FlexProjectData
from CompilerDeck.deploy.BuildPackageUploader import BuildPackageUploader

#___________________________________________________________________________________________________ ANECompileThread
class ANECompileThread(RemoteExecutionThread):
    """ Threaded external processor execution"""

#===================================================================================================
#                                                                                       C L A S S

    STAGE_COMPLETE = 'stageComplete'

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        RemoteExecutionThread.__init__(self, parent, explicitComplete=True, **kwargs)
        self._pausePackageSteps     = ArgsUtils.extract('pausePackageSteps', False, kwargs)
        self._uploadAfterPackage    = ArgsUtils.extract('uploadAfterPackage', False, kwargs)
        self._flexData              = FlexProjectData(**kwargs)
        self._queue                 = []
        self._isProcessingQueue     = False
        self._isAbortingQueue       = False
        self._bucket                = None
        self._output                = dict()

        if self._uploadAfterPackage:
            self._output['urls'] = dict()
            self._bucket = self._flexData.createBucket()

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
        useWindows  = pd.isPlatformActive(FlexProjectData.WINDOWS_PLATFORM) and OsUtils.isWindows()
        useMac      = pd.isPlatformActive(FlexProjectData.MAC_PLATFORM) and OsUtils.isMac()
        useAndroid  = pd.isPlatformActive(FlexProjectData.ANDROID_PLATFORM)
        useIOS      = pd.isPlatformActive(FlexProjectData.IOS_PLATFORM)

        # In cases where nothing was set (usual because debugging will be run on the default
        # platform) pick the platform to compile if such a platform exists
        useAny = useFlash or useAir or useWindows or useMac or useAndroid or useIOS
        if not useAny:
            if pd.hasPlatform(FlexProjectData.AIR_PLATFORM):
                useAir = True
            elif pd.hasPlatform(FlexProjectData.WINDOWS_PLATFORM) and OsUtils.isWindows():
                useWindows = True
            elif pd.hasPlatform(FlexProjectData.MAC_PLATFORM) and OsUtils.isMac():
                useMac = True
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
            pid = FlexProjectData.FLASH_PLATFORM
            q.append([self._doCompile, pid, 'Flash SWF Compiled'])
            if self._uploadAfterPackage:
                q.append([self._doUpload, pid, 'Flash'])

        if useAir:
            pid = FlexProjectData.AIR_PLATFORM
            q.append([self._doCompile, pid, 'Air SWF Compiled'])
            q.append([self._doPackage, pid, 'Air Packaged'])
            if self._uploadAfterPackage:
                q.append([self._doUpload, pid, 'Air'])

        if useWindows:
            pid = FlexProjectData.WINDOWS_PLATFORM
            q.append([self._doCompile, pid, 'Windows SWF Compiled'])
            q.append([self._doPackage, pid, 'Windows Packaged'])
            if self._uploadAfterPackage:
                q.append([self._doUpload, pid, 'Windows'])

        if useMac:
            pid = FlexProjectData.MAC_PLATFORM
            q.append([self._doCompile, pid, 'Mac SWF Compiled'])
            q.append([self._doPackage, pid, 'Mac Packaged'])
            if self._uploadAfterPackage:
                q.append([self._doUpload, pid, 'Mac'])

        if useAndroid:
            pid = FlexProjectData.ANDROID_PLATFORM
            q.append([self._doCompile, pid, 'Android SWF Compiled'])
            q.append([self._doPackage, pid, 'Android Packaged'])
            if self._uploadAfterPackage:
                q.append([self._doUpload, pid, 'Android'])

        if useIOS:
            pid = FlexProjectData.IOS_PLATFORM
            q.append([self._doCompile, pid, 'iOS SWF Compiled'])
            q.append([self._doPackage, pid, 'iOS Packaged'])
            if self._uploadAfterPackage:
                q.append([self._doUpload, pid, 'iOS'])

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

        self._log.write('<h2>Compilation/Packaging Complete</h2>')
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

#___________________________________________________________________________________________________ _doUpload
    def _doUpload(self, platformID, uploadMessage):
        uploader = BuildPackageUploader(self._flexData, self._bucket)
        self._log.write('<hr /><h1>Uploading Package: ' + uploadMessage + '</h1><hr />')
        url = uploader.upload(platformID)
        if url is None:
            self._log.write('<h2>UPLOAD FAILED!</h2>')
            raise Exception, 'Failed to upload file. Compilation/Packaging Process Aborted'
        else:
            self._output['urls'][platformID] = url
            self._log.write('<h2>Upload Success:</h2><a href="%s">%s</a>' % (url, url))

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
        setattr(module, 'logger', self._log)
        setattr(module, 'flexProjectData', self._flexData)
        exec script in module.__dict__
        self._log.write('Post build script execution complete')
