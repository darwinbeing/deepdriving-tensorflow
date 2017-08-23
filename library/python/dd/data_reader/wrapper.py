import ctypes
import os
import numpy as np

from ..labels import Labels_t

if os.name == 'nt':
    _LIBRARY_FILE = "dd-datareader.dll"
else:
    _LIBRARY_FILE = "libdd-datareader.so"

try:
    _CURRENT_SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
    _DEFAULT_LIBRARY_PATH = os.path.join(_CURRENT_SCRIPT_PATH, "..", "..", "..", "bin")
    os.environ["PATH"] += os.pathsep + _DEFAULT_LIBRARY_PATH
except:
    pass

_LIBRARY = ctypes.cdll.LoadLibrary(_LIBRARY_FILE)


class CDataCursor():
    def __init__(self, Database):
        self._Labels = Labels_t()
        self._Image = None

        Constructor = _LIBRARY.CDataReader_createCursor
        Constructor.restype  = ctypes.c_void_p
        Constructor.argtypes = [ctypes.c_void_p]

        self._Object = ctypes.c_void_p(Constructor(Database))


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._Object != None:
            _LIBRARY.CDataEntry_destroy(self._Object)
            self._Object = None


    def __del__(self):
        if self._Object != None:
            _LIBRARY.CDataEntry_destroy(self._Object)
            self._Object = None

    @property
    def Key(self):
        if self._Object != None:
            Getter = _LIBRARY.CDataEntry_getKey
            Getter.restype = ctypes.c_uint64
            return Getter(self._Object)

    @property
    def ImageWidth(self):
        if self._Object != None:
            Getter = _LIBRARY.CDataEntry_getImageWidth
            Getter.restype = ctypes.c_uint32
            return Getter(self._Object)

    @property
    def ImageHeight(self):
        if self._Object != None:
            Getter = _LIBRARY.CDataEntry_getImageHeight
            Getter.restype = ctypes.c_uint32
            return Getter(self._Object)

    @property
    def Labels(self):
        if self._Object != None:
            Getter = _LIBRARY.CDataEntry_getLabels
            Getter.argtypes = [ctypes.c_void_p, ctypes.POINTER(Labels_t)]
            Getter(self._Object, self._Labels)
            return self._Labels

    @property
    def Image(self):
        if self._Object != None:
            if self._Image is None:
                self._Image = np.zeros([self.ImageHeight, self.ImageWidth, 3], dtype=np.uint8)

            elif self._Image.shape[0] != self.ImageHeight or self._Image.shape[1] != self.ImageWidth:
                self._Image = np.zeros([self.ImageHeight, self.ImageWidth, 3], dtype=np.uint8)

            Getter = _LIBRARY.CDataEntry_getImage
            Getter.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
            Getter(self._Object, ctypes.c_void_p(self._Image.ctypes.data))
            return self._Image


    @property
    def Valid(self):
        if self._Object != None:
            Getter = _LIBRARY.CDataEntry_isValid
            Getter.argtypes = [ctypes.c_void_p]
            return Getter(self._Object)


    def next(self):
        if self._Object != None:
            Next = _LIBRARY.CDataEntry_next
            Next.argtypes = [ctypes.c_void_p]
            return Next(self._Object)

    def prev(self):
        if self._Object != None:
            Prev = _LIBRARY.CDataEntry_prev
            Prev.argtypes = [ctypes.c_void_p]
            return Prev(self._Object)

    def setKey(self, Key):
        if self._Object != None:
            Setter = _LIBRARY.CDataEntry_setKey
            Setter.argtypes = [ctypes.c_void_p, ctypes.c_uint64]
            return Setter(self._Object, Key)


class CDataReader():
    def __init__(self, DataPath):

        Constructor = _LIBRARY.CDataReader_create
        Constructor.restype  = ctypes.c_void_p
        Constructor.argtypes = [ctypes.POINTER(ctypes.c_char)]

        self._Object = ctypes.c_void_p(Constructor(DataPath.encode('utf-8')))


    def __del__(self):
        _LIBRARY.CDataReader_destroy(self._Object)


    @property
    def FirstKey(self):
        Getter = _LIBRARY.CDataReader_getFirstKey
        Getter.restype = ctypes.c_uint64
        return Getter(self._Object)


    @property
    def LastKey(self):
        Getter = _LIBRARY.CDataReader_getLastKey
        Getter.restype = ctypes.c_uint64
        return Getter(self._Object)


    def getCursor(self):
        return CDataCursor(self._Object)
