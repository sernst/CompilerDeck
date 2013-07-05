# AndroidCompiler.py
# (C)2012-2013
# Scott Ernst

import os
import shutil
import zipfile

from pyaid.file.FileUtils import FileUtils

from pyglass.app.PyGlassEnvironment import PyGlassEnvironment

from CompilerDeck.adobe.SystemCompiler import SystemCompiler

#___________________________________________________________________________________________________ AndroidCompiler
class AndroidCompiler(SystemCompiler):

#===================================================================================================
#                                                                                       C L A S S

    FLASH_LIBS = ['FlashRuntimeExtensions.jar', 'FlashRuntimeExtensions.so']

    IGNORE_LIBS = ['cordova-2.2.0.jar', 'android-support-v4.jar']

    _V4_SUPPORT_LIB = ['extras', 'android', 'support', 'v4', 'src']

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _compileImpl
    def _compileImpl(self):

        #-------------------------------------------------------------------------------------------
        # CHECK IF ANDROID PROJECT FILES EXIST
        createLibrary = False
        if not os.path.exists(self.getTargetPath('android')):
            os.makedirs(self.getTargetPath('android'))
            createLibrary = True
        if not createLibrary:
            for item in ['build.xml', 'AndroidManifest.xml']:
                if not os.path.exists(self.getTargetPath('android', item)):
                    createLibrary = True
                    break

        #-------------------------------------------------------------------------------------------
        # CREATE/UPDATE ANDROID PROJECT
        cmd = ['"%s%s"' % (
            self._owner.mainWindow.getAndroidSDKPath('tools', 'android', isFile=True),
            '.bat' if PyGlassEnvironment.isWindows() else '')
        ]

        if createLibrary:
            messageHeader = 'CREATING ANDROID PROJECT'
            cmd += [
                'create', 'project',
                '--activity', self._settings.targetName,
                '--package', self._settings.ident
            ]
        else:
            messageHeader = 'UPDATING ANDROID PROJECT'
            cmd += ['update', 'project']

        cmd += [
            '--target', '"android-%s"' % str(self._settings.androidTargetVersion),
            '--name', self._settings.targetName,
            '--path', self.getTargetPath() + 'android'
        ]

        if self.executeCommand(cmd, messageHeader):
            self._log.write('FAILED: ANDROID PROJECT MODIFICATIONS')
            return False

        self._log.write('SUCCESS: UPDATE COMPLETE')
        self._log.write('JDK PATH: ' + self._owner.mainWindow.getJavaJDKPath())

        #-------------------------------------------------------------------------------------------
        # CLEAN PROJECT FOR FRESH COMPILATION
        batchCmd = [
            'set JAVA_HOME=%s' % self._owner.mainWindow.getJavaJDKPath(),
            'cd "%s"'  % (self.getTargetPath() + 'android'),
            'set errorlevel=',
            '%s %s' % (self._owner.mainWindow.getJavaAntPath('bin', 'ant.bat'), 'clean')
        ]

        if self.executeBatchCommand(batchCmd, messageHeader='CLEANING ANDROID PROJECT'):
            self._log.write('FAILED: PROJECT CLEANUP')
            return False
        self._log.write('SUCCESS: PROJECT CLEANED')

        #-------------------------------------------------------------------------------------------
        # COPY SUPPORT LIBRARIES
        if 'V4_SUPPORT' in self._settings.androidLibIncludes:
            self._log.write('Including Android V4 Support library...')
            self._copyV4SupportLib()

        #-------------------------------------------------------------------------------------------
        # COMPILE APK
        libsPath = self.getTargetPath('android', 'libs')
        if not os.path.exists(libsPath):
            os.makedirs(libsPath)

        for item in AndroidCompiler.FLASH_LIBS:
            shutil.copy2(
                self.getAirPath('lib', 'android', item),
                self.getTargetPath('android', 'libs', item)
            )

        batchCmd = [
            'set JAVA_HOME=%s' % self._owner.mainWindow.getJavaJDKPath(),
            'cd "%s"'  % (self.getTargetPath() + 'android'),
            'set errorlevel=',
            '%s %s' % (
                self._owner.mainWindow.getJavaAntPath('bin', 'ant.bat'),
                'debug' if self._settings.debug else 'release'
            )
        ]

        if self.executeBatchCommand(batchCmd, messageHeader='COMPILING ANDROID APK'):
            self._log.write('FAILED: APK COMPILATION')
            return False
        self._log.write('SUCCESS: APK COMPILED')

        #-------------------------------------------------------------------------------------------
        # INCLUDE EXTERNAL JAR LIBRARIES
        libSources = []
        libsPath   = self.getTargetPath('android', 'libs')
        ignores    = AndroidCompiler.FLASH_LIBS + AndroidCompiler.IGNORE_LIBS
        for item in os.listdir(libsPath):
            if item in ignores or not item.endswith('.jar'):
                continue
            libSources.append(item)

        if libSources:
            libSrcPath = self.getTargetPath('android', 'lib-src')
            if os.path.exists(libSrcPath):
                shutil.rmtree(libSrcPath)
            os.makedirs(libSrcPath)

            for item in libSources:
                src  = libsPath + item
                dest = self.getTargetPath('android', 'lib-temp')

                if os.path.exists(dest):
                    shutil.rmtree(dest)
                os.makedirs(dest)

                z = zipfile.ZipFile(src)
                z.extractall(path=dest)

                metaInfPath = self.getTargetPath('android', 'lib-temp', 'META-INF')
                if os.path.exists(metaInfPath):
                    shutil.rmtree(metaInfPath)

                FileUtils.mergeCopy(dest, libSrcPath)
                shutil.rmtree(dest)

            for item in os.listdir(libSrcPath):
                shutil.copytree(
                    libSrcPath + item,
                    self.getTargetPath('android', 'bin', 'classes') + item
                )

            if os.path.exists(libSrcPath):
                shutil.rmtree(libSrcPath)

        #-------------------------------------------------------------------------------------------
        # CREATE JAR FILE
        batchCmd = [
            'set JAVA_HOME=%s' % self._owner.mainWindow.getJavaJDKPath(),
            'cd "%s"' % self.getTargetPath('android', 'bin'),
            'set errorlevel=',
            '"%s" cvf %s -C %s .' % (
                self._owner.mainWindow.getJavaJDKPath('bin', 'jar.exe'),
                self.getTargetPath('bin', 'android', self._settings.targetName + '.jar'),
                self.getTargetPath('android', 'bin') + 'classes'
            )
        ]

        if self.executeBatchCommand(batchCmd, messageHeader='COMPILING ANDROID JAR'):
            self._log.write('FAILED: JAR COMPILATION')
            return False
        self._log.write('SUCCESS: JAR COMPILED')

        #-------------------------------------------------------------------------------------------
        # COPY RESOURCES TO BIN
        binResourcePath = self.getTargetPath('bin', 'android', 'res')
        if os.path.exists(binResourcePath):
            shutil.rmtree(binResourcePath)
        shutil.copytree(self.getTargetPath('android', 'res'), binResourcePath)
        self._log.write('SUCCESS: RESOURCES DEPLOYED')

        return True

#___________________________________________________________________________________________________ _checkOutput
    def _checkOutput(self, code, raw, error):
        if not code:
            return

#___________________________________________________________________________________________________ _copyV4SupportLib
    def _copyV4SupportLib(self):
        v4Path = self._owner.mainWindow.getAndroidSDKPath(*AndroidCompiler._V4_SUPPORT_LIB, isDir=True)
        for item in os.listdir(v4Path):
            itemPath = FileUtils.createPath(v4Path, item, isDir=True)
            self._copyMerges.append(
                FileUtils.mergeCopy(itemPath, self.getTargetPath('android', 'src'), False)
            )

