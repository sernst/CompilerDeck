import sys
from distutils.core import setup

try:
    import py2exe
    isWindows = True
except Exception, err:
    isWindows = False

try:
    import py2app
    isMac = True
except Exception, err:
    isMac = False

if not isWindows and not isMac:
    print 'ERROR: Missing py2exe or py2app package'
    sys.exit(1)

from pyglass.compile.SetupConstructor import SetupConstructor

# Create the setup constructor
con = SetupConstructor(__file__)

# Create setup argument definition
kwargs = con.getSetupKwargs(
    scriptPath='/Users/scott/Python/CompilerDeck/src/CompilerDeck/CompilerDeckApplication.py',
    resources=[],
    includes=["pyside"],
    iconPath='/Users/scott/Python/CompilerDeck/bin/CompilerDeck.icns',
    appDisplayName='CompilerDeck')

# Execute setup process
try:
    print 'Beginning Setup with Settings:'
    for n,v in kwargs.iteritems():
        print '    %s: %s' % (n, str(v))

    setup(**kwargs)
except Exception, err:
    print 'SETUP ERROR:', err
    import traceback
    print traceback.format_exc()

    raise err

