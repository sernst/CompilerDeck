# NativeExtensionCompiler.py
# (C)2014
# Scott Ernst

import os

from pyaid.file.FileUtils import FileUtils
from pyaid.system.SystemUtils import SystemUtils

from CompilerDeck.adobe.SystemCompiler import SystemCompiler

#___________________________________________________________________________________________________ NativeExtensionCompiler
from CompilerDeck.adobe.flex.FlexProjectData import FlexProjectData


class NativeExtensionCompiler(SystemCompiler):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, owner, settings, **kwargs):
        """Creates a new instance of NativeExtensionCompiler."""
        super(NativeExtensionCompiler, self).__init__(owner, settings, **kwargs)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _compileImpl
    def _compileImpl(self):
        sets = self._settings
        os.chdir(sets.projectPath)

        adtPath     = self.getAirPath('bin', 'adt', isFile=True)
        swcRootPath = FileUtils.createPath(sets.projectPath, 'swc', isDir=True)

        buildPath = FileUtils.createPath(sets.projectPath, 'build', isDir=True)
        SystemUtils.remove(buildPath)
        os.makedirs(buildPath)

        sets.setPlatform(FlexProjectData.DEFAULT_PLATFORM)

        swcPath = FileUtils.createPath(
            swcRootPath,
            sets.getSetting('FOLDER'),
            sets.getSetting('FILENAME') + '.swc',
            isFile=True)

        cmd = [adtPath,
            '-package',
            '-target', 'ane', sets.getSetting('FILENAME') + '.ane', 'extension.xml',
            '-swc', swcPath]

        platforms = [
            (FlexProjectData.DEFAULT_PLATFORM, 'default', None),
            (FlexProjectData.ANDROID_PLATFORM, 'Android-ARM', 'jar'),
            (FlexProjectData.IOS_PLATFORM, 'iPhone-ARM', 'a'),
            (FlexProjectData.WINDOWS_PLATFORM, 'Windows-x86', None),
            (FlexProjectData.MAC_PLATFORM, 'MacOS-x86', None)]

        platformsData = []
        for platformDef in platforms:
            if not sets.setPlatform(platformDef[0]):
                continue

            platformFolder = sets.getSetting('FOLDER')

            platformBuildPath = FileUtils.createPath(buildPath, platformFolder, isDir=True, noTail=True)
            os.makedirs(platformBuildPath)

            # LIBRARY.SWF
            SystemUtils.copy(
                FileUtils.createPath(
                    sets.projectPath, 'swc', platformFolder, 'extracted', 'library.swf', isFile=True),
                FileUtils.createPath(platformBuildPath, 'library.swf', isFile=True) )

            # NATIVE LIBRARY
            nativeLibrary = sets.getSetting('NATIVE_LIBRARY')
            if nativeLibrary:
                SystemUtils.copy(
                    FileUtils.createPath(sets.projectPath, platformFolder, nativeLibrary, isFile=True),
                    FileUtils.createPath(buildPath, platformFolder, nativeLibrary, isFile=True))

            # Android RES folder
            if platformDef[0] == FlexProjectData.ANDROID_PLATFORM:
                FileUtils.mergeCopy(
                    FileUtils.createPath(sets.projectPath, platformFolder, 'res', isDir=True),
                    FileUtils.createPath(buildPath, platformFolder, 'res', isDir=True))

            cmd.extend(['-platform', platformDef[1]])

            optionsPath = FileUtils.createPath(
                sets.projectPath, platformFolder, 'platform.xml', isFile=True, noTail=True)
            if os.path.exists(optionsPath):
                cmd.extend(['-platformoptions', '"%s"' % optionsPath])

            cmd.extend(['-C', platformBuildPath, '.'])

            data = dict(
                nativeLibrary=nativeLibrary,
                definition=platformDef,
                folder=platformFolder,
                initializer=sets.getSetting('INITIALIZER'),
                finalizer=sets.getSetting('FINALIZER'))
            platformsData.append(data)

        self._createExtensionDescriptor(platformsData)
        result = self.executeCommand(cmd, 'PACKAGING ANE')

        # Cleanup deployed library.swf files
        SystemUtils.remove(buildPath)

        if result:
            self._log.write('PACKAGING FAILED')
            return False

        self._log.write('PACKAGED SUCCEEDED')
        return True

#___________________________________________________________________________________________________ _createExtensionDescriptor
    def _createExtensionDescriptor(self, platformsData):
        """ Creates """

        sets = self._settings

        version = '.'.join([
            sets.versionInfo['major'],
            sets.versionInfo['minor'],
            sets.versionInfo['micro'] ])

        items = [
            u'<extension xmlns="http://ns.adobe.com/air/extension/%s">' % sets.airVersion,
            u'    <id>%s</id>' % sets.getSetting('ID'),
            u'    <versionNumber>%s</versionNumber>' % version,
            u'    <platforms>']

        for pd in platformsData:
            entry = [
                u'<platform name="%s">' % pd['definition'][1],
                u'    <applicationDeployment>']

            nativeLibrary = pd.get('nativeLibrary', None)
            if not nativeLibrary:
                extension = pd['definition'][2]
                if extension is not None:
                    nativeLibrary = pd['folder'] + '.' + extension

            if nativeLibrary is not None:
                entry.append(u'        <nativeLibrary>%s</nativeLibrary>' % nativeLibrary)

            initializer = pd['initializer']
            if initializer is not None:
                entry.append(u'        <initializer>%s</initializer>' % initializer)

            finalizer = pd['finalizer']
            if finalizer is not None:
                entry.append(u'        <finalizer>%s</finalizer>' % finalizer)

            entry.extend([
                u'    </applicationDeployment>',
                u'</platform>'])

            items.append(u'        ' + u'\n        '.join(entry))

        items.extend([u'    </platforms>', u'</extension>' ])

        with open(FileUtils.createPath(sets.projectPath, 'extension.xml', isFile=True), 'w') as f:
            f.write('\n'.join(items))

