from ..internal import CBaseFactory
from .CNetwork import CNetwork

class CFactory(CBaseFactory):
  def __init__(self, ReaderClass):
    super().__init__(ReaderClass, CNetwork)

  def create(self, Reader, Settings = None):
    return self._Class(Reader, Settings)