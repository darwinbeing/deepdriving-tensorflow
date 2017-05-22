import ctypes
import os
import numpy as np

if os.name == 'nt':
    _LIBRARY_FILE = "dd-situation-view.dll"
else:
    _LIBRARY_FILE = "dd-situation-view.so"

_CURRENT_SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
_LIBRARY_PATH = os.path.join(_CURRENT_SCRIPT_PATH, "..", "..", "bin")
_LIBRARY_NAME = os.path.join(_LIBRARY_PATH, _LIBRARY_FILE)
_LIBRARY = ctypes.cdll.LoadLibrary(_LIBRARY_NAME)

class CSituationView():
    def __init__(self):
        Constructor = _LIBRARY.CSituationView_create
        Constructor.restype = ctypes.c_void_p
        self._Object = ctypes.c_void_p(Constructor())

    def __del__(self):
        _LIBRARY.CSituationView_destroy(self._Object)


    def getImage(self):
        getImage = _LIBRARY.CSituationView_getImage
        getImage.restype = ctypes.POINTER(ctypes.c_uint8)
        Buffer = getImage(self._Object)
        RawImage = np.fromiter(Buffer, dtype=np.uint8, count=320*500*3)
        Image = np.resize(RawImage, (500,320, 3))
        return Image