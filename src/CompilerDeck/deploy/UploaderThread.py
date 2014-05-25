# UploaderThread.py
# (C)2014
# Scott Ernst

from pyglass.threading.RemoteExecutionThread import RemoteExecutionThread

from CompilerDeck.adobe.flex.FlexProjectData import FlexProjectData
from CompilerDeck.deploy.BuildPackageUploader import BuildPackageUploader

#___________________________________________________________________________________________________ UploaderThread
class UploaderThread(RemoteExecutionThread):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, snapshot, **kwargs):
        """Creates a new instance of UploaderThread."""
        super(UploaderThread, self).__init__(parent, **kwargs)
        self._snapshot = snapshot
        self._output = {'urls':dict()}

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _runImpl
    def _runImpl(self):
        """Doc..."""

        self._log.write('<h1>Beginning Uploads...</h1>')

        projectData = FlexProjectData(**self._snapshot)

        for pid,active in self._snapshot['platforms'].iteritems():
            if not active or pid in self._snapshot['platformUploads']:
                continue

            label = 'Unkown'
            if pid == FlexProjectData.MAC_PLATFORM:
                label = 'Mac'
            elif pid == FlexProjectData.WINDOWS_PLATFORM:
                label = 'Windows'
            elif pid == FlexProjectData.ANDROID_PLATFORM:
                label = 'Android'
            elif pid == FlexProjectData.IOS_PLATFORM:
                label = 'iOS'
            elif pid == FlexProjectData.NATIVE_PLATFORM:
                label = 'Native'
            elif pid == FlexProjectData.AIR_PLATFORM:
                label = 'Desktop'
            elif pid == FlexProjectData.FLASH_PLATFORM:
                label = 'Flash'

            uploader = BuildPackageUploader(projectData)
            self._log.write('<h3>Uploading "%s"</h3>' % label)
            url = uploader.upload(pid)
            if url is None:
                self._log.write('<h3 style="color:#FF6666">Upload Failed</h3>')
                continue

            self._log.write('<h3>Upload Success</h3><a href="%s">%s</a>' % (url, url))
            self._output['urls'][pid] = url

        self._log.write('<h2>Uploading Process Complete</h2>')
        return 0
