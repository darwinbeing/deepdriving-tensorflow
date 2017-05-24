import ctypes
import os

if os.name == 'nt':
    _LIBRARY_FILE = "dd-situation-view.dll"
else:
    _LIBRARY_FILE = "dd-situation-view.so"

try:
    _CURRENT_SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
    _DEFAULT_LIBRARY_PATH = os.path.join(_CURRENT_SCRIPT_PATH, "..", "..", "bin")
    os.environ["PATH"] += os.pathsep + _DEFAULT_LIBRARY_PATH
except:
    pass

_LIBRARY = ctypes.cdll.LoadLibrary(_LIBRARY_FILE)

ARE_INDICATORS_VALID = False
INVALID_INDICATORS = None
MAX_INDICATORS = None
MIN_INDICATORS = None

class Indicators_t(ctypes.Structure):
    _fields_ = [
        ('Speed',  ctypes.c_double),
        ('Fast',   ctypes.c_double),
        ('Angle',  ctypes.c_double),
        ('LL',     ctypes.c_double),
        ('ML',     ctypes.c_double),
        ('MR',     ctypes.c_double),
        ('RR',     ctypes.c_double),
        ('DistLL', ctypes.c_double),
        ('DistMM', ctypes.c_double),
        ('DistRR', ctypes.c_double),
        ('L',      ctypes.c_double),
        ('M',      ctypes.c_double),
        ('R',      ctypes.c_double),
        ('DistL',  ctypes.c_double),
        ('DistR',  ctypes.c_double),
    ]


    def __init__(self):
        if ARE_INDICATORS_VALID:
            self.Speed  = 35
            self.Fast   = 0
            self.Angle  = 0
            self.LL     = INVALID_INDICATORS.LL
            self.ML     = -2
            self.MR     = 2
            self.RR     = INVALID_INDICATORS.RR
            self.DistLL = INVALID_INDICATORS.DistLL
            self.DistMM = INVALID_INDICATORS.DistMM
            self.DistRR = INVALID_INDICATORS.DistRR
            self.L      = INVALID_INDICATORS.L
            self.M      = -2
            self.R      = 2
            self.DistL  = INVALID_INDICATORS.L
            self.DistR  = INVALID_INDICATORS.R

    def __str__(self):
        String = ""
        String += "Speed={}\n".format(self.Speed)
        String += "Fast={}\n".format(self.Fast)
        String += "Angle={}\n".format(self.Angle)
        String += "LL={}\n".format(self.LL)
        String += "ML={}\n".format(self.ML)
        String += "MR={}\n".format(self.MR)
        String += "RR={}\n".format(self.RR)
        String += "DistLL={}\n".format(self.DistLL)
        String += "DistMM={}\n".format(self.DistMM)
        String += "DistRR={}\n".format(self.DistRR)
        String += "L={}\n".format(self.L)
        String += "M={}\n".format(self.M)
        String += "R={}\n".format(self.R)
        String += "DistL={}\n".format(self.DistL)
        String += "DistR={}\n".format(self.DistR)
        return String


def setupIndicators():
    global INVALID_INDICATORS
    getInvalidIndicators = _LIBRARY.getInvalidIndicators
    getInvalidIndicators.restype = ctypes.POINTER(Indicators_t)
    INVALID_INDICATORS = getInvalidIndicators().contents

    global MAX_INDICATORS
    getMaxIndicators = _LIBRARY.getMaxIndicators
    getMaxIndicators.restype = ctypes.POINTER(Indicators_t)
    MAX_INDICATORS = getMaxIndicators().contents

    global MIN_INDICATORS
    getMinIndicators = _LIBRARY.getMinIndicators
    getMinIndicators.restype = ctypes.POINTER(Indicators_t)
    MIN_INDICATORS = getMinIndicators().contents

    global ARE_INDICATORS_VALID
    ARE_INDICATORS_VALID = True

setupIndicators()
