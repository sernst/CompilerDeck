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

        out = {'dirs':[], 'files':[], 'merges':[], 'itemNames':[]}
        sets = flexProjectData

        # Copy the icons for the platform deployment from the icons folder for that platform, or,
        # if not platform specific icons folder exists, from the main icons folder instead.
        iconPath = FileUtils.createPath(sets.platformProjectPath, 'icons', isDir=True)
        print 'ICON PATH:', iconPath, os.path.exists(iconPath)
        if not os.path.exists(iconPath):
            iconPath = FileUtils.createPath(sets.projectPath, 'icons', isDir=True)
        if os.path.exists(iconPath):
            out['merges'].append(FileUtils.mergeCopy(
                iconPath, FileUtils.createPath(sets.platformBinPath, 'icons', isDir=True)))
            out['dirs'].append(iconPath)
            out['itemNames'].append('icons')

        # Copy everything in the includes directory
        includesPath = sets.externalIncludesPath
        if os.path.exists(includesPath):
            for item in os.listdir(includesPath):
                source = FileUtils.createPath(includesPath, item)
                out['merges'].append(FileUtils.mergeCopy(
                    source, FileUtils.createPath(sets.platformBinPath, item)))
                if os.path.isdir(source):
                    out['dirs'].append(source)
                else:
                    out['files'].append(source)
                out['itemNames'].append(item)

        includesPath = sets.platformExternalIncludesPath
        if not includesPath or not os.path.exists(includesPath):
            return out

        for item in os.listdir(includesPath):
            source = FileUtils.createPath(includesPath, item)
            out['merges'].append(FileUtils.mergeCopy(
                source, FileUtils.createPath(sets.platformBinPath, item)))
            if os.path.isdir(source):
                out['dirs'].append(source)
            else:
                out['files'].append(source)
            out['itemNames'].append(item)
        return out
