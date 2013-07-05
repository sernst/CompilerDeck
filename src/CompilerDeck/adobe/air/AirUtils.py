# AirUtils.py
# (C)2012-2013
# Scott Ernst

import os
import re

from pyaid.file.FileUtils import FileUtils

#___________________________________________________________________________________________________ AirUtils
class AirUtils(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    DESCRIPTOR_VERSION_PATTERN = re.compile(
        '(?P<prefix><application xmlns="http://ns.adobe.com/air/application/)[0-9\.]+(?P<suffix>">)')

#___________________________________________________________________________________________________ updateDescriptorNamespace
    @classmethod
    def updateDescriptorNamespace(cls, descriptorPath, airVersion):
        data = FileUtils.getContents(descriptorPath)
        data = cls.DESCRIPTOR_VERSION_PATTERN.sub('\g<prefix>' + airVersion + '\g<suffix>', data)
        return FileUtils.putContents(data, descriptorPath)

#___________________________________________________________________________________________________ deployExternalIncludes
    @classmethod
    def deployExternalIncludes(cls, flexProjectData):
        """ Deploys all of the external includes file and folders to the platform-specific project
            bin folder for use in packaging or debugging. Returns a list of FileLists for each
            copy operation that occurred so that the deploy operation can be undone later."""

        out = {'dirs':[], 'files':[], 'merges':[]}
        sets = flexProjectData

        # Copy everything in the includes directory
        includesPath = sets.externalIncludesPath
        for item in os.listdir(includesPath):
            source = FileUtils.createPath(includesPath, item)
            out['merges'].append(FileUtils.mergeCopy(
                source, FileUtils.createPath(sets.projectBinPath, item)))
            if os.path.isdir(source):
                out['dirs'].append(source)
            else:
                out['files'].append(source)

        includesPath = sets.platformExternalIncludesPath
        if not includesPath:
            return out

        for item in os.listdir(includesPath):
            source = FileUtils.createPath(includesPath, item)
            out['merges'].append(FileUtils.mergeCopy(
                source, FileUtils.createPath(sets.projectBinPath, item)))
            if os.path.isdir(source):
                out['dirs'].append(source)
            else:
                out['files'].append(source)
        return out
