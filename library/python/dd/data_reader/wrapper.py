import ctypes
import os

if os.name == 'nt':
    _LIBRARY_FILE = "dd-datareader.dll"
else:
    _LIBRARY_FILE = "dd-datareader.so"

try:
    _CURRENT_SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
    _DEFAULT_LIBRARY_PATH = os.path.join(_CURRENT_SCRIPT_PATH, "..", "..", "..", "bin")
    os.environ["PATH"] += os.pathsep + _DEFAULT_LIBRARY_PATH
except:
    pass

_LIBRARY = ctypes.cdll.LoadLibrary(_LIBRARY_FILE)


class CDataCursor():
    def __init__(self, Database):
        Constructor = _LIBRARY.CDataReader_createCursor
        Constructor.restype  = ctypes.c_void_p
        Constructor.argtypes = [ctypes.c_void_p]

        self._Object = ctypes.c_void_p(Constructor(Database))


    def __enter__(self):
        pass


    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


    def __del__(self):
        if self._Object != None:
            _LIBRARY.CDataEntry_destroy(self._Object)
            self._Object = None


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