# BuildPackageUploader.py
# (C)2014
# Scott Ernst

import os
import datetime

from pyaid.aws.s3.S3Bucket import S3Bucket
from pyaid.time.TimeUtils import TimeUtils

#___________________________________________________________________________________________________ BuildPackageUploader
class BuildPackageUploader(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, projectData, bucket =None, uploadFolder =None, **kwargs):
        """Creates a new instance of BuildPackageUploader."""
        self._flexData = projectData

        if uploadFolder is None:
            self._uploadFolder = '/'.join([
                'downloads',
                'debug' if self._flexData.debug else 'release',
                TimeUtils.getNowDatetime().strftime('%b-%d-%y')])
        else:
            self._uploadFolder = uploadFolder

        if not self._uploadFolder.endswith('/'):
            self._uploadFolder += '/'

        self._bucket = bucket if bucket else self._flexData.createBucket()

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: uploadFolder
    @property
    def uploadFolder(self):
        return self._uploadFolder

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ uploadFile
    def uploadFile(self, sourcePath, targetFilename):
        return self._putFile(sourcePath, self._uploadFolder + targetFilename)

#___________________________________________________________________________________________________ upload
    def upload(self, platformID):
        """Doc..."""
        data = self._flexData
        data.setPlatform(platformID)
        if not os.path.exists(data.targetFilePath):
            return None

        name = data.contentTargetFilename + '-' + \
               data.versionInfo['major'] + '-' + \
               data.versionInfo['minor'] + '-' + \
               data.versionInfo['micro'] + '-' + \
               data.versionInfo['revision'] + '.' + \
               data.airExtension

        return self._putFile(data.targetFilePath, self._uploadFolder + name)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _putFile
    def _putFile(self, sourcePath, key):
        self._bucket.putFile(
            key=key,
            filename=sourcePath,
            policy=S3Bucket.PRIVATE if self._flexData.debug else S3Bucket.PUBLIC_READ)

        expires  = TimeUtils.getNowDatetime()
        expires += datetime.timedelta(days=30)
        if self._flexData.debug:
            url = self._bucket.generateExpiresUrl(key, expires)
        else:
            url = 'http://' + self._bucket.bucketName + '/' + key

        return url

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __unicode__
    def __unicode__(self):
        return unicode(self.__str__())

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s>' % self.__class__.__name__
