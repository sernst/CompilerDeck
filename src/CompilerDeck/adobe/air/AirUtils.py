# AirUtils.py
# (C)2012-2014
# Scott Ernst

import os
import re
import zipfile

from pyaid.file.FileUtils import FileUtils
from pyaid.system.SystemUtils import SystemUtils

# AS NEEDED: from CompilerDeck.adobe.flex.FlexProjectData import FlexProjectData

#___________________________________________________________________________________________________ AirUtils
class AirUtils(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    FILENAME_PATTERN = re.compile('(?P<prefix><filename>)[^<]+(?P<suffix></filename>)')

    CONTENT_FILENAME_PATTERN = re.compile('(?P<prefix><content>)[^<]+(?P<suffix></content>)')

    APP_ICON_PATTERN = re.compile(
        '(?P<prefix><icon>).*?(?P<suffix></icon>)', re.MULTILINE | re.DOTALL)

    APP_EXTENSION_PATTERN = re.compile(
        '(?P<prefix><extensions>).*?(?P<suffix></extensions>)', re.MULTILINE | re.DOTALL)

    APP_ID_PATTERN = re.compile('(?P<prefix><id>)[^<]+(?P<suffix></id>)')

    DESCRIPTOR_VERSION_PATTERN = re.compile(
        '(?P<prefix><application xmlns="http://ns.adobe.com/air/application/)[0-9\.]+(?P<suffix>">)')

#___________________________________________________________________________________________________ updateDescriptorNamespace
    @classmethod
    def updateDescriptorNamespace(cls, descriptorPath, airVersion):
        data = FileUtils.getContents(descriptorPath)
        data = cls.DESCRIPTOR_VERSION_PATTERN.sub('\g<prefix>' + airVersion + '\g<suffix>', data)
        return FileUtils.putContents(data, descriptorPath)

#___________________________________________________________________________________________________ updateAppId
    @classmethod
    def updateAppId(cls, descriptorPath, appId):
        data = FileUtils.getContents(descriptorPath)
        data = cls.APP_ID_PATTERN.sub('\g<prefix>' + appId + '\g<suffix>', data)
        return FileUtils.putContents(data, descriptorPath)

#___________________________________________________________________________________________________ updateAppFilename
    @classmethod
    def updateAppFilename(cls, descriptorPath, filename, contentFilename):
        data = FileUtils.getContents(descriptorPath)
        data = cls.FILENAME_PATTERN.sub('\g<prefix>' + filename + '\g<suffix>', data)
        data = cls.CONTENT_FILENAME_PATTERN.sub('\g<prefix>' + contentFilename + '.swf\g<suffix>', data)
        return FileUtils.putContents(data, descriptorPath)

#___________________________________________________________________________________________________ updateAppIconList
    @classmethod
    def updateAppIconList(cls, descriptorPath, iconDefs):
        s = []
        offset = '\n        '
        for icon in iconDefs:
            size = icon['size']
            name = icon['name']
            s.append('<image%sx%s>icons/%s</image%sx%s>' % (size, size, name, size, size))

        data = FileUtils.getContents(descriptorPath)
        data = cls.APP_ICON_PATTERN.sub(
            '\g<prefix>' + offset + offset.join(s) + '\n    \g<suffix>', data)

        return FileUtils.putContents(data, descriptorPath)

#___________________________________________________________________________________________________ _addAIRNativeExtensionArguments
    @classmethod
    def addAIRNativeExtensionArguments(cls, cmd, settings):
        from CompilerDeck.adobe.flex.FlexProjectData import FlexProjectData

        sets = settings
        if not sets.aneIncludes:
            return

        extensionIDs = []
        for ane in sets.aneIncludes:
            anePath = FileUtils.createPath(sets.projectPath, 'NativeExtensions', ane, isDir=True)
            aneSets = FlexProjectData(anePath)
            cmd.extend(
                ['-extdir', '"%s"' % FileUtils.createPath(aneSets.projectPath, isDir=True, noTail=True)])
            extensionIDs.append(aneSets.getSetting('ID'))

        AirUtils.updateAppExtensions(sets.appDescriptorPath, extensionIDs)

#___________________________________________________________________________________________________ _deployDebugNativeExtensions
    @classmethod
    def deployDebugNativeExtensions(cls, cmd, settings):
        from CompilerDeck.adobe.flex.FlexProjectData import FlexProjectData

        sets = settings
        if not sets.aneIncludes:
            return None

        debugPath = FileUtils.createPath(
            sets.projectPath, 'NativeExtensions', '__debug__', isDir=True, noTail=True)

        if os.path.exists(debugPath):
            SystemUtils.remove(debugPath)
        os.makedirs(debugPath)

        extensionIDs = []
        for ane in sets.aneIncludes:
            anePath = FileUtils.createPath(sets.projectPath, 'NativeExtensions', ane, isDir=True)
            aneSets = FlexProjectData(anePath)
            extensionIDs.append(aneSets.getSetting('ID'))
            aneFilename = aneSets.getSetting('FILENAME')

            aneFile = FileUtils.createPath(anePath, aneFilename + '.ane', isFile=True)
            z = zipfile.ZipFile(aneFile)
            z.extractall(FileUtils.createPath(debugPath, aneFilename + '.ane', isDir=True, noTail=True))

        AirUtils.updateAppExtensions(sets.appDescriptorPath, extensionIDs)

        cmd.extend(['-extdir', '"%s"' % debugPath])
        return debugPath

#___________________________________________________________________________________________________ updateAppExtensions
    @classmethod
    def updateAppExtensions(cls, descriptorPath, extensionIDs):
        s = []
        offset = '\n        '
        for eid in extensionIDs:
            s.append('<extensionID>%s</extensionID>' % eid)
        print 'EXTENSIONS:', s
        data = FileUtils.getContents(descriptorPath)
        data = cls.APP_EXTENSION_PATTERN.sub(
            '\g<prefix>' + offset + offset.join(s) + '\n    \g<suffix>', data)

        return FileUtils.putContents(data, descriptorPath)

#___________________________________________________________________________________________________ deployExternalIncludes
    @classmethod
    def deployExternalIncludes(cls, flexProjectData):
        """ Deploys all of the external includes file and folders to the platform-specific project
            bin folder for use in packaging or debugging. Returns a list of FileLists for each
            copy operation that occurred so that the deploy operation can be undone later. """

        dirs      = []
        files     = []
        merges    = []
        itemNames = []

        out = {'dirs':dirs, 'files':files, 'merges':merges, 'itemNames':itemNames, 'icons':[]}
        sets = flexProjectData

        #-------------------------------------------------------------------------------------------
        # ICONS
        #       Cascade through the various locations where icons may reside for a given platform
        #       and copy the preferred location to the bin for compilation.

        iconTargetPath = FileUtils.createPath(sets.platformBinPath, 'icons', isDir=True)

        #--- Platform[Specific] | Build-Type[Specific] ---#
        iconPath = FileUtils.createPath(
            sets.platformProjectPath, 'icons', sets.buildTypeFolderName, isDir=True)

        #--- Platform[Specific] | Build-Type[Generic] ---#
        if not os.path.exists(iconPath):
            iconPath = FileUtils.createPath(sets.platformProjectPath, 'icons', isDir=True)

        #--- Platform[Generic] | Build-Type[Specific] ---#
        if not os.path.exists(iconPath):
            iconPath = FileUtils.createPath(
                sets.projectPath, 'icons', sets.buildTypeFolderName, isDir=True)

        #--- Platform[Generic] | Build-Type[Generic] ---#
        if not os.path.exists(iconPath):
            iconPath = FileUtils.createPath(sets.projectPath, 'icons', isDir=True)

        # If an icon path exists, copy those files to the target path for inclusion
        if os.path.exists(iconPath):
            cls._deployIcons(iconPath, iconTargetPath, out)
        cls.updateAppIconList(sets.appDescriptorPath, out['icons'])

        #-------------------------------------------------------------------------------------------
        # INCLUDES FOLDER
        #       Copy everything in the includes directory with the generic includes first and then
        #       the platform-specific includes merged in (potentially overwriting general files
        #       in the process if there is a naming collision. This allows for platform specific
        #       file overrides when desirable.

        #--- Generic Includes ---#
        includesPath = sets.externalIncludesPath
        if os.path.exists(includesPath):
            for item in os.listdir(includesPath):
                if item.startswith('.'):
                    continue

                source = FileUtils.createPath(includesPath, item)
                merges.append(FileUtils.mergeCopy(
                    source, FileUtils.createPath(sets.platformBinPath, item)))
                if os.path.isdir(source):
                    dirs.append(source)
                else:
                    files.append(source)
                itemNames.append(item)

        #--- Specific Includes ---#
        includesPath = sets.platformExternalIncludesPath
        if not includesPath or not os.path.exists(includesPath):
            return out

        for item in os.listdir(includesPath):
            if item.startswith('.'):
                continue

            source = FileUtils.createPath(includesPath, item)
            merges.append(FileUtils.mergeCopy(
                source, FileUtils.createPath(sets.platformBinPath, item)))
            if os.path.isdir(source):
                dirs.append(source)
            else:
                files.append(source)
            itemNames.append(item)
        return out

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _deployIcons
    @classmethod
    def _deployIcons(cls, sourcePath, targetPath, record):
        merges    = record['merges']
        dirs      = record['dirs']
        itemNames = record['itemNames']
        icons     = record['icons']

        merges.append(FileUtils.mergeCopy(sourcePath, targetPath))
        dirs.append(sourcePath)
        itemNames.append('icons')

        for item in os.listdir(targetPath):
            size = item.split('_')[-1].split('.')[0]
            icons.append({'size':size, 'name':item})
