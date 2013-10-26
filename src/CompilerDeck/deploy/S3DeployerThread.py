# S3DeployerThread.py
# (C)2013
# Scott Ernst

import os
import datetime
import smtplib
from email.mime.text import MIMEText

from pyaid.aws.s3.S3Bucket import S3Bucket
from pyaid.file.FileUtils import FileUtils
from pyaid.time.TimeUtils import TimeUtils

from pyglass.threading.RemoteExecutionThread import RemoteExecutionThread

from CompilerDeck.adobe.flex.FlexProjectData import FlexProjectData
from CompilerDeck.deploy.ReleaseNotesGenerator import ReleaseNotesGenerator

#___________________________________________________________________________________________________ S3DeployerThread
class S3DeployerThread(RemoteExecutionThread):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, snapshot, sendEmails, releaseNotes, **kwargs):
        """Creates a new instance of S3Deployer."""
        super(S3DeployerThread, self).__init__(parent, **kwargs)
        self._doSendEmails  = sendEmails
        self._releaseNotes  = releaseNotes
        self._flexData      = FlexProjectData(**snapshot)

        self._keyPrefix = [
            'downloads',
            'debug' if self._flexData.debug else 'release',
            TimeUtils.getNowDatetime().strftime('%b-%d-%y')]

        self._bucket = S3Bucket(
            self._flexData.getSetting(['S3', 'BUCKET']),
            self._flexData.getSetting(['S3', 'AWS_ID']),
            self._flexData.getSetting(['S3', 'AWS_SECRET']))

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _runImpl
    def _runImpl(self):
        """Doc..."""
        data = self._flexData
        urls = dict()

        self._log.write(
            '<div style="font-size:24px">Beginning distribution file upload(s)</div><hr>')

        for platformID, platformIsActive in data.platformSelection.iteritems():
            if not platformIsActive or not data.hasPlatform(platformID):
                continue

            data.setPlatform(platformID)
            if not os.path.exists(data.targetFilePath):
                continue

            name = data.targetFilename + '-' + \
                   data.versionInfo['major'] + '-' + \
                   data.versionInfo['minor'] + '-' + \
                   data.versionInfo['revision'] + '.' + \
                   data.airExtension

            key = '/'.join(self._keyPrefix + [name])
            self._log.write('Uploading %s distribution file to: %s' % (platformID, key))
            self._bucket.putFile(
                key=key,
                filename=data.targetFilePath,
                policy=S3Bucket.PRIVATE if data.debug else S3Bucket.PUBLIC_READ)

            expires  = TimeUtils.getNowDatetime()
            expires += datetime.timedelta(days=30)
            if data.debug:
                url = self._bucket.generateExpiresUrl(key, expires)
            else:
                url = 'http://' + self._bucket.bucketName + '/' + key
            urls[platformID] = url
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
            self._sendEmailNotifications(urls, notes)

        self._log.write('<div style="font-size:24px">Deployment Complete!</div>')
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

        filename = self._flexData.targetFilename + \
                self._flexData.versionInfoNumber.replace(u'.', u'-') + u'.txt'
        path += filename

        FileUtils.putContents(notes.generate(), path)

        key = '/'.join(self._keyPrefix + [filename])
        self._log.write('Uploading release notes to: %s' % key)
        self._bucket.putFile(
            key=key,
            filename=path,
            policy=S3Bucket.PRIVATE if self._flexData.debug else S3Bucket.PUBLIC_READ)

        return notes.text

#___________________________________________________________________________________________________ _sendEmailNotifications
    def _sendEmailNotifications(self, deployUrls, releaseNotes):
        version    = self._flexData.versionInfoNumber
        uid        = self._flexData.versionInfoLabel
        label      = self._flexData.getSetting('LABEL', u'Application')

        body = [
            u'A new build of %s is available.\n' % label,
            u'  * Version: ' + version,
            u'  * Build: ' + uid + u'\n\n',
            u'=== DOWNLOADS ===\n',
            u'Please update your application to the latest version by downloading and installing ' +
            u'it from the URL listed below for your choice of platform(s).\n' ]

        for key, url in deployUrls.iteritems():
            if key in [FlexProjectData.NATIVE_PLATFORM, FlexProjectData.AIR_PLATFORM]:
                key = u'Desktop (Mac/PC)'
            elif key == FlexProjectData.IOS_PLATFORM:
                key = u'iOS (iPad 3/4)'
            elif key == FlexProjectData.AIR_PLATFORM:
                key = u'Android'

            body.append(u'--- ' + key + u' Download ---\n' + url + u'\n')

        if releaseNotes:
            body.append(u'\n=== RELEASE NOTES ===\n\n' + releaseNotes)

        body = u'\n'.join(body)

        for email in self._flexData.getSetting(['NOTIFICATION', 'EMAIL', 'RECIPIENTS']):
            self._log.write(
                'Sending email notification to: <span style="font-weight:bold">%s</span>' % email)
            result = self._sendEmail(
                'New Build Available: ' + version,
                body,
                email)
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
