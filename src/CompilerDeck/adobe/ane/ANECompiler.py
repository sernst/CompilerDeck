# ANECompiler.py
# (C)2012-2013
# Scott Ernst

import os
import shutil
import zipfile

from CompilerDeck.adobe.SystemCompiler import SystemCompiler

#___________________________________________________________________________________________________ ANECompiler
class ANECompiler(SystemCompiler):

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _compileImpl
    def _compileImpl(self):
        os.chdir(self.getProjectPath())
        sets = None

        cmd = [
            '"%sbin%sadt.bat"' % (self.getAirPath(), os.sep),
            '-package',
            '-storetype PKCS12',
            '-keystore "%s"' % sets.certPath,
            '-storepass ' + sets.certPassword,
            '-tsa none',
            '-target ane', '%s.ane' % self._settings.targetName,
            '"%s"' % self.getTargetPath('extension.xml'),
            '-swc "%s"' % self.getTargetPath('swc', 'default', self._settings.targetName + '.swc'),
            '-platform Android-ARM',
            '-C "%s"' % (self.getTargetPath('bin') + 'android'),
            '.',
            '-platform default',
            '-C "%s"' % (self.getTargetPath('bin') + 'default'),
            'library.swf'
        ]

        anePath = self.getTargetPath(self._settings.targetName + '.ane')
        if self.executeCommand(cmd, messageHeader='PACKAGING ANE') or not os.path.exists(anePath):
            self._log.write('FAILED: ANE PACKAGING')
            return False
        self._log.write('SUCCESS: ANE PACKAGED')

        self.printCommand(header='DEPLOYING ANE DEBUG FILES')
        debugPath = self.getProjectPath('air', 'ane', 'debug')
        if not os.path.exists(debugPath):
            os.makedirs(debugPath)
        debugPath += self._settings.targetName + '.ane' + os.sep
        if os.path.exists(debugPath):
            success = False
            try:
                shutil.rmtree(debugPath)
                success = True
            except Exception, err:
                pass

            if not success:
                try:
                    os.removedirs(debugPath)
                    success = True
                except Exception, err:
                    pass
            if not success:
                try:
                    os.remove(debugPath)
                    success = True
                except Exception, err:
                    pass
            if not success:
                self._log.write(('ERROR: Unable to remove existing debug files. '
                    + 'Please check to make sure other resources are not preventing the '
                    + '%s folder from being regenerated.') % debugPath)
                return False

        try:
            z = zipfile.ZipFile(anePath)
            z.extractall(path=debugPath)
            self._log.write('SUCCESS: ANE DEBUG FILES DEPLOYED')
        except Exception, err:
            self._log.write('FAILED: ANE DEBUG DEPLOYMENT')
            self._log.writeError('Zip error', err)

        return True
