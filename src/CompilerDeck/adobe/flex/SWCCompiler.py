# SWCCompiler.py
# (C)2012-2013
# Scott Ernst

import os
import shutil
import zipfile

from CompilerDeck.adobe.AdobeSystemCompiler import AdobeSystemCompiler

#___________________________________________________________________________________________________ SWCCompiler
class SWCCompiler(AdobeSystemCompiler):

#===================================================================================================
#                                                                                       C L A S S

    TARGETS = ['default', 'android', 'ios']

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _compileImpl
    def _compileImpl(self):
        sourceCommand = [
            self._owner.mainWindow.getFlexSDKPath('bin', 'acompc.bat', isFile=True),
            '-external-library-path+="%s"' % self.getAirLibraryPath('airglobal.swc'),
            '-external-library-path+="%s"' % self.getFlashLibraryPath(
                'player', self._settings.flashVersion, 'playerglobal.swc'
            )
        ]
        sourcePaths = [self.getProjectPath('internal').replace('\\', '\\\\')]

        for sp in sourcePaths:
            sourceCommand.append('--source-path+="%s"' % sp)

        sourceCommand.append('--include-classes')
        for c in self._settings.sharedClasses:
            sourceCommand.append(c)
        sourceCommand.append(self._settings.targetClass)

        for target in SWCCompiler.TARGETS:
            cmd = sourceCommand + [
                self._getBooleanDefinition('ANDROID', target == 'android'),
                self._getBooleanDefinition('IOS',     target == 'ios'),
                self._getBooleanDefinition('DEFAULT', target == 'default')
            ]

            swcPath = self.getTargetPath('swc', target)
            if not os.path.exists(swcPath):
                os.makedirs(swcPath)

            swcPath = self.getTargetPath('swc', target, self._settings.targetName + '.swc')
            if os.path.exists(swcPath):
                os.remove(swcPath)

            swcCmd = cmd + []
            swcCmd.append('--output ' + swcPath)
            if self.executeCommand(swcCmd, 'COMPILING SWC: "' + target + '"'):
                self._log.write('FAILED: SWC COMPILATION')
                return False
            self._log.write('SUCCESS: SWC COMPILATION')

            try:
                z = zipfile.ZipFile(swcPath)
                z.extractall(self.getTargetPath('swc', target))
            except Exception, err:
                self._log.writeError('FAILED: SWC EXTRACTION', err)
                return False

            self._log.write('SUCCESS: SWC EXTRACTION')

            binPath = self.getTargetPath('bin', target)
            if not os.path.exists(binPath):
                os.makedirs(binPath)
            shutil.copy(
                self.getTargetPath('swc', target, 'library.swf'),
                self.getTargetPath('bin', target, 'library.swf')
            )

            self._log.write('SUCCESS: SWF LIBRARY DEPLOYMENT')

        return True
