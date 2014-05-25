# S3DeployerThread.py
# (C)2013-2014
# Scott Ernst

import os
import smtplib
from email.mime.text import MIMEText

from pyaid.dict.DictUtils import DictUtils
from pyaid.file.FileUtils import FileUtils
from pyglass.threading.RemoteExecutionThread import RemoteExecutionThread

from CompilerDeck.adobe.flex.FlexProjectData import FlexProjectData
from CompilerDeck.deploy.BuildPackageUploader import BuildPackageUploader
from CompilerDeck.deploy.ReleaseNotesGenerator import ReleaseNotesGenerator


#___________________________________________________________________________________________________ S3DeployerThread
class S3DeployerThread(RemoteExecutionThread):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, snapshot, sendEmails, releaseNotes, message, **kwargs):
        """Creates a new instance of S3Deployer."""
        super(S3DeployerThread, self).__init__(parent, **kwargs)
        self._doSendEmails  = sendEmails
        self._releaseNotes  = releaseNotes
        self._snapshot      = snapshot
        self._flexData      = FlexProjectData(**snapshot)
        self._message       = message if message else u''

        if self._flexData.debug:
            self._buildType = u'Beta (Private Testing)'
        elif self._flexData.iosAdHoc:
            self._buildType = u'Release Candidate (Public Pre-Release)'
        else:
            self._buildType = u'Official Release (Public Distribution)'

        if self._releaseNotes:
            self._releaseNotes['buildType'] = self._buildType

        self._output = dict()
        self._bucket = self._flexData.createBucket()

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _runImpl
    def _runImpl(self):
        """Doc..."""
        data = self._flexData

        self._log.write(
            '<div style="font-size:24px">Beginning distribution file upload(s)</div><hr>')

        for platformID, platformIsActive in data.platformSelection.iteritems():
            if not platformIsActive or not data.hasPlatform(platformID):
                continue

            data.setPlatform(platformID)
            if data.isPlatformUploaded:
                url = data.platformUploads[platformID]
            else:
                uploader = BuildPackageUploader(data, self._bucket)
                self._log.write(
                    'Uploading %s distribution file to: %s' % (platformID, uploader.uploadFolder))
                url = uploader.upload(platformID)
                if url is None:
                    continue

                data.platformUploads[platformID] = url

            self._log.write(
                '<div style="font-size:18px">Deployed URL:</div><br />' +
                '<a style="font-size:8px" href="%s">%s</a>' % ((url, url)))

        if self._releaseNotes:
            self._log.write('Generating release notes...')
            notes = self._createReleaseNotes()
        else:
            notes = u''

        if self._doSendEmails:
            self._log.write('Sending notification emails...')
            self._sendEmailNotifications(data.platformUploads, notes)

        self._log.write('<br /><div style="font-size:24px">Deployment Complete!</div>')
        self._output['urls'] = DictUtils.clone(data.platformUploads)
        return 0

#___________________________________________________________________________________________________ _createReleaseNotes
    def _createReleaseNotes(self):
        notes = ReleaseNotesGenerator(
            owner=self.parent(),
            label=self._flexData.getSetting('LABEL', u'Application'),
            versionInfo=self._flexData.versionInfo,
            **self._releaseNotes)

        path = FileUtils.createPath(
            self._flexData.projectPath, 'compiler', 'releaseNotes', isDir=True)
        if not os.path.exists(path):
            os.makedirs(path)

        filename = self._flexData.contentTargetFilename + \
                self._flexData.versionInfoNumber.replace(u'.', u'-') + u'.txt'

        path = FileUtils.createPath(path, filename, isFile=True)
        FileUtils.putContents(notes.generate(), path)

        uploader = BuildPackageUploader(self._flexData, self._bucket)
        url = uploader.uploadFile(path, filename)
        self._log.write('Uploaded release notes to: <a href="%s">%s</a>' % (url, url))

        return notes.text

#___________________________________________________________________________________________________ _sendEmailNotifications
    def _sendEmailNotifications(self, deployUrls, releaseNotes):
        version    = self._flexData.versionInfoNumber
        uid        = self._flexData.versionInfoLabel
        label      = self._flexData.getSetting('LABEL', u'Application')

        body = [
            u'A new build of %s is available: %s\n' % (label, self._message),
            u'  * Type: %s\n\n' % self._buildType,
            u'  * Version: ' + version,
            u'  * Build: ' + uid,
            u'=== DOWNLOADS ===\n',
            u'Please update your application to the latest version by downloading and installing ' +
            u'it from the URL listed below for your choice of platform(s):\n' ]

        for name, url in deployUrls.iteritems():
            if name in FlexProjectData.AIR_PLATFORM:
                key = u'Desktop (Mac/PC)'
            elif name == FlexProjectData.IOS_PLATFORM:
                key = u'iOS (iPad 3+)'
            elif name == FlexProjectData.ANDROID_PLATFORM:
                key = u'Android (2.3+)'
            elif name == FlexProjectData.WINDOWS_PLATFORM:
                key = u'Windows'
            elif name == FlexProjectData.MAC_PLATFORM:
                key = u'Mac'
            else:
                key = name

            body.append(u'--- ' + key + u' Download ---\n' + url + u'\n')

        if releaseNotes:
            body.append(u'\n=== RELEASE NOTES ===\n\n' + releaseNotes)

        body = u'\n'.join(body)

        for email in self._flexData.getSetting(['NOTIFICATION', 'EMAIL', 'RECIPIENTS']):
            self._log.write(
                'Sending email notification to: <span style="font-weight:bold">%s</span>' % email)
            result = self._sendEmail(
                'New Build Available: ' + version,
                body, email)
            if not result:
                return

#___________________________________________________________________________________________________ _sendEmail
    def _sendEmail(self, subject, message, recipient):
        data     = self._flexData
        settings = data.getSetting(['NOTIFICATION', 'EMAIL'])
        if not settings:
            return False

        msg            = MIMEText(message)
        msg['Subject'] = subject
        msg['From']    = settings['SENDER']
        msg['To']      = recipient

        try:
            s = smtplib.SMTP()
            s.set_debuglevel(True)
            s.connect(settings['HOST'], settings['PORT'])
            s.login(settings['LOGIN'], settings['PASSWORD'])
            s.sendmail(settings['SENDER'], [recipient], msg.as_string())
            s.quit()
        except Exception, err:
            self._log.writeError('ERROR: Failed to send email', err)
            return False
        return True
