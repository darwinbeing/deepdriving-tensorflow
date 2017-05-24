import ctypes
import os

if os.name == 'nt':
    _LIBRARY_FILE = "dd-drivecontroller.dll"
else:
    _LIBRARY_FILE = "dd-drivecontroller.so"

try:
    _CURRENT_SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
    _DEFAULT_LIBRARY_PATH = os.path.join(_CURRENT_SCRIPT_PATH, "..", "..", "..", "bin")
    os.environ["PATH"] += os.pathsep + _DEFAULT_LIBRARY_PATH
except:
    pass

_LIBRARY = ctypes.cdll.LoadLibrary(_LIBRARY_FILE)

class CDriveController():
    def __init__(self):
        Constructor = _LIBRARY.CDriveController_create
        Constructor.restype = ctypes.c_void_p

        self._Object = ctypes.c_void_p(Constructor())


    def __del__(self):
        _LIBRARY.CDriveController_destroy(self._Object)
