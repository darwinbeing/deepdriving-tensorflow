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
    def __init__(self, Size, Background):
        self._Width = Size[0]
        self._Height = Size[1]
        self._Channels = 3

        Constructor = _LIBRARY.CSituationView_create
        Constructor.restype = ctypes.c_void_p

        Size = Size_t()
        Size.Width = self._Width
        Size.Height = self._Height

        Color = Color_t()
        Color.R = Background[0];
        Color.G = Background[1];
        Color.B = Background[2];

        self._Object = ctypes.c_void_p(Constructor(Size, Color))

    def __del__(self):
        _LIBRARY.CSituationView_destroy(self._Object)


    def getImage(self):
        getImage = _LIBRARY.CSituationView_getImage
        getImage.restype = ctypes.POINTER(ctypes.c_uint8)
        Buffer = getImage(self._Object)
        RawImage = np.fromiter(Buffer, dtype=np.uint8, count=self._Width*self._Height*self._Channels)
        Image = np.resize(RawImage, (self._Height, self._Width, self._Channels))
        return Image