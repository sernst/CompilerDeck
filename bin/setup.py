from distutils.core import setup
import py2exe

from pyglass.compile.SetupConstructor import SetupConstructor

# Create the setup constructor
con = SetupConstructor(__file__)

# Create setup argument definition
kwargs = con.getSetupKwargs(
    scriptPath='f:\\python\\compilerdeck\\src\\compilerdeck\\compilerdeckapplication.py',
    resources=[],
    includes=["pyside"],
    iconPath='f:\\python\\compilerdeck\\bin\\CompilerDeck.ico'
)

# Execute setup process
setup(**kwargs)

