import ctypes
import os
import numpy as np

if os.name == 'nt':
    _LIBRARY_FILE = "dd-situation-view.dll"
else:
    _LIBRARY_FILE = "dd-situation-view.so"

try:
    _CURRENT_SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
    _DEFAULT_LIBRARY_PATH = os.path.join(_CURRENT_SCRIPT_PATH, "..", "..", "..", "bin")
    os.environ["PATH"] += os.pathsep + _DEFAULT_LIBRARY_PATH
except:
    pass

_LIBRARY = ctypes.cdll.LoadLibrary(_LIBRARY_FILE)
ARE_INDICATORS_VALID = False
INVALID_INDICATORS = None
MAX_INDICATORS = None
MIN_INDICATORS = None


class Size_t(ctypes.Structure):
    _fields_ = [
        ('Width', ctypes.c_double),
        ('Height', ctypes.c_double),
    ]


class Color_t(ctypes.Structure):
    _fields_ = [
        ('R', ctypes.c_double),
        ('G', ctypes.c_double),
        ('B', ctypes.c_double),
    ]


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


class CSituationView():
    def __init__(self, Size, Background):
        self._Width = Size[0]
        self._Height = Size[1]
        self._Channels = 3
        self._Real = Indicators_t()
        self._Estimated = Indicators_t()

        Constructor = _LIBRARY.CSituationView_create
        Constructor.restype = ctypes.c_void_p
        Constructor.argtypes = [Size_t, Color_t, ctypes.POINTER(ctypes.c_char)]

        Size = Size_t()
        Size.Width = self._Width
        Size.Height = self._Height

        Color = Color_t()
        Color.R = Background[0];
        Color.G = Background[1];
        Color.B = Background[2];

        ImagePath = _CURRENT_SCRIPT_PATH

        self._Object = ctypes.c_void_p(Constructor(Size, Color, ImagePath.encode('utf-8')))
        self.update()


    def __del__(self):
        _LIBRARY.CSituationView_destroy(self._Object)


    def getImage(self):
        getImage = _LIBRARY.CSituationView_getImage
        getImage.restype = ctypes.POINTER(ctypes.c_uint8)
        Buffer = getImage(self._Object)
        RawImage = np.fromiter(Buffer, dtype=np.uint8, count=self._Width*self._Height*self._Channels)
        Image = np.resize(RawImage, (self._Height, self._Width, self._Channels))
        return Image


    def update(self, IsRealValid = True, IsEstimatedValid = True):
        update = _LIBRARY.CSituationView_update
        update.argtypes = [ctypes.c_void_p, ctypes.POINTER(Indicators_t), ctypes.POINTER(Indicators_t)]

        Real = None
        if IsRealValid:
            Real = self._Real

        Estimated = None
        if IsEstimatedValid:
            Estimated = self._Estimated

        update(self._Object, Real, Estimated)


    @property
    def Real(self):
        return self._Real

    @property
    def Estimated(self):
        return self._Estimated


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
