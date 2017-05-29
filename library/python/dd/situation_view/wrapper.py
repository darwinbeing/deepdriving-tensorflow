import ctypes
import os
import numpy as np

from .. import Indicators_t

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
_BACKGROUND_COLOR = (0.161, 0.392, 0.008)

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


class CSituationView():
    def __init__(self):
        Background=_BACKGROUND_COLOR
        self._Width = 320
        self._Height = 660
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


