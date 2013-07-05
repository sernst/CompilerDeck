# AirUtils.py
# (C)2012-2013
# Scott Ernst

import os

from pyaid.file.FileUtils import FileUtils

from CompilerDeck.adobe.flex.FlexProjectData import FlexProjectData

#___________________________________________________________________________________________________ AirUtils
class AirUtils(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ deployPlatformFiles
    @classmethod
    def deployPlatformFiles(cls, flexProjectData):
        return {'dirs':[], 'merges':[]}
        sets = flexProjectData

        if sets.currentPlatformID == FlexProjectData.ANDROID_PLATFORM:
            platformType = 'android'
        elif sets.currentPlatformID == FlexProjectData.IOS_PLATFORM:
            platformType = 'ios'
        else:
            platformType = 'desktop'
        platformPath = FileUtils.createPath(sets.projectPath, 'platforms', platformType)
        if not os.path.exists(platformPath):
            return out

        for item in os.listdir(platformPath):
            itemPath = FileUtils.createPath(platformPath, item)
            if not os.path.isdir(itemPath):
                continue
            copyResults = FileUtils.mergeCopy(
                itemPath,
                FileUtils.createPath(sets.targetPath, item),
                overwriteExisting=False
            )
            out['merges'].append(copyResults)
            out['dirs'].append(item)

        return out
