from ..internal import CBaseFactory
from .CMeasurement import CMeasurement

class CFactory(CBaseFactory):
  def __init__(self, ReaderClass):
    super().__init__(ReaderClass, CMeasurement)

  def create(self, Network, Reader, Settings = None):
    return self._Class(Network, Reader, Settings)