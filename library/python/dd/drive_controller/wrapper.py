import ctypes
import os

from .. import Indicators_t, Control_t

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
    def __init__(self, Lanes):
        Constructor = _LIBRARY.CDriveController_create
        Constructor.restype = ctypes.c_void_p
        Constructor.argtypes = [ctypes.c_uint32]

        self._Object = ctypes.c_void_p(Constructor(Lanes))


    def __del__(self):
        _LIBRARY.CDriveController_destroy(self._Object)


    def control(self, Indicators, Control):
        control = _LIBRARY.CDriveController_control
        control.argtypes = [ctypes.c_void_p, ctypes.POINTER(Indicators_t), ctypes.POINTER(Control_t)]

        control(self._Object, Indicators, Control)